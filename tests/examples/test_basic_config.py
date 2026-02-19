"""Tests for examples/basic_config.py — verify config creation patterns work."""

from __future__ import annotations

from osw_selenium.config import OSWConfig


def test_config_from_env_returns_instance():
    """OSWConfig.from_env() returns a valid config object."""
    config = OSWConfig.from_env()
    assert isinstance(config, OSWConfig)
    assert isinstance(config.base_url, str)
    assert isinstance(config.browser, str)
    assert isinstance(config.headless, bool)


def test_config_with_explicit_overrides():
    """OSWConfig accepts explicit keyword overrides."""
    config = OSWConfig(
        base_url="https://my-osw-instance.example.com",
        admin_password="my-secret",
        browser="firefox",
        headless=True,
    )
    assert config.base_url == "https://my-osw-instance.example.com"
    assert config.admin_password == "my-secret"
    assert config.browser == "firefox"
    assert config.headless is True


def test_config_defaults():
    """OSWConfig has sensible defaults for optional fields."""
    config = OSWConfig(base_url="http://localhost", admin_password="pass")
    assert config.admin_username == "Admin"
    assert config.implicit_wait == 10
    assert config.window_width == 1280
    assert config.window_height == 1024
    assert config.accept_insecure_certs is True
