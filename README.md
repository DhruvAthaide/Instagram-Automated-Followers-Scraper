# Instagram Automated Followers Scraping Tool

I have created a Instagram Automated Followers Scraping Tool using Python to scrape all the followers of the profile links you provide using selenium!


## Installation

To install and run this project,

You can download the zip file or Clone the Project Repository using Git with the below command:
```bash
git clone https://github.com/DhruvAthaide/Instagram-Automated-Followers-Scraper.git
```

Once, you have installed the Repository then you can cd into the directory and pip install the requirements needed to run the tool:
```bash
cd Instagram-Automated-Followers-Scraper
```

```bash
pip install -r requirements.txt
```

Then, you need to create a CSV File or Excel File and name it:
```bash
Name: profile_links.csv
```

Then, you need to set the following column name in the Excel File and paste the Instagram profile's link you want to message in this column:
```bash
Column 1: Profile Links
```

Then, in the 'Instagram.py' file on Line 16 & 17 Enter your Username/Email ID and Password in between the Quotes for the String:
```bash
username = "Enter Your Username/Email"
password = "Enter Your Password"
```

If you want to change how many hours it will scrape each profile's followers list, then change the following line to suit the time you want (Scrolling for above 2 hours might get the account suspended if done too frequently):
```bash
duration_seconds = 2 * 60 * 60  # 2 Hours
```

If you want to change how many scrolls per second, then change the following line to suit your neeeds:
```bash
scroll_interval = 1  # Scroll every 1 second (1 scroll per second)
```

Then, you can simply run the python file and not touch anything and it will execute the message sending to the Instagram profile's provided in the CSV or Excel File and all the profile link's followers will appear in a csv file in the RefinedData Folder and if you want the Unrefined Data it will be in the UnrefinedData Folder.

## Authors

- [@Dhruv Athaide](https://github.com/DhruvAthaide)


## Languages & Tools Used:
<p align="left"> 
<a href="https://www.python.org/" target="_blank" rel="noreferrer"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.selenium.dev/" target="_blank" rel="noreferrer"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg" alt="selenium" width="40" height="40"/> </a>
</p>