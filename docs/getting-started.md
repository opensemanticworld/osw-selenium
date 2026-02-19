# Getting Started

## Installation

Install osw-selenium with pip:

```bash
pip install osw-selenium
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add osw-selenium
```

## Basic Usage

```python
from osw_selenium.foo import foo

result = foo("hello")
print(result)  # hello
```

## Development Setup

Clone the repository and install the development environment:

```bash
git clone https://github.com/opensemanticworld/osw-selenium.git
cd osw-selenium
make install
```

Run the tests:

```bash
make test
```

Build the documentation locally:

```bash
make docs
```
