import csv
import os
from selenium import webdriver

user_name = os.getenv("LT_USERNAME");
access_key = os.getenv("LT_ACCESS_KEY")


def write_data_into_csv(browser_name, browser_version, selenium_version, supported_status):
    with open('selenium_data.csv', 'a', newline='') as file:
        field_name = ['browser_name', 'browser_version', 'selenium_version', 'supported_status']
        the_writer = csv.DictWriter(file, fieldnames=field_name)
        the_writer.writerow(
            {'browser_name': browser_name, 'browser_version': browser_version, 'selenium_version': selenium_version,
             'supported_status': supported_status})


def run_test(browser_name, browser_version, selenium_version):
    try:
        desired_caps = {
            'LT:Options': {
                "build": "Selenium_combination_check-1",  # Change your build name here
                "name": browser_name + "-" + browser_version + "-" + selenium_version,  # Change your test name here
                "platformName": "Windows 10",
                "selenium_version": selenium_version,
                "console": 'true',  # Enable or disable console logs
                "network": 'true',  # Enable or disable network logs
            },
            "browserName": browser_name,
            "browserVersion": browser_version,
        }
        driver = webdriver.Remote(
            command_executor="http://{}:{}@hub.lambdatest.com/wd/hub".format(
                user_name, access_key),
            desired_capabilities=desired_caps)
        driver.get("https://www.google.com/")
        print(driver.title)
        write_data_into_csv(browser_name, browser_version, selenium_version, 'Yes')
        driver.quit()
    except:
        print("except")
        write_data_into_csv(browser_name, browser_version, selenium_version, 'No')


def run_all_combination_from_csv():
    with open('Selenium_combinations.csv', 'r') as file:
        data = csv.reader(file)
        next(data)
        for value in data:
            run_test(value[9], value[10], value[3])  # selenium_ver, browser, version


run_all_combination_from_csv()
