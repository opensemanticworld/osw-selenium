# Configuration

## Environment Variables

Set these environment variables or use a `.env` file (loaded automatically via `python-dotenv`):

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `MW_SITE_SERVER` | Yes | `http://localhost` | Base URL of the OSL/MediaWiki instance |
| `MW_ADMIN_PASS` | Yes | -- | Admin password |
| `OSW_BROWSER` | No | `chrome` | `chrome` or `firefox` |
| `OSW_HEADLESS` | No | `false` | `true` for headless mode (CI pipelines) |

## .env File

Create a `.env` file in your project root:

```ini
MW_SITE_SERVER=https://my-osw-instance.example.com
MW_ADMIN_PASS=my-secret-password
OSW_BROWSER=chrome
OSW_HEADLESS=false
```

:::{admonition} Security
:class: warning

Never commit `.env` files containing real passwords to version control.
Add `.env` to your `.gitignore`.
:::

## OSWConfig

Load configuration from environment variables:

```python
from osw_selenium.config import OSWConfig

# Load from env vars (and .env file)
config = OSWConfig.from_env()

# Or override specific fields
config = OSWConfig(
    base_url="https://my-osw-instance.example.com",
    browser="firefox",
    headless=True,
)
```

### Available Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `base_url` | `str` | `MW_SITE_SERVER` or `http://localhost` | MediaWiki site URL |
| `admin_password` | `str` | `MW_ADMIN_PASS` or `""` | Admin password |
| `admin_username` | `str` | `Admin` | Admin username |
| `browser` | `str` | `OSW_BROWSER` or `chrome` | Browser name |
| `headless` | `bool` | `OSW_HEADLESS` or `False` | Headless mode |
| `implicit_wait` | `int` | `10` | Implicit wait in seconds |
| `window_width` | `int` | `1280` | Browser window width |
| `window_height` | `int` | `1024` | Browser window height |
| `accept_insecure_certs` | `bool` | `True` | Accept self-signed TLS |

## Browser Setup

::::{tab-set}

:::{tab-item} Chrome
Chrome is the default browser. In headless mode, osw-selenium
uses `--headless=new` (Chrome's modern headless mode), along with
`--no-sandbox` and `--disable-dev-shm-usage` for CI compatibility.

```python
config = OSWConfig(browser="chrome", headless=True)
driver = create_driver(config)
```
:::

:::{tab-item} Firefox
Firefox uses `--headless` for headless mode. Window size is set
via `set_window_size()` after driver creation.

```python
config = OSWConfig(browser="firefox", headless=True)
driver = create_driver(config)
```
:::

::::

## CI Pipeline Usage

::::{tab-set}

:::{tab-item} GitHub Actions
```yaml
env:
  MW_SITE_SERVER: ${{ secrets.MW_SITE_SERVER }}
  MW_ADMIN_PASS: ${{ secrets.MW_ADMIN_PASS }}
  OSW_HEADLESS: "true"
```
:::

:::{tab-item} GitLab CI
```yaml
variables:
  MW_SITE_SERVER: $MW_SITE_SERVER
  MW_ADMIN_PASS: $MW_ADMIN_PASS
  OSW_HEADLESS: "true"
```
:::

::::

:::{admonition} Integration test auto-skip
:class: note

When `MW_SITE_SERVER` is not set, integration tests are automatically
skipped. This means `make test` passes locally even without a running
OSW instance.
:::
