import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeDriverService
from notify_run import Notify
from selenium.webdriver.common.by import By

def open_page(url):
    driver.get(url)
    time.sleep(1)
    # Accept cookies
    try:
        driver.find_element(By.XPATH, "//*[@id='klaro-cookie-notice']/div/div/div/button").click()
    except:
        pass

def click_filter(filter_name):
    try:
        filter_button = driver.find_elements(By.XPATH, f"//span[text()='{filter_name}']")
        if filter_button:
            filter_button[0].click()
    except Exception as e:
        print(f"Error clicking filter {filter_name}: {e}")

def click_unwanted_filters(not_wanted_items):
    for filter_name in not_wanted_items:
        click_filter(filter_name)

def click_festivalticket_button(wanted_item):
    try:
        ticket_cards = driver.find_elements(By.XPATH, f"//div[contains(@class, 'gc c8r8 fxc')]//div[contains(@class, 'headline') and text()='{wanted_item}']")
        print(f"Found {len(ticket_cards)} {wanted_item} buttons.")
        
        for card in ticket_cards:
            parent_card = card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'gc c8r8 fxc')]")
            
            try:
                clickable_part = parent_card.find_element(By.XPATH, ".//span[contains(@data-bind, 'click:$root.addTicketResaleToCart')]")
                clickable_part.click()
                print("Clicked on a Festivalticket button.")
                return True
            except:
                print("Ticket Already Reserved !")
        return False
            
    except Exception as e:
        print(f"Error clicking Festivalticket button: {e}")

def notifyAndWait():
    notify()
    # Looping to keep the browser open and allow user to checkout
    while True:
        time.sleep(1)
       
       
def initNotify():
    notify = Notify()
    msg = notify.register()
    print(msg)
    while True:
        user_input = input("Scan QR code to subscribe to notification then type 'yes': ")
        if user_input.lower() == 'yes':
            print("Launching chrome ...")
            break
 
def notify():
    try:
        notify.send('OUE OUE OUE')
    except:
        print("ERROR - Could not send notification.")
    # HUGE SUCCESS MESSAGE THAT I CAN SEE IN THE CONSOLE
    print("========================================")
    print("========================================")
    print("TICKET RESERVED !")
    print("========================================")

def reload_and_check():
    open_page(page_url)
    click_unwanted_filters(not_wanted_items)
    success = click_festivalticket_button(wanted_items[0]) or click_festivalticket_button(wanted_items[1])
    if success:
        notifyAndWait()
    else:
        time.sleep(timeout)
        print(f"No Festivalticket button found. Retrying in {timeout} seconds.")
        reload_and_check()

# VARIABLES
driver_path = '/usr/local/bin/chromedriver'
page_url = "https://www.tixforgigs.com/en-GB/Resale/52202/bucht-der-traumer-2024-helenesee-frankfurt-oder"
timeout = 15
wanted_items = ['Festivalticket', 'Förderticket']
not_wanted_items = ['Parkticket', 'Caravan Ticket', 'Sunday Ticket']

# MAIN
if __name__ == "__main__":
    initNotify()
    
    # initChromeDriver
    service = ChromeDriverService(driver_path)
    service.start()

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--user-data-dir=/Users/brichard/Library/Application Support/Google/Chrome/Default/')
    driver = webdriver.Chrome(service=service, options=options)

    reload_and_check()