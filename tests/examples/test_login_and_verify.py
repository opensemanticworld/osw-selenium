"""Tests for examples/login_and_verify.py — verify login flow works against a live OSL instance."""

from __future__ import annotations

import pytest

from osw_selenium.pages.login import LoginPage

pytestmark = pytest.mark.integration


def test_login_page_class_has_expected_locators():
    """LoginPage exposes the expected locator constants (offline check)."""
    assert LoginPage.URL_PATH == "/wiki/Special:UserLogin"
    assert LoginPage.USERNAME_FIELD[1] == "wpName1"
    assert LoginPage.PASSWORD_FIELD[1] == "wpPassword1"
    assert LoginPage.REMEMBER_ME[1] == "wpRemember"
    assert LoginPage.LOGIN_BUTTON[1] == "wpLoginAttempt"


def test_login_and_verify_main_page(logged_in_driver, osw_config):
    """After login the main page should be accessible and contain 'Main Page'."""
    logged_in_driver.get(osw_config.base_url.rstrip("/") + "/wiki/Main_Page")
    assert "Main Page" in logged_in_driver.page_source
