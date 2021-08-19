import requests
import pandas as pd
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import getpass
import re


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num_lecs", help="number of lectures to scrap details", type=int, default=10)
parser.add_argument("-s", "--start_from", help="start scraping from lecture number", type=int, default=1)
parser.add_argument("--url", help="url of the lecture to scrap", type=str, default="https://raw.githubusercontent.com/ris27hav/Mookit_Scraping/main/ESO204A_%20Fluid%20Mechanics%20And%20Rate%20Processes.html?token=ARZX5DJHGZUHGXZIX6TPJW3BE2A6K")
parser.add_argument("--mode", help="mode of scraping", type=str, default="static")
parser.add_argument("--path", help="path to chrome driver", type=str, default="D:/chromedriver.exe")
args = parser.parse_args()


if args.mode == 'dynamic':
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(args.path, options=chrome_options)
    driver.get("https://hello.iitk.ac.in/index.php/user/login")

    id = input("Enter your CC id: ")
    pwd = getpass.getpass('Enter your CC password:')
    login = driver.find_element_by_xpath("//input[@name='name']").send_keys(id)
    password = driver.find_element_by_xpath("//input[@name='pass']").send_keys(pwd)
    submit = driver.find_element_by_xpath("//input[@value='SIGN IN']").click()

    driver.get(args.url)
    html_data = str(driver.page_source)

elif args.mode == 'static':
    html_data = requests.get(args.url).text


html_data = html_data.replace('\n', ' ')

week_list = re.findall(r'<div _ngcontent-c2="" class="weekWrapper">(.+?)</div>', html_data)
week_data_list = re.findall(r'<ul _ngcontent-c2="" class="weekList">(.+?)</ul>', html_data)

data = {
    'week': [],
    'lecture title': [],
    'lecture name': [],
    'duration': [],
    'link': [],
}

for week, week_data in zip(week_list, week_data_list):
    week_title = week.strip()
    week_list_items = re.findall(r'<li _ngcontent-c2="">(.+?)</li>', week_data)
    
    for item in week_list_items:
        cur_lec_title = re.findall(r'</span>(.+?)</span>', item)[0].strip()
        cur_lec_data = re.findall(r'<span _ngcontent-c2="">(.+?)</span>', item)
        
        for lec in cur_lec_data:
            lec_name = re.findall(r'<div _ngcontent-c2="" class="lectureInfoBoxText">(.+?)</div>', lec)[0].strip()
            lec_url = re.findall(r'<a _ngcontent-c2="" href="(.+?)">', lec)[0].strip()
            lec_dur = re.findall(r'<span _ngcontent-c2="">(.+)', lec)[0].strip()

            data['week'].append(week_title)
            data['lecture title'].append(cur_lec_title)
            data['lecture name'].append(lec_name)
            data['duration'].append(lec_dur)
            data['link'].append(lec_url)

to_lec = min(args.start_from + args.num_lecs - 1, len(data['week']))
for label, lists in data.items():
    data[label] = lists[args.start_from - 1 : to_lec]

pd_data = pd.DataFrame(data)
pd_data.to_csv('scraped_data.csv')
