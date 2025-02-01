import os
import sys

sys.path.insert(0, os.path.abspath(".."))  # Ensure Sphinx can find your modules

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Supports Google-style and NumPy-style docstrings
]

html_theme = "sphinx_rtd_theme"  # ReadTheDocs theme (optional)
