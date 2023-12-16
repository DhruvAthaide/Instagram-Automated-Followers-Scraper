from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os 
import re
from bs4 import BeautifulSoup
import csv

# Instagram Login Credentials
username = "Enter Your Username/Email"
password = "Enter Your Password"

# CSV file to read all user profiles provided
data = pd.read_csv("profile_links.csv", header=None, names=['Profile Links'], encoding='latin1', skipinitialspace=True, skip_blank_lines=True)

profile_links = data['Profile Links'].str.strip().tolist()

# Configuring the Chrome driver and Handling Notification Alert
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2,"profile.default_content_setting_values.cookies":2}
# Fullscreen mode
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)


# Opening the Instagram Website
driver.get("https://www.instagram.com/")

# Finding and Inputting the Username
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'username'))
)
username_field.send_keys(username)

# Finding and Inputting the Password
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'password'))
)
password_field.send_keys(password)

# Finding and Clicking the Login Button
login_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
)
login_button.click()

# Time Delay to allow Login Process
time.sleep(7)

# Create a folder to store the text files
textoutput_folder = "UnrefinedData"
os.makedirs(textoutput_folder, exist_ok=True)

# Create a folder to store the CSV files
csvoutput_folder = "RefinedData"
os.makedirs(csvoutput_folder, exist_ok=True)


# Iterate through each profile link
for profile_link in profile_links:
    try:
        # Extract the profile name from the profile link
        profile_name = profile_link.split("/")[-2]  # Assuming the profile link format is "https://www.instagram.com/{profile_name}/"

        # Adjust the profile link to include "followers" to go to the followers page of the profile
        profile_link_followers = profile_link + "followers"

        # Go to the user's profile
        driver.get(profile_link_followers)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body")))  # Wait for the page to load

        # Get the body element
        body_element = driver.find_element(By.XPATH, "//body")

        # Wait for some time to ensure the page is fully loaded before scrolling
        time.sleep(5)

        # Xpath for the Followers Page to have it focused
        target_element_xpath = "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        target_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, target_element_xpath))
        )

        # Use ActionChains to put the focus on the followers page so that it can scroll
        actions = ActionChains(driver)
        actions.move_to_element(target_element).click().perform()
        
        # Scroll the main profile page for 20 seconds
        duration_seconds = 2 * 60 * 60  # 2 Hours
        scroll_interval = 1  # Scroll every 1 second (1 scroll per second)
        total_scrolls = int(duration_seconds / scroll_interval)  # Ensure total_scrolls is an integer
        for _ in range(total_scrolls):
            try:
                # Scroll the main profile page
                body_element.send_keys(Keys.PAGE_DOWN)

                time.sleep(scroll_interval)
            except Exception as e:
                print("Error scrolling:", e)

        # Data Extraction for the Instagram Followers
        
        # Find the target element by XPath
        target_element_xpath = "//div[@role='dialog']"
        target_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, target_element_xpath))
        )

        # Get the inner text of the element using JavaScript
        element_text = driver.execute_script("return arguments[0].outerHTML;", target_element)

        # Save the text to a text file with a unique name based on the profile inside the output folder
        textoutput_file_name = os.path.join(textoutput_folder, f"{profile_name}_output.txt")
        with open(textoutput_file_name, "w", encoding="utf-8") as file:
            file.write(element_text)

        #Refining the Extracted Data
        def extract_usernames(input_file):
            with open(input_file, 'r', encoding='utf-8') as input_f:
                # Extract usernames using regex
                usernames = []
                for line in input_f:
                    span_matches = re.findall(r'dir="auto">([^<]+)</span>', line)
                    usernames.extend(span_matches)

            return usernames

        def extract_names_from_html(html_content):
            # Parse HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract names in the specified format
            names = [span.get_text(strip=True) for span in soup.find_all('span', class_='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft')]
            return names

        if __name__ == "__main__":
            # Save the text to a text file with a unique name based on the profile inside the output folder
            csvoutput_file_name = os.path.join(csvoutput_folder, f"{profile_name}_output.csv")
            
            # Paths to input and output files
            input_file = textoutput_file_name
            output_file = csvoutput_file_name

            # Extract usernames from Text File
            instagram_usernames = extract_usernames(input_file)

            # Read HTML content from Text File
            with open(input_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Extract names from Text File
            instagram_names = extract_names_from_html(html_content)

            # Combine results and write to CSV File
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Full Name', 'Username']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for name_code2, username_code1 in zip(instagram_names, instagram_usernames):
                    writer.writerow({'Full Name': name_code2, 'Username': username_code1})

            print(f"Results saved to '{output_file}'")

        # Navigate back to the user's profile
        driver.back()

    except Exception as e:
        print("Error processing profile:", profile_link, ":", e)

# Close the browser window
driver.quit()
