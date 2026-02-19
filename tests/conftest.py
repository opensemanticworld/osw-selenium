"""Shared pytest fixtures for OSW Selenium tests."""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.json_editor import JsonEditorPage
from osw_selenium.pages.login import LoginPage


@pytest.fixture(scope="session")
def osw_config() -> OSWConfig:
    """Session-scoped OSW configuration loaded from environment variables."""
    return OSWConfig.from_env()


@pytest.fixture(scope="session")
def driver(osw_config: OSWConfig) -> Generator[WebDriver, None, None]:
    """Session-scoped WebDriver instance.

    Shared across all tests to avoid repeated browser startup.
    Quits the browser after all tests complete.
    """
    drv = create_driver(osw_config)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def logged_in_driver(driver: WebDriver, osw_config: OSWConfig) -> WebDriver:
    """Session-scoped driver that has already logged in as Admin.

    Login happens once; cookies persist across all tests in the session.
    """
    login_page = LoginPage(driver, osw_config)
    login_page.login()
    return driver


@pytest.fixture()
def login_page(driver: WebDriver, osw_config: OSWConfig) -> LoginPage:
    """Function-scoped LoginPage instance."""
    return LoginPage(driver, osw_config)


@pytest.fixture()
def json_editor(logged_in_driver: WebDriver, osw_config: OSWConfig) -> JsonEditorPage:
    """Function-scoped JsonEditorPage that assumes the driver is already logged in."""
    return JsonEditorPage(logged_in_driver, osw_config)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Auto-skip integration tests when MW_SITE_SERVER is not set."""
    if os.environ.get("MW_SITE_SERVER"):
        return
    skip_marker = pytest.mark.skip(reason="MW_SITE_SERVER not set — skipping integration test")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_marker)
