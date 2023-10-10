from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
from playwright.sync_api import sync_playwright

# Define the URL of the website with the table
url = "https://sunlight.pirategames.online/ranking#gold"

# Initialize a MongoDB client
client = MongoClient("mongodb://localhost:27017/")  # Change the MongoDB connection string if necessary
db = client["po_db"]  # Replace "pirate_game_db" with your desired database name
collection = db["total_gold"]

print('test')

# Function to scrape data and store it in MongoDB
def scrape_and_store_data(playwright):
    # Send an HTTP GET request to the URL
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
            )

    page = context.new_page()
    page.goto(url)
    html = page.inner_html('.tab-content',timeout=6000000)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div',id="gold")
    table = div.find("table", {"class": "table table-striped"})

    if table:
        # Iterate through table rows, skipping the header row
        sum_gold = 0
        for row in table.find_all("tr")[1:]:
            # Extract data from the table cells
            cells = row.find_all("td")
            sum_gold += int(cells[1].text.strip().replace(",", ""))

            # Create a dictionary to store the data
        player_data = {
            "date" : datetime.now().strftime("%d/%m %H:%M"),
            "gold": sum_gold
            }
            # Insert the data into MongoDB
        print(player_data)
        collection.insert_one(player_data)
        print("Data successfully scraped and stored in MongoDB.")
    else:
        print("Table not found on the webpage.")

# Call the function to scrape and store data
with sync_playwright() as playwright:
    print('playwright')
    scrape_and_store_data(playwright)

# Close the MongoDB connection
client.close()