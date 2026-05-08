import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import random
import json

APPIUM_SERVER_URL = "http://127.0.0.1:4723"
DEVICE_NAME = "192.168.20.23"                    # Update with your device name (adb devices)
PLATFORM_VERSION = "11"                    # Update with your Android version
APP_PACKAGE = "st.suite.android.samples.sampleappunified"        # Hotstar Android package name
APP_ACTIVITY = "st.suite.android.samples.sampleappunified.MainActivity"  # Update if different

# Android KeyCodes
KEYCODE_BACK = 4
KEYCODE_DPAD_UP = 19
KEYCODE_DPAD_DOWN = 20
KEYCODE_DPAD_LEFT = 21
KEYCODE_DPAD_RIGHT = 22
KEYCODE_DPAD_CENTER = 23
KEYCODE_ENTER = 66

@pytest.fixture(scope="function")
def driver_setup(request):
    """Initializes and yields Appium driver for Android."""
    print(f"\nSetting up driver for test: {request.node.name}...")
    appium_options = AppiumOptions()
    appium_options.platform_name = "Android"
    appium_options.automation_name = "UiAutomator2"
    appium_options.set_capability("appium:deviceName", DEVICE_NAME)
    appium_options.set_capability("appium:platformVersion", PLATFORM_VERSION)
    appium_options.set_capability("appium:appPackage", APP_PACKAGE)
    appium_options.set_capability("appium:appActivity", APP_ACTIVITY)
    # --- STABILITY FIXES ---
    appium_options.set_capability("appium:noReset", False)
    appium_options.set_capability("appium:fullReset", False)
    # Force a fresh instrumentation start
    appium_options.set_capability("appium:forceAppLaunch", True)
    # Ensure previous session is killed
    appium_options.set_capability("appium:shouldTerminateApp", True)
    # Give the server more time to recover
    appium_options.set_capability("appium:uiautomator2ServerReadTimeout", 45000)
    # --- END FIXES ---

    driver = None
    try:
        driver = webdriver.Remote(APPIUM_SERVER_URL, options=appium_options)
        driver.implicitly_wait(5)

        ignored_exceptions = [StaleElementReferenceException]
        wait_50s = WebDriverWait(driver, 50, ignored_exceptions=ignored_exceptions)
        video_90s = WebDriverWait(driver, 90, ignored_exceptions=ignored_exceptions)

        print("App launched successfully.")
        time.sleep(5)
        yield driver, wait_50s, video_90s

    except Exception as e:
        print(f"Error during driver initialization: {e}")
        pytest.fail(f"Driver setup failed with error: {e}")

    finally:
        if driver:
            print(f"Tearing down driver for: {request.node.name}")
            driver.quit()
            # CRITICAL: Sleep gives the Android OS time to release the instrumentation socket
            time.sleep(5)
#



def _validate_titles(wait):
        home_items = {
            "Movie_1": '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/text" and @text="Caminandes 1: Llama Drama"]',
            "Movie_2": '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/text" and @text="Caminandes 2: Gran Dillama"]',
            "Movie_3": '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/text" and @text="Caminandes 3: Llamigos"]',
            "Movie_4": '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/text" and @text="Sintel"]',
            "Movie_5": '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/text" and @text="Sintel"]',
        }

        for name, xpath in home_items.items():
            time.sleep(1)
            title = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
            assert title is not None, f"{name} title is not available"
            print(f"{name} title is available")


def _validate_movie_card(wait):
    movie_card = {
        "Card_1": '//android.widget.LinearLayout[@resource-id="st.suite.android.samples.sampleappunified:id/content"]/android.widget.LinearLayout[1]',
        "Card_2": '//android.widget.LinearLayout[@resource-id="st.suite.android.samples.sampleappunified:id/content"]/android.widget.LinearLayout[2]',
        "Card_3": '//android.widget.LinearLayout[@resource-id="st.suite.android.samples.sampleappunified:id/content"]/android.widget.LinearLayout[3]',
        "Card_4": '//android.widget.LinearLayout[@resource-id="st.suite.android.samples.sampleappunified:id/content"]/android.widget.LinearLayout[4]',
        "Card_5": '//android.widget.LinearLayout[@resource-id="st.suite.android.samples.sampleappunified:id/content"]/android.widget.LinearLayout[5]',
    }

    for name, xpath in movie_card.items():
        time.sleep(1)
        title = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
        assert title is not None, f"{name} card is not available"
        print(f"{name} card is available")


def validate_movie_cards(driver):
    for i in range(2, 7):  # Loops from instance 2 to 6
        selector = f'new UiSelector().className("android.widget.LinearLayout").instance({i})'

        try:
            # Short wait to keep the test moving quickly
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, selector))
            )

            # Calculate display index: if i is 2, (i - 1) is 1
            card_number = i - 1
            print(f"movie card {card_number} found and validated")

        except Exception:
            print(f"movie card {i - 1} could not be found.")
            break

def test_case_001(driver_setup):
    driver, wait, _ = driver_setup
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="st.suite.android.samples.sampleappunified:id/logo"]')))
    print("logo is visible")
    validate_movie_cards(driver)

def test_case_002(driver_setup):
    driver, wait, _ = driver_setup
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="st.suite.android.samples.sampleappunified:id/logo"]')))
    print("logo is visible")
    driver.press_keycode(KEYCODE_DPAD_CENTER)
    time.sleep(10)
    driver.press_keycode(KEYCODE_BACK)
    validate_movie_cards(driver)


def test_case_003(driver_setup):
    driver, wait, _ = driver_setup
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="st.suite.android.samples.sampleappunified:id/logo"]')))
    print("logo is visible")
    validate_movie_cards(driver)
    driver.press_keycode(KEYCODE_DPAD_CENTER)
    time.sleep(10)
    driver.press_keycode(KEYCODE_DPAD_DOWN)
    driver.press_keycode(KEYCODE_DPAD_RIGHT)
    driver.press_keycode(KEYCODE_DPAD_CENTER)

    element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/current_time"]')))
    text = element.text.strip()

    minutes, seconds = map(int, text.split(":"))
    total_seconds = minutes * 60 + seconds
    print(f"current time: {total_seconds} seconds")
    assert total_seconds > 10, f"Time is not greater than 10 sec, actual: {total_seconds}"


def test_case_004(driver_setup):
    driver, wait, _ = driver_setup
    wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="st.suite.android.samples.sampleappunified:id/logo"]')))
    print("logo is visible")
    validate_movie_cards(driver)
    driver.press_keycode(KEYCODE_DPAD_CENTER)
    time.sleep(15)
    driver.press_keycode(KEYCODE_DPAD_DOWN)
    driver.press_keycode(KEYCODE_DPAD_CENTER)

    element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/current_time"]')))
    time1 = element.text.strip()

    # Wait for 3 seconds
    time.sleep(3)

    # Get time again
    time2 = driver.find_element(
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="st.suite.android.samples.sampleappunified:id/current_time"]'
    ).text.strip()

    # Verify timer paused
    assert time1 == time2, f"Timer is still running: {time1} -> {time2}"

    print(f"Timer is paused: {time1}")