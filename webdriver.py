from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    desired_capabilities = {'goog:loggingPrefs': {'performance': 'ALL', 'browser': 'ALL'}}
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              chrome_options=options, desired_capabilities=desired_capabilities)
    return driver