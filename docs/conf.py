
# # -*- coding: utf-8 -*-
# sphinx_py3doc_enhanced_theme 2.3.2
# A theme based on the theme of https://docs.python.org/3/ with some responsive enhancements.
# https://pypi.python.org/pypi/sphinx_py3doc_enhanced_theme

from __future__ import unicode_literals
from retriever import VERSION  
import os


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon'
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = 'EcoData Retriever'
year = '2016'
author = 'Ethan white'
copyright = '{0}, {1}'.format(year, author)
version = release = VERSION
import sphinx_py3doc_enhanced_theme
html_theme = "sphinx_py3doc_enhanced_theme"
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]
# html_theme_options = {
#     'githuburl': 'https://github.com/ionelmc/python-aspectlib/'
# }

# html_theme_options = {
#     'githuburl': 'https://github.com/ionelmc/sphinx-py3doc-enhanced-theme/',
#     'bodyfont': '"Lucida Grande",Arial,sans-serif',
#     'headfont': '"Lucida Grande",Arial,sans-serif',
#     'codefont': 'monospace,sans-serif',
#     'linkcolor': '#0072AA',
#     'visitedlinkcolor': '#6363bb',
#     'extrastyling': False,
# }
pygments_style = 'trac'
templates_path = ['.']
html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = True
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)