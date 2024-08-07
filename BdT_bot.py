import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Define the path to the ChromeDriver executable
driver_path = '/usr/local/bin/chromedriver'
page_url = "https://www.tixforgigs.com/en-GB/Resale/52202/bucht-der-traumer-2024-helenesee-frankfurt-oder"

# Create a Service object for ChromeDriver
service = Service(driver_path)
service.start()

# Initialize Chrome WebDriver using the service
# Options for window size and creating chrome profile
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--user-data-dir=/Users/brichard/Library/Application Support/Google/Chrome/Default/')
driver = webdriver.Chrome(service=service, options=options)


def open_page(url):
    driver.get(url)
    time.sleep(1)
    # Accept cookies
    try:
        driver.find_element(By.XPATH, "//*[@id='klaro-cookie-notice']/div/div/div/button").click()
    except:
        pass

from selenium.webdriver.common.by import By
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
        # Locate all cards with the headline "Festivalticket"
        ticket_cards = driver.find_elements(By.XPATH, f"//div[contains(@class, 'gc c8r8 fxc')]//div[contains(@class, 'headline') and text()='{wanted_item}']")
        print(f"Found {len(ticket_cards)} {wanted_item} buttons.")
        
        for card in ticket_cards:
            # Find the parent element of the headline to locate the entire card
            parent_card = card.find_element(By.XPATH, "./ancestor::div[contains(@class, 'gc c8r8 fxc')]")
            
            try:
                # Locate the clickable part inside the card
                clickable_part = parent_card.find_element(By.XPATH, ".//span[contains(@data-bind, 'click:$root.addTicketResaleToCart')]")
                # Click the clickable part
                clickable_part.click()
                print("Clicked on a Festivalticket button.")
                return True
            except:
                print("Ticket Already Reserved !")
        print("No Festivalticket button found. Retrying in 30 seconds.")
        return False
            
    except Exception as e:
        print(f"Error clicking Festivalticket button: {e}")

def exit():
    # HUGE SUCCESS MESASAGE THAT I CAN SEE IN THE CONSOLE
    print("========================================")
    print("========================================")
    print("TICKET RESERVED !")
    print("========================================")
    while True:
        time.sleep(1)
    

wanted_items = ['Festivalticket', 'Förderticket']
not_wanted_items = ['Parkticket', 'Caravan Ticket', 'Sunday Ticket']

def reload_and_check(success):
    time.sleep(30)
    if success:
        exit()
    open_page(page_url)
    click_unwanted_filters(not_wanted_items)
    reload_and_check(click_festivalticket_button(wanted_items[0]) or click_festivalticket_button(wanted_items[1]))
    
reload_and_check(False)