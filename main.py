import seleniumwire.undetected_chromedriver as selwire_driver
import undetected_chromedriver as sel_driver
# from seleniumwire import webdriver  as selwire_driver 
# from selenium import webdriver as sel_driver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import csv
import io
import gzip
import os
import re


# Change Download Directory, Email & Password here
download_dir = "/Users/mian/ScrapedData/Google Rec/Scraped_Data"
email = "rita@mosaicdesignlabs.com"
password = "mosaictest123"

columns = ["audioId", "fileName Audio", "fileName Trans", "Location", "Duration", "Title", "Tags", "Date", "Time", "Latitude", "Longitude"]
with open(f'{download_dir}/Metadata.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    print("CSV file created successfully.")


options = sel_driver.ChromeOptions()

# Set download directory preferences
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "savefile.default_directory": download_dir,
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')



selenium_driver = sel_driver.Chrome(
     service=Service(ChromeDriverManager().install()), 
    options=options,

)

selWire_options = selwire_driver.ChromeOptions()
selWire_options.add_argument('--ignore-ssl-errors=yes')
selWire_options.add_argument('--ignore-certificate-errors')
selWire_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "savefile.default_directory": download_dir,
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

selWiredriver= selwire_driver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=selWire_options,

)

selWiredriver.maximize_window()
selenium_driver.maximize_window()


selWiredriver.scopes = [
    '.*pixelrecorder-pa.clients6.google.com.*'  
]

def SignIn():
    
    # email input
    email_input = selWiredriver.find_element(By.TAG_NAME, "input")
    email_input.send_keys(email)
    time.sleep(2)

    next_btn = selWiredriver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    next_btn.click()
    time.sleep(4)

    # password input
    password_input = selWiredriver.find_element(By.NAME, "Passwd")
    password_input.send_keys(password)
    time.sleep(2)

    next_btn = selWiredriver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    next_btn.click()
    time.sleep(4)
    return

def SignInSelenium():
    
    # email input
    email_input = selenium_driver.find_element(By.TAG_NAME, "input")
    email_input.send_keys(email)
    time.sleep(2)

    next_btn = selenium_driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    next_btn.click()
    time.sleep(4)

    # password input
    password_input = selenium_driver.find_element(By.NAME, "Passwd")
    password_input.send_keys(password)
    time.sleep(2)

    next_btn = selenium_driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    next_btn.click()
    time.sleep(4)
    return

def parse_duration(duration):
    # Check if duration contains hours
    if len(duration.split(":")) == 3:
        # Format is HH:MM:SS
        hours, minutes, seconds = map(int, duration.split(":"))
        total_seconds = 35
    else:
        # Format is MM:SS
        minutes, seconds = map(int, duration.split(":"))
        print(f"Minutes  : {minutes}")
        if minutes > 0:
            if minutes > 30:
                total_seconds = 30
            else:
                total_seconds = 20

        else:
            if seconds > 30:
                total_seconds  = 10
            else:
                total_seconds = 8
    
    return total_seconds

# selWiredriver.minimize_window()
selWiredriver.get("https://www.google.com/")
time.sleep(3)

try:
    # SignIn Button click
    signin_btn = selWiredriver.find_element(By.LINK_TEXT, "Sign in")
    signin_btn.click()
    time.sleep(3)
    SignIn()

except Exception as e:
    print("Already SignIn")
    print(e)

selWiredriver.get("https://recorder.google.com/")
time.sleep(15)

main_window_root = selWiredriver.find_element(By.TAG_NAME, "recorder-main").shadow_root
side_bar = main_window_root.find_element(By.CSS_SELECTOR, "recorder-sidebar")

side_bar_root = side_bar.shadow_root

recorder_sidebar_items = side_bar_root.find_element(By.CSS_SELECTOR, "recorder-sidebar-items")
recorder_sidebar_items_root = recorder_sidebar_items.shadow_root


rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

section_scroll = recorder_sidebar_items_root.find_element(By.CSS_SELECTOR, "div.items > ul.library-list")


# infinit scroll new version
# item_1 = rec_items[0]
# item_1.click()

# while True:
#     # updated recording list
#     rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

#     last_rec_item = rec_items[len(rec_items)-1]
#     recorder_sidebar_item_root = last_rec_item.find_element(By.CSS_SELECTOR, "recorder-sidebar-item").shadow_root
#     recorder_metadata_root =  recorder_sidebar_item_root.find_element(By.CSS_SELECTOR, "recorder-metadata").shadow_root
    
#     # title
#     title = recorder_metadata_root.find_element(By.CSS_SELECTOR, '.title-wrapper .title .rest').text
#     print(f"title : {title}")

#     if title == "last":
#         break

#     for i in range(0,8):
#          last_rec_item.send_keys(Keys.PAGE_DOWN)
         
#     time.sleep(5)




#  old version infinite scroll
if rec_items:
    item_1 = rec_items[0]
    item_1.click()

 
    last_height = selWiredriver.execute_script("return arguments[0].scrollHeight", section_scroll)
    
    while True:
       

            rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

            last_rec_item = rec_items[len(rec_items)-1]

            for i in range(0,8):
                last_rec_item.send_keys(Keys.PAGE_DOWN)
            time.sleep(5)

            new_height =  selWiredriver.execute_script("return arguments[0].scrollHeight", section_scroll)
            

            if new_height == last_height:
                break

            last_height = new_height

    print("Scrolled to the bottom")
else:
    print("No items found to click.")

server_audio_list = []

# Tracing requests
for request in selWiredriver.requests:
    if "https://pixelrecorder-pa.clients6.google.com/$rpc/java.com.google.wireless.android.pixel.recorder.protos.PlaybackService/GetRecordingList" in request.url:
        # print("Request URL:", request.url)
        # print("Request Method:", request.method)
        # print("Request Headers:", request.headers)


        try:
            if request.response.body:
              
                if request.response.headers.get("Content-Encoding") == "gzip":
           
                    content = gzip.decompress(request.response.body)
                else:
                    content = request.response.body

                
                
                body_json = json.loads(content.decode('utf-8'))
                for event in body_json[0]:  
                    latitude = event[4]
                    longitude = event[5]
                    title = event[1]
                    audioId = event[13]
    
                    # print("Latitude:", latitude)
                    # print("Longitude:", longitude)
                    # print("Title:", title)
                    # print("Audio ID:", audioId)
                    # print("                    ")

                    server_audio_list.append({"title" : title, "audioId" : audioId, "lat" : latitude, "long": longitude})


               
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Response Body:", content.decode('utf-8'))  
        except Exception as ex:
            print("Error processing response:", ex)

        print("=" * 50)

selWiredriver.quit()
print("selenium Wire driver Ended - Now starting Selenium Driver")
# selenium_driver.minimize_window()


# selenium_driver Code Here

selenium_driver.get("https://www.google.com/")
time.sleep(3)

try:
    # SignIn Button click
    signin_btn = selenium_driver.find_element(By.LINK_TEXT, "Sign in")
    signin_btn.click()
    time.sleep(3)
    SignInSelenium()

except Exception as e:
    print("Already SignIn")
    print(e)

selenium_driver.get("https://recorder.google.com/")
time.sleep(15)

main_window_root = selenium_driver.find_element(By.TAG_NAME, "recorder-main").shadow_root
side_bar = main_window_root.find_element(By.CSS_SELECTOR, "recorder-sidebar")

side_bar_root = side_bar.shadow_root

recorder_sidebar_items = side_bar_root.find_element(By.CSS_SELECTOR, "recorder-sidebar-items")
recorder_sidebar_items_root = recorder_sidebar_items.shadow_root


rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

section_scroll = recorder_sidebar_items_root.find_element(By.CSS_SELECTOR, "div.items > ul.library-list")

if rec_items:
    item_1 = rec_items[0]
    item_1.click()

    # Get initial scroll height
    last_height = selenium_driver.execute_script("return arguments[0].scrollHeight", section_scroll)
    

    while True:
        # Scroll down
        # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", section_scroll)
        # time.sleep(3)
        rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

        last_rec_item = rec_items[len(rec_items)-1]

        for i in range(0,8):
         last_rec_item.send_keys(Keys.PAGE_DOWN)
        

        # Wait for new items to load
        time.sleep(5)

        # Get new scroll height
        new_height =  selenium_driver.execute_script("return arguments[0].scrollHeight", section_scroll)
        

        if new_height == last_height:
            break

        last_height = new_height

    print("Scrolled to the bottom")
else:
    print("No items found to click.")

# 

rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

print(f"length of server Audio List : {len(server_audio_list)}")
print("List length returned by the selenium driver ")
print(len(rec_items))

counter = 0  # counter
for item in rec_items:

    # check for Last Scraped Records and If reached then Quit
    first_col_data = None
    with open('LastScrapedRecord.csv', mode='r') as file:
    
        csv_reader = csv.reader(file)
        
        try:
            first_row = next(csv_reader)
            first_col_data = first_row[0]
        except Exception as e:
            first_col_data = ""
        print(f"Last Run Stored Audio Id : {first_col_data} ")

    if server_audio_list[counter]['audioId'] == first_col_data:
        print("Reaced")
        print(server_audio_list[counter]['audioId'])
        with open('LastScrapedRecord.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([server_audio_list[0]['audioId']])

        try:
            print("Bot Closed Data already present")
            selenium_driver.quit()
            break
        except Exception as e:
            selenium_driver.quit()
            print("Bot Closed Data already present")
            break



    print("counter")
    print(counter)

    item.click()
    time.sleep(3)
    


    recorder_sidebar_item_root = item.find_element(By.CSS_SELECTOR, "recorder-sidebar-item").shadow_root
    recorder_metadata_root =  recorder_sidebar_item_root.find_element(By.CSS_SELECTOR, "recorder-metadata").shadow_root
    
    # title
    title = recorder_metadata_root.find_element(By.CSS_SELECTOR, '.title-wrapper .title .rest').text
    print(f"title : {title}")

    # Time
    match = re.search(r'\bat\s(\d{1,2}:\d{2}\s*[ap]m)\b', title, re.IGNORECASE)
    if match:
        audio_time = match.group(1)
    else:
       audio_time  = ""

    duration = recorder_metadata_root.find_element(By.CSS_SELECTOR, "span.duration").text
    print(f"Duration : {duration}")

    date = recorder_metadata_root.find_element(By.CSS_SELECTOR, ".flex-overflow-wrapper span").text
    print(f"Date : {date}")

    location = recorder_metadata_root.find_element(By.CSS_SELECTOR, ".location").text
    print(f"Location : {location}")

    try:
        chip = recorder_metadata_root.find_element(By.CSS_SELECTOR, ".chip").text
        print(f"Chip : {chip}")
    
    except Exception as e:
        chip = ""


    fileName = title.replace(":", "-")
    time.sleep(4)
    
    recorder_content = main_window_root.find_element(By.CSS_SELECTOR, "recorder-content")
    recorder_content_root = recorder_content.shadow_root

    recorder_settings =  recorder_content_root.find_element(By.CSS_SELECTOR, "recorder-settings")
    recorder_settings_root = recorder_settings.shadow_root

    mwc_icon_btn = recorder_settings_root.find_element(By.CSS_SELECTOR, "mwc-icon-button.menu")
    mwc_icon_btn.click() 
    time.sleep(1)
    mwc_icon_btn_root = mwc_icon_btn.shadow_root
    # print(mwc_icon_btn_root)



    button = mwc_icon_btn_root.find_element(By.CSS_SELECTOR, "button.mdc-icon-button")
    # button_root = button.shadow_root
    # button.click()

    mwc_menu = recorder_settings_root.find_element(By.CSS_SELECTOR, 'mwc-menu')
    # print(mwc_menu)

    inner_html = selenium_driver.execute_script("return arguments[0].shadowRoot.innerHTML;", mwc_menu)

    download_btn = mwc_menu.find_element(By.CSS_SELECTOR, "mwc-list-item")
    download_btn.click()
    time.sleep(1)

    recorder_download_modal_root =  main_window_root.find_element(By.CSS_SELECTOR, "recorder-download-modal").shadow_root

    audio_checkBox =  recorder_download_modal_root.find_element(By.CSS_SELECTOR, 'mwc-check-list-item[aria-label="Audio file (.m4a)"]')
    text_checkBox =  recorder_download_modal_root.find_element(By.CSS_SELECTOR, 'mwc-check-list-item[aria-label="Text file (.txt)"]')
    download_btn_main = recorder_download_modal_root.find_element(By.CSS_SELECTOR, "mwc-button.download")
    cancel_btn = recorder_download_modal_root.find_element(By.CSS_SELECTOR, "mwc-button.cancel")

    # download_link = f"https://usercontent.recorder.google.com/download/playback/{server_audio_list[counter]['audioId']}?download=true"
    
    # print(download_link)
    # driver.get(download_link)
    time.sleep(1)


    for i in range(0,2):
        if i == 1:
            mwc_icon_btn.click() 
            time.sleep(1)

            download_btn.click()
            time.sleep(1)

            try:


                audio_checkBox.click()
                time.sleep(1)

                text_checkBox.click()
                time.sleep(1)

                download_btn_main.click()
                time.sleep(1)
                
            except:
                cancel_btn.click()
                continue
                


        if i == 0:
            time.sleep(1)
            try:
                download_waiting_time = parse_duration(duration)
            except:
                download_waiting_time = 8
            print(f"Download waiting time : {download_waiting_time}")
            download_btn_main.click()
            time.sleep(download_waiting_time)

            most_recent_file = None
            most_recent_time = 0
            # iterate over the files in the directory using os.scandir
            for entry in os.scandir(download_dir):
                if entry.is_file():
                    # get the modification time of the file using entry.stat().st_mtime_ns
                    mod_time = entry.stat().st_mtime_ns
                    if mod_time > most_recent_time:
                        # update the most recent file and its modification time
                        most_recent_audiofile = entry.name
                        most_recent_time = mod_time

    print(f"Most Recent Audio File : {most_recent_audiofile}")


    time.sleep(3)
    most_recent_file = None
    most_recent_time = 0

    # iterate over the files in the directory using os.scandir
    for entry in os.scandir(download_dir):
        if entry.is_file():
            # get the modification time of the file using entry.stat().st_mtime_ns
            mod_time = entry.stat().st_mtime_ns
            if mod_time > most_recent_time:
                # update the most recent file and its modification time
                most_recent_transfile = entry.name
                most_recent_time = mod_time

    print(f"Most Recent Transcript File : {most_recent_transfile}")

    csv_data = [{"audioId" : server_audio_list[counter]['audioId'], "fileName Audio" : most_recent_audiofile, "fileName Trans" : most_recent_transfile, "Location" : location, "Duration" : duration, "Title" : title, "Tags" : chip, "Date" : date, "Time" : audio_time, "Latitude" : server_audio_list[counter]['lat'], "Longitude" : server_audio_list[counter]['long']}]
    
    with open(f"{download_dir}/Metadata.csv", 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerows(csv_data)



    counter = counter + 1

     # Updating the LastScrapedRecord.csv file with the AudioId of last in the last(at top)
    if counter == len(server_audio_list):
        with open('LastScrapedRecord.csv', 'w') as csvfile:
            print("Scraped Till the End")
            writer = csv.writer(csvfile)
            writer.writerow([server_audio_list[0]['audioId']])
            break

    



selenium_driver.quit()
