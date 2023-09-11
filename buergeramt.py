import subprocess
import importlib
import os
import sys

# Check if pyttsx3 is already installed
try:
    importlib.import_module("pyttsx3")
    print("pyttsx3 is already installed.")
except ImportError:
    print("pyttsx3 is not installed. Installing it now...")

    # Use pip to install pyttsx3
    try:
        subprocess.check_call(["pip", "install", "pyttsx3"])
        print("pyttsx3 has been successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing pyttsx3: {e}")
    except Exception as ex:
        print(f"An error occurred during installation: {ex}")

# Check if libespeak1 is already installed
try:
    subprocess.check_call(["espeak", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("libespeak1 is already installed.")
except (subprocess.CalledProcessError, FileNotFoundError) as e:
    print("libespeak1 is not installed. Installing it now...")

    # Use the appropriate package manager for your Linux distribution to install libespeak1
    # Replace the package manager command below based on your distribution

    # For Ubuntu/Debian
    try:
        subprocess.check_call(["sudo", "apt-get", "install", "libespeak1"])
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error installing libespeak1: {e}")

    print("libespeak1 has been successfully installed.")



# Define the package name to upgrade
package_name = "selenium"

# Run the pip command to upgrade the package
try:
    with open(os.devnull, 'w') as null:
        subprocess.check_call(["pip", "install", "--upgrade", package_name], stdout=null, stderr=null)
    print(f"Successfully upgraded {package_name}.")
except subprocess.CalledProcessError as e:
    # print(f"Error upgrading {package_name}: {e}")
    print(f"Error upgrading {package_name}")
except Exception as ex:
    # print(f"An error occurred: {ex}")
    print(f"An error occurred")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyttsx3


# Initialize the text-to-speech engine
engine = pyttsx3.init()

url = "https://service.berlin.de/terminvereinbarung/termin/restart/?providerList=122208%2C122210%2C122217%2C122219%2C122226%2C122227%2C122231%2C122238%2C122243%2C122246%2C122251%2C122252%2C122254%2C122257%2C122260%2C122262%2C122267%2C122271%2C122273%2C122274%2C122276%2C122277%2C122280%2C122282%2C122284%2C122285%2C122286%2C122291%2C122294%2C122296%2C122297%2C122301%2C122304%2C122309%2C122311%2C122312%2C122314%2C150230%2C331011%2C349977&requestList=331533&source=dldb"


# Set the GeckoDriver executable path using the PATH environment variable
geckodriver_path = "./geckodriver-v0.33.0-linux64/geckodriver"
os.environ["PATH"] += os.pathsep + os.path.dirname(geckodriver_path)



# Define a function to check if the browser tab is open
def is_browser_tab_open(driver):
    try:
        # Get the handles of all open tabs
        all_handles = driver.window_handles

        # Loop through all the handles and check each tab's status
        for handle in all_handles:
            driver.switch_to.window(handle)
            date_elements = driver.find_elements(By.XPATH, "//td[contains(@class, 'buchbar')]/a")
            # If date_elements are found, the tab is considered open
            if date_elements:
                return True

        # If no open tabs are found, return False
        return False
    except Exception:
        # If any exception occurs, the tab is considered closed
        return False


def print_progress_bar(iteration, total, bar_length=50):
    progress = iteration / total
    arrow = '=' * int(round(bar_length * progress))
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\r[{arrow}{spaces}] {int(progress * 100)}%')
    sys.stdout.flush()

def wait_with_progress_bar(backoff):
    for i in range(backoff + 1):
        print_progress_bar(i, backoff)
        time.sleep(1)  # Sleep for 1 second
    print()  # Print a newline to clear the progress bar

"""
The HTML contains content of the following form:
```
                    <td tabindex="0" class="nichtbuchbar" aria-label="07.11.2023 - An diesem Tag sind keine Termine mehr verfügbar" title="07.11.2023 - An diesem Tag sind keine Termine mehr verfügbar">07</td>
                        <td class="buchbar"><a tabindex="0" aria-label="08.11.2023 - An diesem Tag einen Termin buchen" title="08.11.2023 - An diesem Tag einen Termin buchen" href="https://service.berlin.de/terminvereinbarung/termin/time/1699398000/">08</a></td>
                    <td tabindex="0" class="nichtbuchbar" aria-label="09.11.2023 - An diesem Tag sind keine Termine mehr verfügbar" title="09.11.2023 - An diesem Tag sind keine Termine mehr verfügbar">09</td>
```
"""
def get_available_dates():
    # Check for error 429 in the HTML title
    if "Service-Portal Berlin - (null) - 429" in driver.page_source:
        return "TooManyRequests429"

    # Check if the HTML contains the message indicating no available dates
    if "Es sind aktuell keine Termine für ihre Auswahl verfügbar" in driver.page_source or \
       "Entschuldigung, es sind aktuell keine Termine für ihre Auswahl verfügbar" in driver.page_source:
        return []
    else:
        try:
            # Find all the elements that contain date information
            date_elements = driver.find_elements(By.XPATH, "//td[contains(@class, 'buchbar')]/a")

            # Initialize an empty list to store the dates
            available_dates = []

            # Iterate through the elements and extract the dates
            for date_element in date_elements:
                date_text = date_element.get_attribute("aria-label").strip()
                available_dates.append(date_text)

            return available_dates
        except AttributeError as e:
            print("An error occurred while retrieving available dates.")
            print("Perhaps there are no available dates?")
            print("Error: ", e)


backoff, attempt = 30, 0


def parse_availability():
    global backoff, attempt

    # Open the URL
    driver.get(url)

    # Get the HTML content of the page
    page_html = driver.page_source

    # Call the function to parse and extract available dates from the HTML
    # get_available_dates(page_html)
    print("available dates: ", get_available_dates(), ", backoff: ", backoff, ", attempt: ", attempt)

    available_dates = get_available_dates()

    if available_dates == "TooManyRequests429":
        # Convert the text to speech
        engine.say("Too many requests! Let's be good citizens...")
        backoff *= 2

        # Wait for the speech to finish
        engine.runAndWait()

    elif available_dates == None:
        # Convert the text to speech
        engine.say("Wow something is seriously wrong here! Come check it out... Attempt: " + str(attempt))

        # Wait for the speech to finish
        engine.runAndWait()

        while is_browser_tab_open(driver):
            pass

    elif len(get_available_dates()) > 0:
        # Convert the text to speech
        engine.say("There are available dates! Attempt: " + str(attempt))

        # Wait for the speech to finish
        engine.runAndWait()

        while is_browser_tab_open(driver):
            pass

    wait_with_progress_bar(backoff)
    backoff -= 1
    attempt += 1

    # This is what the call on a date looks like
    # https://service.berlin.de/terminvereinbarung/termin/time/1699225200/


try:
    # Create a browser instance using Firefox
    driver = webdriver.Firefox()

    while True:

        try:
            parse_availability()

        except Exception as e:
            print("Error: ", e)
            engine.say("This error might be of interest to you! Come check it out... Attempt: " + str(attempt))
            print("Retrying...")

            # Close the browser tab
            driver.quit()
            # Create a browser instance using Firefox
            driver = webdriver.Firefox()


finally:
    # Close the browser tab
    driver.quit()
