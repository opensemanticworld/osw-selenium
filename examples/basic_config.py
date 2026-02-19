"""Example: Configure OSWConfig with explicit values or environment variables."""

from osw_selenium.config import OSWConfig

# Option 1: Load everything from environment variables (or .env file)
config_from_env = OSWConfig.from_env()
print(f"Base URL: {config_from_env.base_url}")
print(f"Browser:  {config_from_env.browser}")
print(f"Headless: {config_from_env.headless}")

# Option 2: Override specific fields (password still comes from env)
config_custom = OSWConfig(
    base_url="https://my-osw-instance.example.com",
    browser="firefox",
    headless=True,
)
print(f"\nCustom base URL: {config_custom.base_url}")
print(f"Custom browser:  {config_custom.browser}")
print(f"Custom headless: {config_custom.headless}")
