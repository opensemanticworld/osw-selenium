"""Example: Log in to an OSL instance and verify the main page loads.

Requires MW_SITE_SERVER and MW_ADMIN_PASS environment variables.
"""

from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.login import LoginPage

config = OSWConfig.from_env()
driver = create_driver(config)

try:
    # Log in as admin
    login_page = LoginPage(driver, config)
    login_page.login()

    # Navigate to main page and verify
    driver.get(config.base_url.rstrip("/") + "/wiki/Main_Page")
    if "Main Page" not in driver.page_source:
        print("ERROR: Main Page not found in page source.")
    else:
        print("Login successful — Main Page loaded.")
finally:
    driver.quit()
