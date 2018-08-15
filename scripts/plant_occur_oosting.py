# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'env': Table('env', replace_columns=[[u'check', u'checkrec']]),'trees': Table('trees', replace_columns=[[u'check', u'checkrec']],cleanup=Cleanup(correct_invalid_value, missing_values=[u'.', u'']))},
                           version="1.2.1",
                           title="Oosting Natural Area (North Carolina) plant occurrence (Palmer et al. 2007)",
                           citation="Michael W. Palmer, Robert K. Peet, Rebecca A. Reed, Weimin Xi, and Peter S. White. 2007. A multiscale study of vascular plants in a North Carolina Piedmont forest. Ecology 88:2674.",
                           name="plant-occur-oosting",
                           retriever_minimum_version="2.0.dev",
                           urls={u'trees': u'https://ndownloader.figshare.com/files/5599967', u'species': u'https://ndownloader.figshare.com/files/5599964', u'pres': u'https://ndownloader.figshare.com/files/5599961', u'env': u'https://ndownloader.figshare.com/files/5599970'},
                           keywords=[u'plants', u'local-scale', u'time-series', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3528371",
                           description="A data set collected in 1989 of vascular plant occurrences in overlapping grids of nested plots in the Oosting Natural Area of the Duke Forest, Orange County, North Carolina, USA.")