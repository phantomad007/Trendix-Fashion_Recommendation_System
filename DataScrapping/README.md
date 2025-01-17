# Libraries Used:
## Selenium: for operating browser interactions and getting page source
## WebDriver Manager : to automatically manage and install latest driver instead of manually downloading driver as per version
## Pandas : to structure data and convert it as dataframe
## beautifulsoup4 : to find tags and scrap the data.
## Requests : for downloading images from web

# Flow of the code:
1)	First the code will visit the main page
      'https://www.myntra.com/{Fashion_type}?rawQuery={Fashion_type}&sort=popularity'
      Here “Fashion type” will be whatever category we want scrap ex. Shirts, T shirts, etc...
2)	Next, the code will collect links of products from the main page and store in list, it will move to next page once it collects all the links 
3)	It will collect individual product  links until we hit our target number “No of products”
4)	Now code will iterate over each product link and collects data and stores them

Written Python code for Scraping data from Myntra.
designed in structured and dynamic manner, we just need to give category and no of products we want to scrap, it will automatically collect data from the site. 
code is Designed  in way it will deal with driver crashes and data inconsistencies if any. 

If by any change the code breaks in halfway and collected only half of the data for a product remaining category will be filled as “None”, so the data stays consistent with products.

# User Defined Functions:

1)	get_random_browser():

    Input : don’t need any input , but it access list of user agents declared and assigined to global variable “User_agent”
    
    Output/Returns : returns a random browser (i.e. one of chrome, edge, firefox or Brave) with random user agent  

2)	human_interaction(driver):
      
   Input: takes driver as input 
   Purpose: scroll to random position of pages to imitate human behaviour 
   Output/Returns: Nothing


3)	manage_cookies(driver, action="load")

    Input:  driver and action “load/save” , by default it is set to load
    Output/Returns: returns nothing, it will add cookies to drivers if any or save cookies to cookie file

4)	scroll_to_bottom(driver):
    
    Input: takes driver as input
    Output/Returns: scroll to bottom of the page so the next buttion at end of the page becomes clickable

5)	scrape_website(url):
    
    Input: takes url as input
    
    Purpose : access driver as global variable and if there is no driver initializes new one and calls flowing functions 
          i.	if driver is None:
                  driver = get_random_browser()
          ii.	manage_cookies(driver, action="load")
          iii.	will wait until body tag is present
          iv.	human_interaction(driver)
          v.	scroll_to_bottom(driver)
    
6)	download_image(url, product_id,  Fashion_type,category):

    Input : takes url of the image, product_id , fashion_type ( shirts/shoes/trousers etc…)
    	And category (ex.. women/men/boys/girl etc..)
    
    Purpose: saves the image file in pre_defined library
    Names the file with unique name i.e.  {temp_Fashion_type}_{category}_{product_id}.jpg" and Returns file path and file name 

7)	 length_of_data():

     Input: nothing , it will access all the variables globally.
     Purpose: when called , prints the length of list of variables we are storing our data

8)	data_correction():
    
    Input: nothing , function access all the variables globally 
    Purpose : when called compares length of list variables against serial no and appends none if lengths don’t match to maintain constancy




