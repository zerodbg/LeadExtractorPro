from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --- Setup Chrome WebDriver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# --- Open Google Maps ---
driver.get("https://www.google.com/maps/search/software+development/")

time.sleep(5)  # wait for map and results to load

# --- Scroll to load more results ---
for _ in range(3):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

# --- Prepare list to store data ---
data = []

# --- Scrape search results ---
results = driver.find_elements(By.CSS_SELECTOR, 'div.Nv2PK')  # container for each business
for result in results[:10]:
    try:
        # Business Name
        name = result.find_element(By.CSS_SELECTOR, 'div.qBF1Pd.fontHeadlineSmall').text
        
        # Category and Address
        category_address = result.find_element(By.CSS_SELECTOR, 'div.W4Efsd').text
        
        # Phone number
        phone = ""
        spans = result.find_elements(By.CSS_SELECTOR, 'span.UsdlK')
        if spans:
            phone = spans[0].text
        
        # Rating and Reviews
        rating, reviews = "", ""
        try:
            rating_element = result.find_element(By.CSS_SELECTOR, 'span.MW4etd')
            rating = rating_element.text
            reviews_element = result.find_element(By.CSS_SELECTOR, 'span.UY7F9')
            reviews = reviews_element.text
        except:
            pass
        
        # Website link
        website = ""
        try:
            website_element = result.find_element(By.CSS_SELECTOR, 'a.lcr4fd.S9kvJb')
            website = website_element.get_attribute('href')
        except:
            pass

        # Append to data list
        data.append({
            "Name": name,
            "Category & Address": category_address,
            "Phone": phone,
            "Rating": rating,
            "Reviews": reviews,
            "Website": website
        })
        
    except Exception as e:
        continue

# --- Save data using pandas ---
df = pd.DataFrame(data)
df.to_csv("google_maps_data.csv", index=False)  # Save as CSV
df.to_json("google_maps_data.json", orient="records")  # Save as JSON
df.to_csv("google_maps_data.txt", sep="\t", index=False)  # Save as TXT with tab-separated

print("Data saved to google_maps_data.csv, google_maps_data.json, and google_maps_data.txt")

# --- Close the browser ---
driver.quit()
