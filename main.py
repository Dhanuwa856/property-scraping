from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

# Set up the Chrome WebDriver
os.environ['PATH'] += r"C:\Python"
driver = webdriver.Chrome()

#  Define the URL

base_url = "https://www.zillow.com/homes/New-York,-NY_rb/"

# open the url

driver.get(base_url)
# wait for the page to load
time.sleep(5)

#  Extract data
land_listings = []
max_price = 500000
target_listings = 100

def parse_price(price_str):
  price_str = price_str.replace('$','').replace(',','')
  try:
    return int(price_str)
  except ValueError:
    return None

while len(land_listings) < target_listings:
  # Find all the listings on the current page
  land_containers = driver.find_elements(By.CSS_SELECTOR,'ul.List-c11n-8-102-0__sc-1smrmqp-0.StyledSearchListWrapper-srp-8-102-0__sc-1ieen0c-0.kquqgw.gLCZxh.photo-cards.photo-cards_extra-attribution li')
  
  for container in land_containers:
    if len(land_listings) >= target_listings:
      break
    
    try:
      price_text = container.find_element(By.CSS_SELECTOR,'span.PropertyCardWrapper__StyledPriceLine-srp-8-102-0__sc-16e8gqd-1.vjmXt').text.strip()
      price = parse_price(price_text)
    except:
      price = None  
      
    if price and price < max_price:
      try:
        address = container.find_element(By.TAG_NAME,'address').text.strip()
        
      except:
        address = 'N/A'  
      
      try:
        url_element = container.find_element(By.TAG_NAME,'a')
        url = url_element.get_attribute('href')
        
      except:
        url = "N/A"    
       
       
      try:
        published_time = container.find_element(By.CSS_SELECTOR,'span.StyledPropertyCardBadge-c11n-8-102-0__sc-tmjrig-0.bGzpMl').text.strip()
      except:
        published_time = "N/A"  
      land_listings.append((price,address,published_time,url)) 


# Close the WebDriver
driver.quit()

# Save data to a DataFrame
df = pd.DataFrame(land_listings,columns=['Price','Address','Published Time','Url'])
df.to_excel('ny_land_listings_filtered.xlsx',index=False)

print("Data scraping completed and saved to ny_land_listings_filtered.xlsx")
