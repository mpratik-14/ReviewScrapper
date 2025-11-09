from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
import csv
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].strip().replace(" ", "+")
            flipkart_url = f"https://www.flipkart.com/search?q={searchString}"
            response = requests.get(flipkart_url, headers={"User-Agent": "Mozilla/5.0"})
            response.encoding = 'utf-8'
            flipkart_html = bs(response.text, "html.parser")

            bigboxes = flipkart_html.find_all("div", {"class": "cPHDOP col-12-12"})
            if len(bigboxes) <= 3:
                return "No products found. Try a different keyword."
            del bigboxes[0:3]

            productLink = None
            for box in bigboxes:
                title_tag = box.find('a', {'class': 'CGtC98'})
                title = title_tag.text.strip().lower() if title_tag else ''
                if searchString in title:
                    productLink = "https://www.flipkart.com" + title_tag['href']
                    break

            if not productLink:
                box = bigboxes[0]
                productLink = "https://www.flipkart.com" + box.div.div.div.a['href']

            print(f"🔗 Scraping product link: {productLink}")

            prodRes = requests.get(productLink, headers={"User-Agent": "Mozilla/5.0"})
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")

            commentboxes = prod_html.find_all('div', {'class': "RcXBOT"})
            if not commentboxes:
                return "No reviews found for this product."

            reviews = []
            for commentbox in commentboxes:
                name = commentbox.find('p', {'class': '_2NsDsF AwS1CA'})
                rating = commentbox.find('div', {'class': 'XQDdHH Ga3i8K'})
                commentHead = commentbox.find('p', {'class': 'z9E0IG'})
                comment_div = commentbox.find('div', {'class': 'ZmyHeo'})

                if comment_div:
                    read_more = comment_div.find('span', {'class': 'wTYmpv'})
                    if read_more:
                        read_more.decompose()
                    comment = comment_div.get_text(strip=True)
                else:
                    comment = 'No Comment'

                mydict = {
                    "Product": searchString.replace("+", " "),
                    "Name": name.text.strip() if name else 'No Name',
                    "Rating": rating.text.strip() if rating else 'No Rating',
                    "CommentHead": commentHead.text.strip() if commentHead else 'No Heading',
                    "Comment": comment
                }
                reviews.append(mydict)

            filename = f"{searchString.replace('+', '_')}.csv"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Product", "Name", "Rating", "CommentHead", "Comment"])
                writer.writeheader()
                writer.writerows(reviews)

            print(f"✅ CSV saved at: {filepath}")

            return render_template('results.html', reviews=reviews)

        except Exception as e:
            print('❌ Exception:', e)
            return f"Error: {str(e)}"
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
