from seleniumwire import webdriver  # Import seleniumwire
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
import csv
import io
import gzip

download_dir = "/Users/mian/ScrapedData/Google Rec/Scraped_Data"

columns = ["audioId", "fileName Audio", "fileName Trans", "Location", "Duration", "Title", "Tags", "Date", "Latitude", "Longitude"]
with open(f'{download_dir}/Metadata.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    print("CSV file created successfully.")

# Initialize Chrome options
options = Options()

# Set download directory preferences
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "savefile.default_directory": download_dir,
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Other potential optimizations
# options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_argument('--disable-infobars')  # Disable infobars
options.add_argument('--disable-extensions')  # Disable extensions
options.add_argument('--disable-popup-blocking')  # Disable popup blocking
options.add_argument('--disable-translate')  # Disable translation prompt

# Configure selenium-wire
seleniumwire_options = {
    'disable_encoding': True , # Disable automatic encoding
    'disable_capture' : True
    # Add any other specific options you might need
}

# Initialize webdriver with selenium-wire and chrome options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=options,
    seleniumwire_options=seleniumwire_options
)

# Example of limiting request capture
driver.scopes = [
    '.*pixelrecorder-pa.clients6.google.com.*'  # Only capture requests to the specific URL
]

def SignIn():
    
    # email input
    email_input = driver.find_element(By.TAG_NAME, "input")
    email_input.send_keys("rita@mosaicdesignlabs.com")
    time.sleep(2)

    next_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    next_btn.click()
    time.sleep(4)

    # password input
    password_input = driver.find_element(By.NAME, "Passwd")
    password_input.send_keys("mosaictest123")
    time.sleep(2)

    next_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    next_btn.click()
    time.sleep(4)
    return


driver.get("https://www.google.com/")
time.sleep(3)

try:
    # SignIn Button click
    signin_btn = driver.find_element(By.LINK_TEXT, "Sign in")
    signin_btn.click()
    time.sleep(3)
    SignIn()

except Exception as e:
    print("Already SignIn")
    print(e)

driver.get("https://recorder.google.com/")
time.sleep(15)

main_window_root = driver.find_element(By.TAG_NAME, "recorder-main").shadow_root
side_bar = main_window_root.find_element(By.CSS_SELECTOR, "recorder-sidebar")

side_bar_root = side_bar.shadow_root

recorder_sidebar_items = side_bar_root.find_element(By.CSS_SELECTOR, "recorder-sidebar-items")
recorder_sidebar_items_root = recorder_sidebar_items.shadow_root


rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

section_scroll = recorder_sidebar_items_root.find_element(By.CSS_SELECTOR, "div.items > ul")

item_1 = rec_items[0]
item_1.click()

# Get scroll height
last_height = driver.execute_script("return arguments[0].scrollHeight", section_scroll)

while True:
    # Scroll down
    item_1.send_keys(Keys.PAGE_DOWN)
    item_1.send_keys(Keys.PAGE_DOWN)
    item_1.send_keys(Keys.PAGE_DOWN)
    
    # Wait for new audios to load
    time.sleep(1)
    
    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight", section_scroll)
    if new_height == last_height:
        break
    last_height = new_height

print("scrolled")

server_audio_list = []

# Tracing requests
for request in driver.requests:
    if "https://pixelrecorder-pa.clients6.google.com/$rpc/java.com.google.wireless.android.pixel.recorder.protos.PlaybackService/GetRecordingList" in request.url:
        # print("Request URL:", request.url)
        # print("Request Method:", request.method)
        # print("Request Headers:", request.headers)
        print("Request Response Body:")

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
                    print(server_audio_list)
                    print(f"len : {len(server_audio_list)}")

               
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Response Body:", content.decode('utf-8'))  
        except Exception as ex:
            print("Error processing response:", ex)

        print("=" * 50)


rec_items = recorder_sidebar_items_root.find_elements(By.CSS_SELECTOR, "div.items > ul > div.item")

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
        print(f"Last Stored Audio Id : {first_col_data} ")

    if server_audio_list[counter]['audioId'] == first_col_data:
        print("Reaced")
        print(server_audio_list[counter]['audioId'])
        with open('LastScrapedRecord.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([server_audio_list[0]['audioId']])

        try:
            print("Bot Closed Data already present")
            driver.close()
        except Exception as e:
            print("Bot Closed Data already present")

    # Updating the LastScrapedRecord.csv file with the AudioId of last in the last(at top)
    if counter == len(server_audio_list) - 1:
        with open('LastScrapedRecord.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([server_audio_list[0]['audioId']])

    print("counter")
    print(counter)

    item.click()
    time.sleep(2)
    recorder_sidebar_item_root = item.find_element(By.CSS_SELECTOR, "recorder-sidebar-item").shadow_root
    recorder_metadata_root =  recorder_sidebar_item_root.find_element(By.CSS_SELECTOR, "recorder-metadata").shadow_root
    
    # title
    title = recorder_metadata_root.find_element(By.CSS_SELECTOR, '.title-wrapper .title .rest').text
    print(f"title : {title}")

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
        print("not Favouited")

    fileName = title.replace(":", "-")



    csv_data = [{"audioId" : server_audio_list[counter]['audioId'], "fileName Audio" : fileName, "fileName Trans" : fileName, "Location" : location, "Duration" : duration, "Title" : title, "Tags" : chip, "Date" : date, "Latitude" : server_audio_list[counter]['lat'], "Longitude" : server_audio_list[counter]['long']}]
    
    with open(f"{download_dir}/Metadata.csv", 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerows(csv_data)

    time.sleep(2)
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

    inner_html = driver.execute_script("return arguments[0].shadowRoot.innerHTML;", mwc_menu)

    download_btn = mwc_menu.find_element(By.CSS_SELECTOR, "mwc-list-item")
    download_btn.click()
    time.sleep(1)

    recorder_download_modal_root =  main_window_root.find_element(By.CSS_SELECTOR, "recorder-download-modal").shadow_root

    audio_checkBox =  recorder_download_modal_root.find_element(By.CSS_SELECTOR, 'mwc-check-list-item[aria-label="Audio file (.m4a)"]')
    text_checkBox =  recorder_download_modal_root.find_element(By.CSS_SELECTOR, 'mwc-check-list-item[aria-label="Text file (.txt)"]')
    download_btn_main = recorder_download_modal_root.find_element(By.CSS_SELECTOR, "mwc-button.download")

    # download_link = f"https://usercontent.recorder.google.com/download/playback/{server_audio_list[counter]['audioId']}?download=true"
    counter = counter + 1
    # print(download_link)
    # driver.get(download_link)
    time.sleep(1)
    print("audi fine donaloaded")

    for i in range(0,2):
        if i == 1:
            mwc_icon_btn.click() 
            time.sleep(1)

            download_btn.click()
            time.sleep(1)

            audio_checkBox.click()
            time.sleep(1)

            text_checkBox.click()
            time.sleep(1)

        
        time.sleep(1)
        download_btn_main.click()
        time.sleep(1)

    # time.sleep(5)

print(len(rec_items))

# inner_html = driver.execute_script("return arguments[0].outerHTML;", rec_items)
# print("printing")
# print(inner_html)
# print(html)
# print(Main_window.text)




time.sleep(100000)



# Perform your tasks...

# Close the browser
driver.quit()
