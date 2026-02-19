"""Page object for the MediaWiki login page."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from osw_selenium.pages.base import BasePage


class LoginPage(BasePage):
    """Page object for the MediaWiki login page.

    Encapsulates both standard login and hidden-form OIDC login flows.
    """

    URL_PATH = "/wiki/Special:UserLogin"

    USERNAME_FIELD = (By.ID, "wpName1")
    PASSWORD_FIELD = (By.ID, "wpPassword1")
    REMEMBER_ME = (By.ID, "wpRemember")
    LOGIN_BUTTON = (By.ID, "wpLoginAttempt")

    def login(self, username: str | None = None, password: str | None = None) -> None:
        """Log in via the standard login form.

        Args:
            username: Override username (defaults to config.admin_username).
            password: Override password (defaults to config.admin_password).
        """
        username = username or self.config.admin_username
        password = password or self.config.admin_password

        self.navigate_to(self.URL_PATH)
        self.enable_cursor()
        self.scroll_and_fill(self.USERNAME_FIELD, username)
        self.scroll_and_fill(self.PASSWORD_FIELD, password)
        self.scroll_and_check(self.REMEMBER_ME)
        self.scroll_and_click(self.LOGIN_BUTTON)

    def login_hidden(self, username: str | None = None, password: str | None = None) -> None:
        """Log in via hidden form (OIDC setups where local login is hidden).

        Uses JavaScript to force form elements visible before filling them.

        Args:
            username: Override username (defaults to config.admin_username).
            password: Override password (defaults to config.admin_password).
        """
        username = username or self.config.admin_username
        password = password or self.config.admin_password

        self.navigate_to(self.URL_PATH)

        # Force hidden form elements visible
        for element_id in ("wpName1", "wpPassword1", "wpRemember", "wpLoginAttempt"):
            self.execute_js(f"document.querySelector('#{element_id}').style.display = 'block'")

        self.fill_field(self.USERNAME_FIELD, username)
        self.fill_field(self.PASSWORD_FIELD, password)
        self.check_option(self.REMEMBER_ME)
        self.click(self.LOGIN_BUTTON)
