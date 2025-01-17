# Trendix - Fashion Recommendation System

### **Project Overview:**

The Trendix project aims to create an AI fashion outfit generator that provides personalized recommendations based on user inputs such as body type, season and occasion. By leveraging data scraped from popular fashion websites and machine learning models, the system will suggest customized outfit options for occasions such as office, party, beach and casual settings. The project combines data science, machine learning and visualization to build an intelligent system that simplifies the process of finding the ideal outfit.

**Goal:**
The goal is to create an AI-driven solution that helps users quickly find personalized fashion suggestions, considering current trends, body type and occasion.

**Data Source:** https://www.myntra.com

### **Data Scraping**

**Libraries Used:**

- Selenium: For handling browser interactions and retrieving page source data.

- WebDriver Manager: Automatically manages and installs the latest drivers, removing the need for manual downloading of drivers by version.

- Pandas: Used to structure data and convert it into a DataFrame.

- BeautifulSoup: For finding tags and scraping the required data.

- Requests: For downloading images from the web.

**Source:**

Myntra Website: Myntra is an Indian fashion e-commerce company, founded in 2007. In 2014, Myntra was acquired by Flipkart, another major e-commerce company, and a direct competitor of Amazon. In May 2018, Walmart acquired about 77% of Flipkart’s shares, which also gave them ownership of Myntra. In the financial year 2023, Myntra reported an operating revenue of ₹43.75 billion.

### **Flow of the Python Scraper Code:**

![image](https://github.com/user-attachments/assets/b1c0c885-f074-4795-a5c3-6f95b7b6dea8)

**Initial Page Visit:** The code visits the main page at 'https://www.myntra.com/{Fashion_type}?rawQuery={Fashion_type}&sort=popularity', where Fashion_type represents the desired category (e.g. shirts, t-shirts).

**Product Link Collection:** The code gathers product links from the main page and stores them in a list. It moves to the next page once all links on the current page are collected.

**Target Number of Products:** The code continues collecting individual product links until the specified target number of products is reached.

**Data Collection:** The code iterates over each product link, collecting relevant data and storing it.

The code is designed in a structured and dynamic way, requiring only the input of the category and the number of products to scrape, after which it automatically collects the data from the website. The code is also built to handle driver crashes and data inconsistencies. If the code crashes halfway through scraping and only partial data is collected for a product, the remaining fields will be filled with “None” to ensure data consistency.



