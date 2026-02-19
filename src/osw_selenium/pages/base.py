"""Base page object with shared browser interaction methods."""

from __future__ import annotations

import contextlib
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from osw_selenium.config import OSWConfig

_ENABLE_CURSOR_JS = """
(function() {
    if (document.getElementById('selenium_mouse_follower')) return;
    var img = document.createElement('img');
    img.setAttribute('src', 'data:image/png;base64,'
        + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAA'
        + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH8W+XmYwkS2I0'
        + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxLixYZb5KAAZZhbunu7O/PKf'
        + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsuGYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
        + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZdoLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
        + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9vlkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
        + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJLN0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
        + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsXtOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
        + 'dAAAAABJRU5ErkJggg==');
    img.setAttribute('id', 'selenium_mouse_follower');
    img.setAttribute('style',
        'position: absolute; z-index: 99999999999; pointer-events: none; left:0; top:0; width: 50px; height: auto');
    document.body.appendChild(img);
    document.onmousemove = function(e) {
        document.getElementById('selenium_mouse_follower').style.left = e.pageX + 'px';
        document.getElementById('selenium_mouse_follower').style.top = e.pageY + 'px';
    };
})();
"""

_NOTIFICATION_JS_TEMPLATE = """
(function() {{
    var div = document.getElementById('osw-selenium-toast');
    if (!div) {{
        div = document.createElement('div');
        div.id = 'osw-selenium-toast';
        div.style.cssText = 'visibility:visible; min-width:300px; background-color:#333; color:#fff; '
            + 'text-align:center; border-radius:2px; padding:8px; position:fixed; z-index:1000; '
            + 'left:50%; bottom:15px; margin-left:-150px;';
        document.body.appendChild(div);
    }}
    div.style.visibility = 'visible';
    div.textContent = '{text}';
    setTimeout(function() {{ div.style.visibility = 'hidden'; }}, {timeout});
}})();
"""

_IS_IN_VIEWPORT_JS = """
(function() {
    var el = arguments[0];
    var rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
})();
"""


class BasePage:
    """Base page object with shared browser interaction methods.

    Args:
        driver: The Selenium WebDriver instance.
        config: The OSW test configuration.
        default_timeout: Default explicit wait timeout in seconds.
    """

    def __init__(self, driver: WebDriver, config: OSWConfig, default_timeout: int = 10) -> None:
        self.driver = driver
        self.config = config
        self.timeout = default_timeout
        self._wait = WebDriverWait(driver, default_timeout)

    # --- Navigation ---

    def navigate_to(self, path: str) -> None:
        """Navigate to a path relative to the base URL.

        Args:
            path: URL path starting with ``/`` (e.g. ``/wiki/Main_Page``).
        """
        url = self.config.base_url.rstrip("/") + path
        self.driver.get(url)

    # --- Waiting ---

    def wait_for_element(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """Wait for an element to be present in the DOM.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
            timeout: Override timeout in seconds.

        Returns:
            The located WebElement.
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """Wait for an element to be visible.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
            timeout: Override timeout in seconds.

        Returns:
            The visible WebElement.
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_invisible(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement | bool:
        """Wait for an element to become invisible or absent.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
            timeout: Override timeout in seconds.

        Returns:
            True once the element is no longer visible.
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_clickable(self, locator: tuple[str, str], timeout: int | None = None) -> WebElement:
        """Wait for an element to be clickable.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
            timeout: Override timeout in seconds.

        Returns:
            The clickable WebElement.
        """
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    # --- Element queries ---

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """Find a single element.

        Args:
            locator: A ``(By.XXX, value)`` tuple.

        Returns:
            The located WebElement.
        """
        return self.driver.find_element(*locator)

    def find_elements(self, locator: tuple[str, str]) -> list[WebElement]:
        """Find all matching elements.

        Args:
            locator: A ``(By.XXX, value)`` tuple.

        Returns:
            List of matching WebElements.
        """
        return self.driver.find_elements(*locator)

    def count_visible_elements(self, css_selector: str) -> int:
        """Count visible elements matching a CSS selector.

        Args:
            css_selector: A CSS selector string.

        Returns:
            Number of displayed elements matching the selector.
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        return sum(1 for el in elements if el.is_displayed())

    # --- Interaction ---

    def click(self, locator: tuple[str, str]) -> None:
        """Click an element.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
        """
        self.wait_for_clickable(locator).click()

    def fill_field(self, locator: tuple[str, str], value: str) -> None:
        """Clear and fill a text field.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
            value: The text to enter.
        """
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(value)

    def check_option(self, locator: tuple[str, str]) -> None:
        """Check a checkbox if not already checked.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
        """
        element = self.wait_for_clickable(locator)
        if not element.is_selected():
            element.click()

    # --- Scroll + interaction combos ---

    def is_element_in_viewport(self, element: WebElement) -> bool:
        """Check if an element is within the visible viewport.

        Args:
            element: The WebElement to check.

        Returns:
            True if the element is fully visible in the viewport.
        """
        return bool(self.driver.execute_script(_IS_IN_VIEWPORT_JS, element))

    def scroll_into_view(self, element: WebElement) -> None:
        """Scroll an element into the viewport.

        Args:
            element: The WebElement to scroll to.
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def move_to_element(self, element: WebElement) -> None:
        """Move the cursor to an element.

        Args:
            element: The WebElement to move to.
        """
        ActionChains(self.driver).move_to_element(element).perform()

    def scroll_and_move(self, locator: tuple[str, str]) -> WebElement:
        """Scroll to and move the cursor to an element.

        Args:
            locator: A ``(By.XXX, value)`` tuple.

        Returns:
            The target WebElement.
        """
        element = self.wait_for_element(locator)
        if not self.is_element_in_viewport(element):
            self.scroll_into_view(element)
        self.move_to_element(element)
        return element

    def scroll_and_click(self, locator: tuple[str, str]) -> None:
        """Scroll to an element and click it.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
        """
        element = self.scroll_and_move(locator)
        element.click()

    def scroll_and_fill(self, locator: tuple[str, str], value: str) -> None:
        """Scroll to a field and fill it.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
            value: The text to enter.
        """
        element = self.scroll_and_move(locator)
        element.clear()
        element.send_keys(value)

    def scroll_and_check(self, locator: tuple[str, str]) -> None:
        """Scroll to a checkbox and check it.

        Args:
            locator: A ``(By.XXX, value)`` tuple.
        """
        element = self.scroll_and_move(locator)
        if not element.is_selected():
            element.click()

    # --- JavaScript execution ---

    def execute_js(self, script: str, *args: object) -> object:
        """Execute a JavaScript snippet.

        Args:
            script: The JavaScript code to execute.
            *args: Arguments passed to the script.

        Returns:
            The script's return value.
        """
        return self.driver.execute_script(script, *args)

    def enable_cursor(self) -> None:
        """Inject a visible mouse cursor overlay for video recordings."""
        self.driver.execute_script(_ENABLE_CURSOR_JS)

    def add_notification(self, text: str, timeout_ms: int = 3000) -> None:
        """Show a toast notification on the page.

        Args:
            text: The notification message.
            timeout_ms: Auto-hide delay in milliseconds.
        """
        # Escape single quotes and backslashes for JS string
        safe_text = text.replace("\\", "\\\\").replace("'", "\\'")
        self.driver.execute_script(_NOTIFICATION_JS_TEMPLATE.format(text=safe_text, timeout=timeout_ms))

    def dismiss_notifications(self) -> None:
        """Click away any visible MediaWiki notifications."""
        for selector in (".mw-notification-title", ".mw-notification-content"):
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                if el.is_displayed():
                    with contextlib.suppress(Exception):
                        el.click()

    def wait(self, seconds: float) -> None:
        """Explicit sleep — use sparingly, prefer explicit waits.

        Args:
            seconds: Number of seconds to sleep.
        """
        time.sleep(seconds)
