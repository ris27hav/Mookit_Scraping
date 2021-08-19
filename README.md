# Mookit Scraping

I used *requests* to get the source code of the website from a downloaded html file. I tried to use requests session to get the source code from live website by first signing in and then getting the data but it didn't work. So for this purpose, I used *selenium*. After getting the html code, I used *ReGeX* to find the required data. After scraping, I used *pandas* to convert the data into a dataframe. Then I used this dataframe to create a csv file.

At the time of writing, the dynamic mode has some problem scraping the required data, though it retrieves the correct html file. I had earlier used *BeautifulSoup* and then it worked. But it needs debugging to get working with *ReGeX*.

This script is able to scrape the lecture title, week number, lecture number, lecture link, and lecture duation from the website. I will try to fix the dynamic mode if time permits.
