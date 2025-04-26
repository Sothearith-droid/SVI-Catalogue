from flask import Flask, render_template
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from dotenv import load_dotenv
from flask_caching import Cache
from flask import send_from_directory
from datetime import timedelta
import logging
import time

load_dotenv()

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Google Sheets authentication
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Load credentials from environment variable
try:
    service_account_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
except KeyError:
    app.logger.error("GOOGLE_CREDENTIALS environment variable not set")
    raise RuntimeError("GOOGLE_CREDENTIALS environment variable not set")

# Authorize the client
client = gspread.authorize(creds)

# Load Google sheet
SHEET_NAME = "Products"
sheet = client.open(SHEET_NAME)

# Configure cache
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=1)

def convert_link(link):
    """Convert Google drive file link to direct image URL"""
    if "https://drive.google.com" in link:
        try:
            file_id = link.split("/d/")[1].split("/")[0]
            return f"https://lh3.googleusercontent.com/d/{file_id}"
        except IndexError:
            app.logger.warning("Failed to convert Google Drive link: %s", link)
            return link
    return link

@cache.cached(timeout=300)  # cache for 5 minutes
def get_category_data():
    app.logger.info("Fetching category data")
    category_worksheet = sheet.worksheet('Category')
    data = category_worksheet.get_all_values()
    headers = data[0]
    return [dict(zip(headers, row)) for row in data[1:]]

@cache.cached(timeout=300)  # cache for 5 minutes
def get_slideshow_data():
    app.logger.info("Fetching slideshow data")
    slideshow_worksheet = sheet.worksheet('Slideshow')
    data = slideshow_worksheet.get_all_values()
    headers = data[0]
    return [dict(zip(headers, row)) for row in data[1:]]

@app.route('/')
def home():
    return all_category()

@app.route('/category')
def all_category():
    try:
        app.logger.info("User accessed /category")
        categories = get_category_data()
        slideshow = get_slideshow_data()

        for cat in categories:
            cat["Category Icon"] = convert_link(cat["Category Icon"])
        for slide in slideshow:
            slide["Slide Category Icon"] = convert_link(slide["Slide Category Icon"])
        return render_template('all_categories.html', all_categories=categories, slideshow=slideshow)
    except gspread.exceptions.WorksheetNotFound:
        app.logger.error("Category or Slideshow worksheet not found")
        return render_template("404.html"), 500

@app.route('/category/<category_name>')
@cache.cached()
def show_category(category_name):
    try:
        app.logger.info("User accessed category: %s", category_name)
        worksheet = sheet.worksheet(category_name)
        data = worksheet.get_all_values()
        headers = data[0]
        products = [dict(zip(headers, row)) for row in data[1:]]

        categories = get_category_data()

        for product in products:
            if "Image 1" in product:
                product["Image 1"] = convert_link(product["Image 1"])

        return render_template('one_category.html', all_categories=categories, category=category_name, products=products)
    except gspread.exceptions.WorksheetNotFound:
        app.logger.warning("Worksheet not found for category: %s", category_name)
        return render_template("404.html"), 500

@app.route('/category/<category_name>/<product_id>')
@cache.cached()
def show_product(category_name, product_id):
    try:
        app.logger.info("User requested product %s in category %s", product_id, category_name)
        worksheet = sheet.worksheet(category_name)
        data = worksheet.get_all_values()
        headers = data[0]
        products = [dict(zip(headers, row)) for row in data[1:]]

        categories = get_category_data()

        product = next((p for p in products if p["ProductID"] == product_id), None)

        if not product:
            app.logger.warning("Product ID not found: %s", product_id)
            return render_template("404.html"), 500
        else:
            for i in range(1, 7):
                key = f"Image {i}"
                if key in product:
                    product[key] = convert_link(product[key])

        return render_template("product.html", all_categories=categories, product=product)
    except gspread.exceptions.WorksheetNotFound:
        app.logger.error("Worksheet not found for category: %s", category_name)
        return render_template("404.html"), 500

@app.route('/contact')
def find_us():
    app.logger.info("User accessed contact page")
    categories = get_category_data()
    return render_template("find_us.html", all_categories=categories)

@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning("404 error occurred: %s", e)
    return render_template("404.html"), 404

@app.context_processor
def inject_timestamp():
    return {'version': int(time.time())}

if __name__ == '__main__':
    app.run()
