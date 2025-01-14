
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import uuid
import datetime
import os
import requests

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/") # Use environment variable for production
DB_NAME = "twitter_trends"
COLLECTION_NAME = "trends"

# ProxyMesh Configuration (replace with your actual credentials)
PROXYMESH_USER = os.environ.get("PROXYMESH_USER")
PROXYMESH_PASSWORD = os.environ.get("PROXYMESH_PASSWORD")
PROXYMESH_ENDPOINT = f"http://{PROXYMESH_USER}:{PROXYMESH_PASSWORD}@us-east.proxymesh.com:31280"

def get_trending_topics():
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXYMESH_ENDPOINT)
        chrome_options.add_argument("--headless=new") # Run in headless mode

        driver = webdriver.Chrome(options=chrome_options) # Make sure you have ChromeDriver installed and in your PATH
        driver.get("https://twitter.com/home")

        # Wait for the trending topics to load (adjust timeout as needed)
        wait = WebDriverWait(driver, 10)
        trending_topics_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='trend']//span")))
        trending_topics = [element.text for element in trending_topics_elements[:5]]
        
        # Get IP address used by the request
        ip_address = requests.get('https://api.ipify.org').text
        driver.quit()
        return trending_topics, ip_address

    except Exception as e:
        print(f"Error during scraping: {e}")
        return None, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    unique_id = uuid.uuid4()
    trending_topics, ip_address = get_trending_topics()

    if trending_topics:
        try:
          client = MongoClient(MONGO_URI)
          db = client[DB_NAME]
          collection = db[COLLECTION_NAME]
          
          trend_data = {
              "unique_id": str(unique_id),
              "trend1": trending_topics[0] if len(trending_topics)>0 else None,
              "trend2": trending_topics[1] if len(trending_topics)>1 else None,
              "trend3": trending_topics[2] if len(trending_topics)>2 else None,
              "trend4": trending_topics[3] if len(trending_topics)>3 else None,
              "trend5": trending_topics[4] if len(trending_topics)>4 else None,
              "date_time": datetime.datetime.now(),
              "ip_address": ip_address
          }
          collection.insert_one(trend_data)
          client.close()
          return "Scraping complete and data saved to MongoDB!"
        except Exception as e:
            return f"Error connecting to MongoDB: {e}", 500
    else:
        return "Failed to retrieve trending topics.", 500

if __name__ == "__main__":
    app.run(debug=True)


# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Trending Topics</title>
</head>
<body>
    <h1>Scrape Twitter Trends</h1>
    <button onclick="scrapeData()">Scrape Data</button>
    <div id="result"></div>

    <script>
        function scrapeData() {
            fetch('/scrape')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('result').innerText = data;
                });
        }
    </script>
</body>
</html>
