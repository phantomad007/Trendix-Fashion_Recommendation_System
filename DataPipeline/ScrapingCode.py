#!/usr/bin/env python
# coding: utf-8



#product=input('enter the product you want to search')
# give the type of clothing or brands or anything here 
Fashion_type='T-Shirt'
temp_Fashion_type=Fashion_type # to dynamicly name images and save csv file
No_of_products=2000 # it will collect that many data points (give littel more than what you want to be safe side)




#importing all the libraries used
import random # used to random components or values
import time # used in sleep time (ex time.sleep(wait_time))
import pandas as pd # used to create data frames and store in csv file
import os # used to manipulate file manager
import requests # used to get image from url (ex. response = requests.get(url))
import pickle # used to handel cookies (to store and read cookies)
from bs4 import BeautifulSoup as bs # to navigate and get data from html file
from selenium import webdriver # automating web browser (does large of our work)
from selenium.webdriver.chrome.service import Service as ChromeService # Manages the ChromeDriver service for Selenium
from selenium.webdriver.firefox.service import Service as FirefoxService#Manages the GeckoDriver service for Selenium(Firefox)
from selenium.webdriver.edge.service import Service as EdgeService#Manages the EdgeDriver service for Selenium (Edge)
from webdriver_manager.chrome import ChromeDriverManager#Automatically manages the downloading and setup of ChromeDriver.
from webdriver_manager.firefox import GeckoDriverManager#Automatically manages the downloading and setup of GeckoDriver.
from webdriver_manager.microsoft import EdgeChromiumDriverManager#Automatically manages the downloading and setup of EdgeDriver.
from selenium.webdriver.chrome.options import Options as ChromeOptions#Allows you to set options for the Chrome browser
from selenium.webdriver.firefox.options import Options as FirefoxOptions#Allows you to set options for the Firefox browser.
from selenium.webdriver.edge.options import Options as EdgeOptions#Allows you to set options for the Edge browser.
from selenium.webdriver.support.ui import WebDriverWait# used to wait for certain conditions to be met before proceeding.
from selenium.webdriver.support import expected_conditions as EC #Contains a set of predefined conditions to use with WebDriverWait.
from selenium.webdriver.common.by import By#Provides a way to locate elements on a web page.
from selenium.common.exceptions import TimeoutException
#from azure.storage.blob import BlobServiceClient
from google.cloud import storage #to interact with GCS.
from datetime import datetime




#Set environment variable to authenticate with GCP.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/marad.BEN10/TrendixSpace/trendix07-4b90f367a765.json"

# Initialize the GCS client and bucket once to reuse in functions.
client = storage.Client()
bucket_name = "messydata"  # GCS bucket name
bucket = client.bucket(bucket_name)




# List of user-agents
# commented out mobile agents, as myntra using different type of page for mobile
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    #"Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1",
    #"Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.52 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.110 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    #"Mozilla/5.0 (Linux; Android 9; Pixel 3a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
]




# Function to launch a random browser with a random user-agent
def get_random_browser():
    browsers = ['chrome', 'edge']  # List of browsers available on my machine (-; pavan)
    # you can add or remove as per your needs/availability
    
    chosen_browser = random.choice(browsers)  # Randomly choose a browser to confuse and hide scraping
    
    random_user_agent = random.choice(user_agents)  # Randomly choose a user-agent from the above list
    
    # remove the if block if you are not using the browser or can add you have any other browser
    if chosen_browser == 'chrome':
        # Chrome options setup
        chrome_options = ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument(f"user-agent={random_user_agent}")
        
        # Install Chrome driver and launch browser
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        print(f"Launched Chrome Browser with user-agent: {random_user_agent}")
    
    elif chosen_browser == 'firefox':
        # Firefox options setup 
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("general.useragent.override", random_user_agent)
        firefox_options.add_argument("-width=1200")
        firefox_options.add_argument("-height=800")
        firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Example path to Firefox
        driver = webdriver.Firefox(options=firefox_options)
        
        # Install Firefox driver and launch browser
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        print(f"Launched Firefox Browser with user-agent: {random_user_agent}")
    
    elif chosen_browser == 'edge':
        # Edge options setup
        edge_options = EdgeOptions()
        edge_options.add_argument("start-maximized")
        edge_options.add_argument(f"user-agent={random_user_agent}")
        
        # Install Edge driver and launch browser
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
        print(f"Launched Edge Browser with user-agent: {random_user_agent}")
    
    elif chosen_browser == 'brave':
        # Path to Brave browser executable
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

        # Set up Brave options
        chrome_options = ChromeOptions()
        chrome_options.binary_location = brave_path
        chrome_options.add_argument(f"user-agent={random_user_agent}")
        
        # Automatically download and set up the correct ChromeDriver version
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        print(f"Launched Brave Browser with user-agent: {random_user_agent}")
    
    return driver




# Function to simulate human interaction with normal distribution delays
def human_interaction(driver):
    # Random wait times (normally distributed) between actions
    wait_time = abs(random.gauss(mu=7, sigma=1))  # mean = 7 seconds, stddev = 1 second
    time.sleep(wait_time)
    
    try:
        # Wait until the "See More" div is clickable and then click it
        see_more = WebDriverWait(driver, abs(random.gauss(mu=10, sigma=4))).until(EC.element_to_be_clickable((By.CLASS_NAME, "index-showMoreText")))
        see_more.click()
    except Exception as e:
        print(f"see_more_Click failed or Not_available")
    
    # Simulate page scroll with a normal distributions
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    mean_scroll_position = scroll_height // abs(random.gauss(mu=5, sigma=2))  # random place of the page as mean=5
    scroll_position = abs(int(random.gauss(mean_scroll_position, scroll_height // abs(random.gauss(mu=3, sigma=1)))))
    scroll_position = min(scroll_position, scroll_height)  # to Ensure we don't scroll beyond the page height
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    
    wait_time_after_scroll = abs(random.gauss(mu=5, sigma=1.5)) 
    time.sleep(wait_time_after_scroll)




# Function to handle cookies and sessions
def manage_cookies(driver, action="load"):
    cookie_file = "cookies.pkl"
    
    if action == "load":
        try:
            with open(cookie_file, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except FileNotFoundError:
            print("No saved cookies found. Starting a new session.")
    
    elif action == "save":
        with open(cookie_file, "wb") as file:
            pickle.dump(driver.get_cookies(), file)




# Not used in this code but you can use this block if needed
def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = abs(random.gauss(mu=5, sigma=2))  # Adjust this time as needed
    
    # Get the initial height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the new content to load
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Calculate the new height after scrolling
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break the loop if no more new content is loaded
        if new_height == last_height:
            break
        last_height = new_height




def scrape_website(url):
    global driver
    if driver is None:
        driver = get_random_browser()
    driver.get(url)
    
    manage_cookies(driver, action="load")  # Load cookies if available
    
    # Wait for the main content to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    scroll_to_bottom(driver)
    
    # Simulate human interaction while scraping
    human_interaction(driver)
    
    print("Page title:", driver.title)




def download_image(url, product_id, temp_Fashion_type, category):
    # Define the blob name in GCS
    blob_name = f"{temp_Fashion_type}/{category}/{temp_Fashion_type}_{category}_{product_id}.jpg"

    # Download the image
    response = requests.get(url)

    if response.status_code == 200:
        # Upload the image content to GCS
        blob = bucket.blob(blob_name)
        blob.upload_from_string(response.content, content_type='image/jpeg')
        print(f"Uploaded image to gs://{bucket_name}/{blob_name}")
        # Return the GCS path and blob name
        gcs_file_path = f"gs://{bucket_name}/{blob_name}"
        return gcs_file_path, f"{temp_Fashion_type}_{category}_{product_id}.jpg"
    else:
        print(f"Failed to download image from {url}")
        return None, None


# Removed local file system operations. Instead of saving images locally, the function uploads them directly to GCS.
# Uses the GCS bucket and blob to store images in an organized manner based on temp_Fashion_type and category.
# Returns the GCS file path and image reference name.



# this function just returns the length if our data variables or features 
# please add here if you initialize any new variables or features
# no need to input any data just call the function it will get data from global variables
def length_of_data():
    global Serial_No,Product_id,Brand_Name,category,Description,Rating,Rating_count,Price,Specifications
    global MRP_Price,Discount,size,product_description,image_ref,file_path,image_url,individual_ratings
    print('')
    print('lengths of each list is:')
    print()
    print(f"Serial_No: {len(Serial_No)}")
    print(f"Product_id: {len(Product_id)}")
    print(f"Brand_Name: {len(Brand_Name)}")
    print(f"category: {len(category)}")
    print(f"Description: {len(Description)}")
    print(f"Rating: {len(Rating)}")
    print(f"Rating_count: {len(Rating_count)}")
    print(f"Price: {len(Price)}")
    print(f"MRP_Price: {len(MRP_Price)}")
    print(f"Discount: {len(Discount)}")
    print(f"size: {len(size)}")
    print(f"product_description: {len(product_description)}")
    print(f"image_ref: {len(image_ref)}")
    print(f"file_path: {len(file_path)}")
    print(f"image_url: {len(image_url)}")
    print(f"Specifications: {len(Specifications)}")
    print(f"individual_ratings: {len(individual_ratings)}")




#this function just validates data inconsistences and makes corrections
#please add here if you initialize any new variables or features
#as the first data to appended in our code is 'Serial_No' , i used this as base. 
# no need to input any data just call the function it will get data from global variables
def data_correction():
    global Serial_No,Product_id,Brand_Name,category,Description,Rating,Rating_count,Price,Specifications
    global MRP_Price,Discount,size,product_description,image_ref,file_path,image_url,individual_ratings
    flag=0
    print('')
    print(f"data correction check at Serial_No: {len(Serial_No)}")
    if len(Serial_No)>len(Product_id):
        print(f"Product_id: {len(Product_id)}")
        Product_id.append('None')
        flag=1
    if len(Serial_No)>len(Brand_Name):
        print(f"Brand_Name: {len(Brand_Name)}")
        Brand_Name.append('None')
        flag=1
    if len(Serial_No)>len(category):
        print(f"category: {len(category)}")
        category.append('None')
        flag=1
    if len(Serial_No)>len(Description):
        print(f"Description: {len(Description)}")
        Description.append('None')
        flag=1
    if len(Serial_No)>len(Rating):
        print(f"Rating: {len(Rating)}")
        Rating.append('None')
        flag=1
    if len(Serial_No)>len(Rating_count):
        print(f"Rating_count: {len(Rating_count)}")
        Rating_count.append('None')
        flag=1
    if len(Serial_No)>len(Price):
        print(f"Price: {len(Price)}")
        Price.append('None')
        flag=1
    if len(Serial_No)>len(MRP_Price):
        print(f"MRP_Price: {len(MRP_Price)}")
        MRP_Price.append('None')
        flag=1
    if len(Serial_No)>len(Discount):
        print(f"Discount: {len(Discount)}")
        Discount.append('None')
        flag=1
    if len(Serial_No)>len(size):
        print(f"size: {len(size)}")
        size.append('None')
        flag=1
    if len(Serial_No)>len(product_description):
        print(f"product_description: {len(product_description)}")
        product_description.append('None')
        flag=1
    if len(Serial_No)>len(image_ref):
        print(f"image_ref: {len(image_ref)}")
        image_ref.append('None')
        flag=1
    if len(Serial_No)>len(file_path):
        print(f"file_path: {len(file_path)}")
        file_path.append('None')
        flag=1
    if len(Serial_No)>len(image_url):
        print(f"image_url: {len(image_url)}")
        image_url.append('None')
        flag=1
    if len(Serial_No)>len(Specifications):
        print(f"Specifications: {len(Specifications)}")
        Specifications.append('None')
        flag=1
    if len(Serial_No)>len(individual_ratings):
        print(f"individual_ratings: {len(individual_ratings)}")
        individual_ratings.append('None')
        flag=1
    if flag==0:
        print('No inconsistencies in data')
        print('')
    else:
        print('')
        print('Because of some error data updation has been corrected')
        print('')
        length_of_data()




#names to store the data scraped and names are self explanatory
# initiate the browser so i can use it as global variable through various methods
driver = None

productLink = [] # just for refernce, to loop through while scraping each product

Serial_No=[] 
Product_id=[] 
Brand_Name=[]
category=[]
Gender=[]
Description=[]
Rating=[]
Rating_count=[]
Price=[]
MRP_Price=[]
Discount=[]
size=[]
product_description=[]
image_ref=[] # i am referencing it to fashion_type and product_id to check data if needed in future.
file_path=[]
image_url=[]
Specifications=[]
individual_ratings=[]




#generating the link to scrap (works for myntra, might have change for other web sites )
url = f'https://www.myntra.com/{Fashion_type}?rawQuery={Fashion_type}&sort=popularity' # main or start page
print(url)




current_page=0




# this block gets individual product links to scrape data from main page
No_of_pages=700 # we can change this to while loop , but this works too as there are break statements 
# it will click next and product links ( the more the number the more the data)
#this blocks stop excution if we have enough data as mentioned in 'no_of_products'
start=current_page
for i in range(start,No_of_pages):
    
    try :
        # if driver is closed or crashed , new driver will be called
        if i==0: scrape_website(url)
        
        if 'driver' not in locals() or driver is None:
            temp_link=f'https://www.myntra.com/{temp_Fashion_type}?rawQuery={temp_Fashion_type}&sort=recommended'
            scrape_website(temp_link)
            print(temp_link)
        # at start it will cal scrape_website latter it will just click next as there is no need to main function again
        
        
        # to stimulate human behaviour 
        human_interaction(driver)
        
        # gets source data
        Myntra_source= driver.page_source
        # converts source data to html file
        Myntra_html= bs(Myntra_source, "html.parser")
        
        # finds class '"results-base"' which contains links of our products
        pclass=Myntra_html.find_all("ul", {"class": "results-base"})  

        # Iterate over each element in pclass to get products links (imagine this as file and looping through each line)
        for p in pclass:
            hrefs = p.find_all('a', href=True)  # Find all 'a' tags with href in each element
            for href in hrefs:
                t = href['href']  # Get the 'href' attribute
                t = "https://www.myntra.com/" + t
                 # here myntra is storing only half ref, and adding https://www.myntra.com/"
                if t not in productLink :
                    productLink.append(t)
                else: 
                    print('productLink already collected')
                    print(t)
                # breaking from inner loop if we have enough data 
                if len(productLink)==No_of_products:
                    break
            # breaking loop if we have enough data 
            if len(productLink)==No_of_products:
                break
        try:
            # find next option which will be at end of the each page
            Next_element=Myntra_html.find("li", {"class": "pagination-next"}) 
            # will wait till next buttion is clickable
            Next=WebDriverWait(driver, abs(random.gauss(mu=10, sigma=1))).until(EC.element_to_be_clickable((By.CLASS_NAME, "pagination-next")))
            # by clicking next it will move next page
            Next.click()
            print('Next button clicked')

        except TimeoutException:
            print("Next button not clicked")
        
        print(f'No of product links collected is {len(productLink)} out of {No_of_products}')
        print(f'page {i+1} is done out of {No_of_pages}')
        
        current_page+=1
    # exception handline to move on to next item if any error
    except Exception as e:
        print(f"Driver failed at {i} and error is {e}, reinitializing...")

    # Skip to the next page if we have enough
    if len(productLink)==No_of_products:
        print(f'reqired products links i.e..{No_of_products} acquired')
        break




Myntra_html




# just displaying the links we are going to scrape
for i in range(len(productLink)):
    print(f'{i+1} link is {productLink[i]}')




productLink44




#this is the main block that gets our data of each product, you can intruppted and start this block at any point
#it will extracted data from last intruppted point
#if you intruppted and run this block again, please use rull all below option, so the csv file also triggers
count = len(Serial_No)
loop_start=count
loop_end=min(len(productLink),No_of_products) # goes till reqired data poins as specified or till the data available
print(f'loops starts at product {loop_start} and goes till {loop_end}')
# loop through each product link and scraping each product

for product in range(loop_start,loop_end):
    print(f'at loop {product+1}/{(loop_end)}')
    # every time will check if driver is crashed or not , if crashed will generate new one so the code stop excuting 
    # handeled this trough try and Expect block.
    try :
        if 'driver' not in locals() or driver is None:
            driver = get_random_browser()

        #driver = get_random_browser()
        driver.get(productLink[product])

        human_interaction(driver)
        print('passes 1st checkpoint')
        
        try:
            # Wait until the "See More" div is clickable and then click it
            see_more = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "index-showMoreText")))
            see_more.click()
        except Exception as e:
            print(f"see_more_Click failed or Not_available at {product}")

        # count starts at zero , so just updating here to sore in serial number
        count+=1
        Serial_No.append(count)
        print(f'passed 2nd checkpoint : serial_no is {count}')
        # getting the source code to find tags,anchors and div ....
        Myntra_product_source= driver.page_source
        # coverting to html formart using beautiful soup  
        Myntra_product_html = bs(Myntra_product_source, "html.parser")
        print('passes html_source checkpoint')
        # finds the header tag
        brand_element= Myntra_product_html.find("h1", {"class": "pdp-title"})
        # from here its just same code blocks repeats for each feature that we extarct
        # for some we have looped through to get data if we want multiple data/text
        Brand = None
        if brand_element:
            Brand = brand_element.text.strip()  # Remove extra spaces or newlines
            Brand_Name.append(Brand)
        else:
            print(f"Brand not found at {product} Loop")
            Brand_Name.append('None')
        print('passes brand element checkpoint')
        
        a_tags = Myntra_product_html.find_all("a", {"class": "breadcrumbs-link"})

        # Access the 3rd <a> tag (index 2 since indexing starts at 0)
        if len(a_tags) >= 3:
            third_a_tag = a_tags[2]
            third_a_tag_url = third_a_tag.get('href')
            temp_category=f"{third_a_tag_url}".strip('/')
            category.append(temp_category)
        else:
            category.append('None')

        temp_product_id= None
        product_id_element = Myntra_product_html.find("span", {"class": "supplier-styleId"})
        temp_product_id = product_id_element.get_text(strip=True) if product_id_element else 'None'
        Product_id.append(temp_product_id)
        

        Product_image_element= Myntra_product_html.find('div', class_='image-grid-image')
        

        if Product_image_element:
            Product_image_element_style = Product_image_element.get('style')

            if Product_image_element_style:
                # Extract the URL from the style attribute
                url = Product_image_element_style.split('url("')[-1].split('")')[0]
                gcs_file_path,temp_image_ref=download_image(url, temp_product_id, temp_Fashion_type,temp_category)
            if gcs_file_path:
                file_path.append(gcs_file_path)
                image_ref.append(temp_image_ref)
                image_url.append(url)  
            else:
                image_url.append('None')
                file_path.append('None')
                image_ref.append('None')
                print(f'image not found in loop {product+1}/{loop_end}')

        descp_element = Myntra_product_html.find("h1", {"class": "pdp-name"})
        descp =None

        if descp_element:
            descp = descp_element.text.strip()  # Remove extra spaces or newlines
            Description.append(descp)
        else:
            print(f"Description not found at {product}")
            Description.append('None')
        print('passes 3rd checkpoint')
        Overall_rating_element = Myntra_product_html.findAll("div", {"class": "index-overallRating"})
        
        Overall_rating=None

        for i in Overall_rating_element:
            Overall_rating=i.find('div').text

        if Overall_rating:
            Rating.append(Overall_rating)
        else:
            print(f"Overall_rating not found at {product}")
            Rating.append('None')

        Overall_rating_count_element = Myntra_product_html.findAll("div", {"class": "index-ratingsCount"})
        
        Overall_rating_count=None

        for i in Overall_rating_count_element:
            Overall_rating_count = i.get_text(strip=True)

        if Overall_rating_count:
            Rating_count.append(Overall_rating_count)
        else:
            print(f"Rating_count not found at {product}")
            Rating_count.append('None')

        Price_element = Myntra_product_html.findAll("span", {"class": "pdp-price"})
        
        now_Price=None

        for i in Price_element:
            now_Price=i.get_text(strip=True)

        if now_Price:
            Price.append(now_Price)
        else:
            print(f"Price not found at {product}")
            Price.append('None')
            
        temp_MRP_Price=None

        MRP_element = Myntra_product_html.findAll("span", {"class": "pdp-mrp"})

        for i in MRP_element:
            temp_MRP_Price=i.get_text(strip=True)

        if temp_MRP_Price:
            MRP_Price.append(temp_MRP_Price)
        else:
            print(f"MRP_Price not found at {product}")
            MRP_Price.append('None')

        Discount_element = Myntra_product_html.findAll("span", {"class": "pdp-discount"})
        
        temp_Discount=None

        for i in Discount_element:
            temp_Discount=i.get_text(strip=True)
            if temp_Discount:
                Discount.append(temp_Discount)
            else:
                print(f"Discount not found at {product}")
                Discount.append('None')
        if not temp_Discount: Discount.append('None')

        tables=Myntra_product_html.find_all('div',{'class':'index-tableContainer'})
        Specifications_temp={}
        for i in tables:
            sep_tables=i.find_all('div',{'class':'index-row'})
            for j in sep_tables:
                key=j.find('div',{'class':'index-rowKey'}).get_text(strip=True)
                value=j.find('div',{'class':'index-rowValue'}).get_text(strip=True)
                Specifications_temp[key]=value
        if Specifications_temp:
            Specifications.append(Specifications_temp)
        else:
            Specifications.append('None')
        
        ratings_table=Myntra_product_html.find_all('div',{'class':'index-flexRow index-ratingBarContainer'})
        ratings_temp={}
        for i in ratings_table:
            key=i.find('span',{'class':'index-ratingLevel'}).get_text(strip=True)
            value=i.find('div',{'class':'index-count'}).get_text(strip=True)
            ratings_temp[key]=value
        
        if ratings_temp:
            individual_ratings.append(ratings_temp)
        else:
            individual_ratings.append('None')

        buttons = Myntra_product_html.find_all("button", {"class": "size-buttons-size-button size-buttons-size-button-default"})

        # Loop through the buttons to extract the size 
        temp_size= []
        for button in buttons:
            extracted_size= button.find("p", {"class": "size-buttons-unified-size"}).get_text(strip=True)
            temp_size.append(extracted_size)

        if temp_size:
            size.append(temp_size)
        else:
            print(f"size not found at {product}")
            size.append('None')    

        Product_details_element = Myntra_product_html.find_all("p", {"class": "pdp-product-description-content"})
        temp_product_description=None

        for line in Product_details_element:

            ul_element = line.find("ul")
            if ul_element:
                # Find all <li> elements within the <ul>
                li_elements = ul_element.find_all("li")
                # Extract text from each <li> and store them in a list
                temp_product_description = [li.get_text(strip=True) for li in li_elements]
            else:
                temp_product_description=line.get_text(strip=True)
                break
        if temp_product_description:
            product_description.append(temp_product_description)
        else:
            product_description.append('None')
        data_correction()
        print('passes all checkpoints Hurray !!')
    except KeyboardInterrupt:
        print(f"key board interrputed at {product}")
        print('data has been corrected as below')
        data_correction()
        break
    except Exception as e:
        print(f"Driver failed at {product} and error is {e}, reinitializing...")
        print('data has been corrected as below')
        data_correction()
        driver = get_random_browser()
        continue  # Skip to the next product
    





driver.quit()





Fashion_type = [f'{temp_Fashion_type}'] * len(Product_id)

# Create a dictionary
data = {
    'Serial_No':Serial_No,
    'Fashion_type': Fashion_type,
    'Product_id': Product_id,
    'Brand_Name': Brand_Name,
    'category': category,
#    'Gender': Gender,
    'Description': Description,
    'Rating': Rating,
    'Rating_count': Rating_count,
    'Price': Price,
    'MRP_Price': MRP_Price,
    'Discount': Discount,
    'size': size,
    'product_description': product_description,
    'image_ref': image_ref,
    'file_path': file_path,
    'image_url': image_url,
    'Specifications':Specifications,
    'Rating_as_stars':individual_ratings
}

# Create the DataFrame
df = pd.DataFrame(data)





df.tail()




# Convert the DataFrame to CSV format
csv_data = df.to_csv(index=False)

# Define the blob name in GCS
csv_blob_name = f"{temp_Fashion_type}/{temp_Fashion_type}_dataset.csv"

# Upload the CSV data to GCS
blob = bucket.blob(csv_blob_name)
blob.upload_from_string(csv_data, content_type='text/csv')

print(f"DataFrame uploaded to gs://{bucket_name}/{csv_blob_name}")






