from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
from playwright.sync_api import sync_playwright




# Define the URL of the website with the table
url = "https://sunlight.pirategames.online/"


# Initialize a MongoDB client
client = MongoClient("mongodb://localhost:27017/")  # Change the MongoDB connection string if necessary
db = client["po_db"]  # Replace "pirate_game_db" with your desired database name
collection = db["player_count"]

# Function to scrape data and store it in MongoDB
def scrape_and_store_data(playwright):
    # Send an HTTP GET request to the URL
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
            )
    page = context.new_page()
    page.goto(url)
    page.is_visible('main-container')
    html = page.inner_html('.home-headline')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    #div = soup.find('div',{'class':'home-headline'})
    player_count  = soup.find("font", {"color": "yellow"}).contents[0]


    player_data = {
        "date" : datetime.now().strftime("%d/%m %H:%M"),
        "player_count": int(player_count)
    }
    # Insert the data into MongoDB
    print(player_data)
    collection.insert_one(player_data)
    print("Data successfully scraped and stored in MongoDB.")


# Call the function to scrape and store data
with sync_playwright() as playwright:
    scrape_and_store_data(playwright)

# Close the MongoDB connection
client.close()