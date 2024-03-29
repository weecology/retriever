import sys
import sphinx_rtd_theme

from retriever.lib.defaults import ENCODING

encoding = ENCODING.lower()

from retriever.lib.defaults import VERSION, COPYRIGHT
from retriever.lib.scripts import SCRIPT_LIST, reload_scripts
from retriever.lib.tools import open_fw
from retriever.lib.repository import check_for_updates
from retriever.lib.rdatasets import update_rdataset_catalog


def to_str(object, object_encoding=encoding):
    return str(object).encode('UTF-8').decode(encoding)


# Rdatasets
# Create the .rst file for the available APIs
datasetfile = open_fw("available_apis.rst")
datasetfile_title = """==============
APIs Available
==============

**Socrata API**
---------------

**Total number of datasets supported : 85,244 out of 213,965**

**Rdatasets**
-------------


"""
rdatasets = update_rdataset_catalog(test=True)
datasetfile.write(datasetfile_title)

index = 1
for package in rdatasets.keys():
    for dataset in rdatasets[package].keys():
        script = rdatasets[package][dataset]

        title = str(index) + ". **{}**\n".format(to_str(script['title'].strip(), encoding))
        datasetfile.write(title)
        datasetfile.write("~" * (len(title) - 1) + "\n\n")

        name = f"rdataset-{package}-{dataset}"
        # keep the gap between : {} standard as required by restructuredtext
        datasetfile.write(":name: {}\n\n".format(name))
        reference_link = script['doc']
        # Long urls can't render well, embed them in a text(home link)
        datasetfile.write(":reference: `{s}'s home link <{r}>`_.\n".format(
            s=name, r=to_str(reference_link).rstrip("/")))

        datasetfile.write(":R package: {}\n\n".format(package))
        datasetfile.write(":R Dataset: {}\n\n".format(dataset))
        index += 1

datasetfile.write("\n\n")
datasetfile.close()

# Retriever Datasets
# Create the .rst file for the available datasets
datasetfile = open_fw("datasets_list.rst")
datasetfile_title = """==================
Datasets Available
==================


"""
check_for_updates()
reload_scripts()
script_list = SCRIPT_LIST()

# write the title of dataset rst file
# ref:http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
datasetfile.write(datasetfile_title)

# get info from the scripts using specified encoding
for script_num, script in enumerate(script_list, start=1):
    reference_link = ''
    if script.ref.strip():
        reference_link = script.ref
    elif hasattr(script, 'homepage'):
        reference_link = script.homepage
    elif not reference_link.strip():
        if bool(script.urls.values()):
            reference_link = list(script.urls.values())[0].rpartition('/')[0]
        else:
            reference_link = 'Not available'
    title = str(script_num) + ". **{}**\n".format(to_str(script.title.strip(), encoding))
    datasetfile.write(title)
    datasetfile.write("-" * (len(title) - 1) + "\n\n")

    # keep the gap between : {} standard as required by restructuredtext
    datasetfile.write(":name: {}\n\n".format(script.name))

    # Long urls can't render well, embed them in a text(home link)
    if len(to_str(reference_link)) <= 85:
        datasetfile.write(":reference: `{}`\n\n".format(reference_link))
    else:
        datasetfile.write(":reference: `{s}'s home link <{r}>`_.\n".format(
            s=script.name, r=to_str(reference_link).rstrip("/")))

    datasetfile.write(":citation: {}\n\n".format(to_str(script.citation, encoding)))
    datasetfile.write(":description: {}\n\n".format(to_str(script.description, encoding)))
datasetfile.close()

needs_sphinx = '1.3'

# Add any Sphinx extension module names here, as strings.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Data Retriever'
copyright = COPYRIGHT

version = release = VERSION

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".


# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)


# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'
