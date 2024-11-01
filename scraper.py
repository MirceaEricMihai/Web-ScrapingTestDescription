from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Set up Chrome WebDriver with the path to chromedriver
service = Service("C:/Users/Eric/Desktop/WebScrapingProject/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the website
driver.get("https://www.citygross.se/matvaror")

# Accept cookies if the cookie banner appears
try:
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Tillåt alla')]"))
    ).click()
except:
    print("No Cookiebot pop-up found or unable to close it")

# Open a CSV file for writing with UTF-8 encoding (including BOM for Excel compatibility)
with open('citygross_products_output.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Name", "Description", "Price"])

    # Define the list of categories with their names and CSS selectors
    categories = [
        {"name": "Kött & fågel", "selector": "#viewport > aside.b-secondary-nav.noticeHidden > nav > span:nth-child(14) > a > div > div > div.sc-uhnfH.fNQNlz > div"},
        {"name": "Frukt & grönt", "selector": "#viewport > aside.b-secondary-nav.noticeHidden > nav > span:nth-child(15) > a > div > div > div.sc-uhnfH.fNQNlz > div"},
        {"name": "Mejeri, ost & ägg", "selector": "#viewport > aside.b-secondary-nav.noticeHidden > nav > span:nth-child(16) > a > div > div > div.sc-uhnfH.fNQNlz > div"},
    ]

    # Loop through each category
    for category in categories:
        try:
            # Scroll to the category menu to make it visible
            category_menu = driver.find_element(By.CSS_SELECTOR, "#viewport > aside.b-secondary-nav.noticeHidden > nav")
            driver.execute_script("arguments[0].scrollIntoView();", category_menu)
            time.sleep(1)  # Wait for the scroll to complete

            # Scroll specifically to the target category element in the menu
            target_category = driver.find_element(By.CSS_SELECTOR, category["selector"])
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_category)
            time.sleep(1)  # Small delay to ensure it's in view
            
            # Click on the current category
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, category["selector"]))
            ).click()
            time.sleep(2)  # Wait for the category page to load

            # Iterate through the first two pages in each category
            for page_num in range(2):  # Index starts from 0, so this extracts data from two pages
                
                # Scroll to the bottom of the page to load all products
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for products to load after scrolling

                # Locate all product elements on the current page
                products = driver.find_elements(By.CSS_SELECTOR, "#b-main > div > div > div.grid-container-mobileGutter > div")
                for product in products:
                    try:
                        # Extract product name
                        name = product.find_element(By.CSS_SELECTOR, "div.details > h2").text
                        
                        # Extract product description
                        description = product.find_element(By.CSS_SELECTOR, "div.details > h3").text
                        
                        # Attempt to extract product price with multiple selectors
                        try:
                            price = product.find_element(By.CSS_SELECTOR, "div.price-section.full-width.end-end.mt-10 > div.c-pricetag-grid").text
                        except:
                            try:
                                price = product.find_element(By.CSS_SELECTOR, "div.price-section.center-center.mt-10 > div").text
                            except:
                                try:
                                    price = product.find_element(By.CSS_SELECTOR, "#b-main > div > div > div.grid-container-mobileGutter > div:nth-child(7) > a > div.product-card__lower-container > div.push-to-bottom.push-to-bottom--ie-support.full-width > div.price-section.center-center").text
                                except:
                                    price = "Unavailable"  # Default text if price is missing

                        # Write product details to the CSV file
                        writer.writerow([category["name"], name, description, price])
                        print(f"Found product - Name: {name}, Price: {price}")
                    except Exception as e:
                        print("Error extracting data for a product:", e)

                # After extracting products on the first page, navigate to the second page
                if page_num == 0:  # Only attempt to navigate if on the first page
                    try:
                        # Find and click the button for the second page in pagination
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#b-main > div > div > div.c-pagination > div > div > div > div:nth-child(3) > button"))
                        )
                        driver.execute_script("arguments[0].click();", next_button)
                        print("Navigating to page 2...")
                        time.sleep(3)  # Wait for the second page to load
                    except Exception as e:
                        print(f"Could not navigate to page 2 in category: {category['name']}. Error: {e}")
                        break

            print(f"Finished scraping category: {category['name']}")

        except Exception as e:
            print(f"Could not click on category: {category['name']}. Error: {e}")

# Close the browser
driver.quit()
print("Scraping completed.")
