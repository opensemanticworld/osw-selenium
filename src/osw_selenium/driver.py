"""WebDriver factory for creating Chrome or Firefox instances."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from osw_selenium.config import OSWConfig


def create_driver(config: OSWConfig) -> webdriver.Chrome | webdriver.Firefox:
    """Create a Selenium WebDriver instance from the given config.

    Selenium 4.6+ handles driver binary download automatically via selenium-manager.
    No webdriver-manager or Docker is needed.

    Args:
        config: The OSW test configuration.

    Returns:
        A configured Chrome or Firefox WebDriver instance.

    Raises:
        ValueError: If browser name is not "chrome" or "firefox".
    """
    if config.browser == "chrome":
        options = ChromeOptions()
        if config.headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={config.window_width},{config.window_height}")
        options.accept_insecure_certs = config.accept_insecure_certs
        driver = webdriver.Chrome(options=options)
    elif config.browser == "firefox":
        options = FirefoxOptions()
        if config.headless:
            options.add_argument("--headless")
        options.accept_insecure_certs = config.accept_insecure_certs
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(config.window_width, config.window_height)
    else:
        msg = f"Unsupported browser: {config.browser!r}. Use 'chrome' or 'firefox'."
        raise ValueError(msg)

    driver.implicitly_wait(config.implicit_wait)
    return driver
