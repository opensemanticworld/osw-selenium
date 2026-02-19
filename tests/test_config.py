"""Unit tests for OSWConfig — no browser or OSW instance needed."""

from __future__ import annotations

from osw_selenium.config import OSWConfig


def test_config_defaults():
    config = OSWConfig(base_url="http://example.com", admin_password="pass")
    assert config.base_url == "http://example.com"
    assert config.admin_password == "pass"
    assert config.admin_username == "Admin"
    assert config.browser == "chrome"
    assert config.headless is False
    assert config.implicit_wait == 10
    assert config.window_width == 1280
    assert config.window_height == 1024
    assert config.accept_insecure_certs is True


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("MW_SITE_SERVER", "https://test.example.com")
    monkeypatch.setenv("MW_ADMIN_PASS", "secret123")
    monkeypatch.setenv("OSW_BROWSER", "firefox")
    monkeypatch.setenv("OSW_HEADLESS", "true")
    config = OSWConfig.from_env()
    assert config.base_url == "https://test.example.com"
    assert config.admin_password == "secret123"
    assert config.browser == "firefox"
    assert config.headless is True


def test_config_frozen():
    import pytest

    config = OSWConfig()
    with pytest.raises(AttributeError):
        config.base_url = "http://other"  # type: ignore[misc]
