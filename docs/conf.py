# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "bite-parser"
copyright = "2022, Jan Gosmann"
author = "Jan Gosmann"

release = "unreleased"
version = "dev"

import os
import re

github_ref = os.environ.get("GITHUB_REF", "")
version_name_match = re.match(r"^refs/heads/(.*)$", github_ref)
if version_name_match:
    version = version_name_match.group(1)
else:
    version_match = re.match(r"^refs/tags/v(\d+\.\d+.\d+)$", github_ref)
    if version_match:
        version = version_match.group(1)
        release = version_match.group(1).rsplit(".", maxsplit=1)[0]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


autodoc_typehints = "signature"


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    filename = info["module"].replace(".", "/")
    ref = "main"
    if version_name_match:
        ref = version_name_match.group(1)
    return f"https://github.com/py-plato/plato/blob/{ref}/{filename}.py"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_theme_options = {"display_version": False}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = ["css/versioning.css"]
html_js_files = ["js/versioning.js"]
