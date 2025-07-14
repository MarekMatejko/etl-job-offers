from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from sqlalchemy import create_engine
import os

# Basic settings
BASE_URL = "https://justjoin.it"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
}

# Scroll + Link collection (selenium)
def create_driver():
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless")  # To run in mode without GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")  
    options.add_argument("window-size=1920x1080")  # Resolution setting

    # Starting the Chrome browser
    driver = webdriver.Chrome(options=options)
    return driver


def save_to_postgres(df):
    db_user = os.getenv("DB_USER", "scraper_user")
    db_pass = os.getenv("DB_PASS", "scraper_pass")
    db_name = os.getenv("DB_NAME", "scraper_db")
    db_host = os.getenv("DB_HOST", "db")  # Base container name
    db_port = os.getenv("DB_PORT", "5432")

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

    df.to_sql("job_offers", engine, if_exists="replace", index=False)  # For now we replace data
    print("✅ Data saved to PostgresQL.")


def collect_offer_links():
    driver = create_driver()
    driver.get(BASE_URL)
    time.sleep(5)

    offers_collected = set()
    total_scroll = 3000
    step = 300
    delay = 0.5
    current_position = 0

    while current_position < total_scroll:   #while current_position < scroll_height: For now only few scrols
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(delay)
        current_position += step

        offers = driver.find_elements(By.CSS_SELECTOR, "a[href^='/job-offer/']")
        for offer in offers:
            href = offer.get_attribute("href")
            if href:
                if href.startswith("/job-offer/"):
                    href = BASE_URL + href
                offers_collected.add(href)

    driver.quit()
    return list(offers_collected)


# Parsing pages of offers (BEAUTIFULSOUP)
def parse_offer_page(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Empty"

        # Company i Location
        company = "Empty"
        location = "Empty"

        company_tag = soup.find("h2", class_="MuiTypography-body1")
        if company_tag:
            company = company_tag.text.strip()

        location_tag = soup.find("span", class_="mui-1o4wo1x")
        if location_tag:
            location = location_tag.text.strip()

        # Salary
        salary = "Empty"
        salary_tag = soup.find(lambda tag: tag.name == "span" and "PLN" in tag.text)
        if salary_tag:
            salary = salary_tag.text.strip()

        # Stack
        stack = []
        tech_boxes = soup.select("div.MuiBox-root.mui-qsaw8")
        for box in tech_boxes:
            name_tag = box.find("h4")
            level_tag = box.find("span")
            if name_tag:
                tech_name = name_tag.text.strip()
                tech_level = level_tag.text.strip() if level_tag else "Empty"
                stack.append(f"{tech_name} ({tech_level})")

        return {
            "url": url,
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "stack": stack
        }

    except Exception as e:
        print(f"Error while processing  {url}: {e}")
        return None

# Main function
if __name__ == "__main__":
    offer_links = collect_offer_links()

    print(f"\n🔎 Gathered {len(offer_links)} links. I start processing..\n")
    
    all_offers = []
    for i, link in enumerate(offer_links[:30]):  # You can change how much you want
        print(f"[{i+1}] {link}")
        details = parse_offer_page(link)
        if details:
            all_offers.append(details)
        time.sleep(1)  # Server pause

    df = pd.DataFrame(all_offers)
    # print("\n📊 Table of offers:")
    # print(df)

    # Save to the file
    # df.to_csv("job_offers_full.csv", index=False)
    save_to_postgres(df)
    print("\n💾 Data to the PostgresQL database was saved.")