"""Configuration for OSW Selenium tests, loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


@dataclass(frozen=True)
class OSWConfig:
    """Configuration for OSW Selenium tests.

    Args:
        base_url: The MediaWiki site URL (MW_SITE_SERVER env var).
        admin_password: The admin password (MW_ADMIN_PASS env var).
        admin_username: The admin username.
        browser: Browser name — "chrome" or "firefox".
        headless: Run headless if True.
        implicit_wait: Default implicit wait in seconds.
        window_width: Browser window width.
        window_height: Browser window height.
        accept_insecure_certs: Accept self-signed TLS.
    """

    base_url: str = field(default_factory=lambda: os.environ.get("MW_SITE_SERVER", "http://localhost"))
    admin_password: str = field(default_factory=lambda: os.environ.get("MW_ADMIN_PASS", ""))
    admin_username: str = "Admin"
    browser: str = field(default_factory=lambda: os.environ.get("OSW_BROWSER", "chrome").lower())
    headless: bool = field(default_factory=lambda: os.environ.get("OSW_HEADLESS", "false").lower() == "true")
    implicit_wait: int = 10
    window_width: int = 1280
    window_height: int = 1024
    accept_insecure_certs: bool = True

    @classmethod
    def from_env(cls) -> OSWConfig:
        """Create config from environment variables.

        If ``python-dotenv`` is installed, ``.env`` is loaded first.

        Returns:
            A new OSWConfig populated from the current environment.

        Example:
            >>> import os
            >>> os.environ["MW_SITE_SERVER"] = "http://test.local"
            >>> cfg = OSWConfig.from_env()
            >>> cfg.base_url
            'http://test.local'
        """
        load_dotenv()
        return cls()
