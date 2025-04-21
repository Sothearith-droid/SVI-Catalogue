from flask import Flask, render_template
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Google Sheets authentication
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Load credentials from environment variable
try:
    service_account_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
except KeyError:
    raise RuntimeError("GOOGLE_CREDENTIALS environment variable not set")


# Authorize the client
client = gspread.authorize(creds)

# Load Google sheet
SHEET_NAME = "Products"
sheet = client.open(SHEET_NAME)

def convert_link(link):
    """Convert Google drive file link to direct image URL"""
    if "https://drive.google.com" in link:
        try:
            file_id = link.split("/d/")[1].split("/")[0]    # extract file ID
            return f"https://lh3.googleusercontent.com/d/{file_id}"
        except IndexError:
            return link # return original link if format is incorrect
    return link # return original link if not Google Drive link

def sheet_to_dict(worksheet):
    data = worksheet.get_all_values()
    headers = data[0]
    return [dict(zip(headers, row)) for row in data[1:]]

# Route to display all categories
@app.route('/category')
def all_category():
    try:
        category_worksheet = sheet.worksheet('Category')
        category_data = category_worksheet.get_all_values()

        slideshow_worksheet = sheet.worksheet('Slideshow')
        slideshow_data = slideshow_worksheet.get_all_values()
        
        headers = category_data[0]
        slideshow = [dict(zip(headers, row)) for row in slideshow_data[1:]]
        categories = [dict(zip(headers, row)) for row in category_data[1:]]

        for cat in categories:
            cat["Category Icon"] = convert_link(cat["Category Icon"])

        for slide in slideshow:
            slide["Category Icon"] = convert_link(slide["Category Icon"])

        return render_template('all_categories.html', all_categories=categories, slideshow=slideshow)
    except gspread.exceptions.WorksheetNotFound:
        return render_template("404.html"), 500

# Route to display all products in a category
@app.route('/category/<category_name>')
def show_category(category_name):
    try:
        worksheet = sheet.worksheet(category_name)  # open the sheet based on category name
        data = worksheet.get_all_values()   # fetch all data
        headers = data[0]   # first row i.e., column name
        products = [dict(zip(headers, row)) for row in data[1:]]    # convert all rows into dictionary

        category_worksheet = sheet.worksheet('Category')
        category_data = category_worksheet.get_all_values()
        cat_headers = category_data[0]
        categories = [dict(zip(cat_headers, row)) for row in category_data[1:]]

        # convert image links
        for product in products:
            product["Image 1"] = convert_link(product["Image 1"])
            # product["Image 2"] = convert_link(product["Image 2"])
            # product["Image 3"] = convert_link(product["Image 3"])
            # product["Image 4"] = convert_link(product["Image 4"])
            # product["Image 5"] = convert_link(product["Image 5"])
            # product["Image 6"] = convert_link(product["Image 6"])

        return render_template('one_category.html', all_categories=categories, category=category_name, products=products)
    except gspread.exceptions.WorksheetNotFound:
        return render_template("404.html"), 500

# Route to display a single product
@app.route('/category/<category_name>/<product_id>')
def show_product(category_name, product_id):
    try:
        worksheet = sheet.worksheet(category_name)
        data = worksheet.get_all_values()
        headers = data[0]
        products = [dict(zip(headers, row)) for row in data[1:]]

        category_worksheet = sheet.worksheet('Category')
        category_data = category_worksheet.get_all_values()
        cat_headers = category_data[0]
        categories = [dict(zip(cat_headers, row)) for row in category_data[1:]]

        # Find the product by id
        product = next((p for p in products if p["ProductID"] == product_id), None)

        if not product:
            return render_template("404.html"), 500
        else:
            for i in range(1, 7):
                key = f"Image {i}"
                if key in product:
                    product[key] = convert_link(product[key])

        return render_template("product.html", all_categories=categories, product=product)
    except gspread.exceptions.WorksheetNotFound:
        return render_template("404.html"), 500

@app.route('/contact')
def find_us():
    category_worksheet = sheet.worksheet('Category')
    category_data = category_worksheet.get_all_values()
    cat_headers = category_data[0]
    categories = [dict(zip(cat_headers, row)) for row in category_data[1:]]
    return render_template("find_us.html", all_categories=categories)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)