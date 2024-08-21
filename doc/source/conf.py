"""Sphinx documentation configuration file."""
from datetime import datetime

from sphinx_gallery.sorting import FileNameSortKey

# -- Project information -----------------------------------------------------

project = "api-eigen-example"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS Inc."

# The short X.Y version
release = version = "0.0.1"

# -- General configuration ---------------------------------------------------
extensions = [
    "jupyter_sphinx",
    "notfound.extension",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_gallery.gen_gallery",
    "sphinxemoji.sphinxemoji",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
    "sphinx.ext.todo",
    "breathe",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "numpy": ("https://numpy.org/devdocs", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "pyvista": ("https://docs.pyvista.org/", None),
}

# SS01, SS02, SS03, GL08 all need clean up in the code to be reactivated.
# numpydoc configuration
numpydoc_use_plots = True
numpydoc_show_class_members = False
numpydoc_xref_param_type = True
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    # "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    # "SS02",  # Summary does not start with a capital letter
    "SS03",  # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Copy button customization ---------------------------------------------------
# exclude traditional Python prompts from the copied code
copybutton_prompt_text = r">>> ?|\.\.\. "
copybutton_prompt_is_regexp = True

# -- Sphinx Gallery Options ---------------------------------------------------
sphinx_gallery_conf = {
    # convert rst to md for ipynb
    # "pypandoc": True,
    # path to your examples scripts
    "examples_dirs": ["../../examples/"],
    # path where to save gallery generated examples
    "gallery_dirs": ["examples"],
    # Pattern to search for example files
    "filename_pattern": r"\.py",
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery example by file name instead of number of lines (default)
    "within_subsection_order": FileNameSortKey,
    # directory where function granular galleries are stored
    "backreferences_dir": None,
    # Modules for which function level galleries are created.  In
    "doc_module": "api-eigen-example",
    "ignore_pattern": "flycheck*",
    "thumbnail_size": (350, 350),
    "reset_modules_order": "both",
}


# -- Options for HTML output -------------------------------------------------
html_short_title = html_title = "API Eigen Example"
html_theme = "ansys_sphinx_theme"
html_theme_options = {
    "logo": "ansys",
    "github_url": "https://github.com/ansys/api-eigen-example",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "api-eigen-example-doc"


# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"api-eigen-example-Documentation-{version}.tex",
        "API Eigen Example Documentation",
        author,
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "api-eigen-example",
        "API Eigen Example Documentation",
        [author],
        1,
    )
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "api-eigen-example",
        "API Eigen Example Documentation",
        author,
        "api-eigen-example",
        "A demo project for showing different protocol communications (API REST, gRPC) both in Python and C++.",
        "Engineering Software",
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]

# -- Import the C++ docs -----------------------------------------------------

import subprocess

subprocess.call("make clean", shell=True)
subprocess.call(
    "cd ../../src/ansys/eigen/cpp/rest/server/docs ; doxygen; cd -", shell=True
)
subprocess.call(
    "cd ../../src/ansys/eigen/cpp/rest/client/docs ; doxygen; cd -", shell=True
)
subprocess.call(
    "cd ../../src/ansys/eigen/cpp/grpc/server/docs ; doxygen; cd -", shell=True
)
subprocess.call(
    "cd ../../src/ansys/eigen/cpp/grpc/client/docs ; doxygen; cd -", shell=True
)

breathe_projects = {
    "cpp-rest-server": "../../src/ansys/eigen/cpp/rest/server/docs/xml/",
    "cpp-rest-client": "../../src/ansys/eigen/cpp/rest/client/docs/xml/",
    "cpp-grpc-server": "../../src/ansys/eigen/cpp/grpc/server/docs/xml/",
    "cpp-grpc-client": "../../src/ansys/eigen/cpp/grpc/client/docs/xml/",
}
breathe_default_project = "cpp-rest-server"

breathe_projects_source = {
    "cpp-rest-server": (
        "../../src/ansys/eigen/cpp/rest/server/src",
        ["RestServer.hpp", "RestDb.hpp", "EigenFunctionalities.hpp"],
    ),
    "cpp-rest-client": (
        "../../src/ansys/eigen/cpp/rest/client/src",
        ["EigenClient.hpp"],
    ),
    "cpp-grpc-server": (
        "../../src/ansys/eigen/cpp/grpc/server/src",
        ["GRPCServer.hpp", "GRPCService.hpp"],
    ),
    "cpp-grpc-client": (
        "../../src/ansys/eigen/cpp/grpc/client/src",
        ["GRPCClient.hpp"],
    ),
}
breathe_show_include = False
breathe_separate_member_pages = True
