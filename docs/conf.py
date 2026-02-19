"""Sphinx configuration for osw-selenium."""

project = "osw-selenium"
author = "Andreas Raeder"
project_copyright = "2026, OpenSemanticWorld"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Theme -------------------------------------------------------------------

html_theme = "furo"
html_title = "osw-selenium"

html_theme_options = {
    "source_repository": "https://github.com/opensemanticworld/osw-selenium",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2962ff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#82b1ff",
        "color-brand-content": "#82b1ff",
    },
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
}

# Show section headings in sidebar for each page
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
    ],
}

# -- MyST parser settings ----------------------------------------------------

myst_enable_extensions = [
    "colon_fence",
    "fieldlist",
]
myst_heading_anchors = 3

# -- Intersphinx settings ----------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "selenium": ("https://www.selenium.dev/selenium/docs/api/py/", None),
}

# -- Autodoc settings --------------------------------------------------------

autodoc_member_order = "bysource"

# -- Copy button settings ----------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
