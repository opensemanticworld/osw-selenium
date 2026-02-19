"""OSW Selenium — reusable UI testing library for OpenSemanticLab."""

from osw_selenium.config import OSWConfig
from osw_selenium.driver import create_driver
from osw_selenium.pages.base import BasePage
from osw_selenium.pages.json_editor import JsonEditorPage
from osw_selenium.pages.login import LoginPage

__all__ = [
    "BasePage",
    "JsonEditorPage",
    "LoginPage",
    "OSWConfig",
    "create_driver",
]
