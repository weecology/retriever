# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'all_plots_1935_1948': Table('all_plots_1935_1948', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'all_plots_1974_1980': Table('all_plots_1974_1980', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'sampling_history': Table('sampling_history', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']),columns=[(u'record_id', (u'pk-auto',)), (u'plot', (u'char', u'10')), (u'yr_1935', (u'char', u'10')), (u'yr_1948', (u'char', u'10')), (u'yr_1974', (u'char', u'10')), (u'yr_1978', (u'char', u'10')), (u'yr_1979', (u'char', u'10')), (u'yr_1989', (u'char', u'10')), (u'yr_1992', (u'char', u'10')), (u'yr_1993', (u'char', u'10')), (u'yr_1994', (u'char', u'10')), (u'yr_1997', (u'char', u'10')), (u'yr_1999', (u'char', u'10')), (u'yr_2001', (u'char', u'10')), (u'yr_2002', (u'char', u'10')), (u'yr_2004', (u'char', u'10')), (u'yr_2007', (u'char', u'10'))]),'upland_plots_1989_2007': Table('upland_plots_1989_2007', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA', u'']))},
                           version="1.2.1",
                           title="Michigan forest canopy dynamics plots - Woods et al. 2009",
                           citation="Kerry D. Woods. 2009. Multi-decade, spatially explicit population studies of canopy dynamics in Michigan old-growth forests. Ecology 90:3587.",
                           name="forest-plots-michigan",
                           retriever_minimum_version="2.0.dev",
                           urls={u'all_plots_1935_1948': u'https://ndownloader.figshare.com/files/5608016', u'all_plots_1974_1980': u'https://ndownloader.figshare.com/files/5608019', u'swamp': u'https://ndownloader.figshare.com/files/5608025', u'sampling_history': u'https://ndownloader.figshare.com/files/5608031', u'species_codes': u'https://ndownloader.figshare.com/files/5608028', u'upland_plots_1989_2007': u'https://ndownloader.figshare.com/files/5608022'},
                           keywords=[u'plants', u'local-scale', u'time-series', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/collections/Multi-decade_spatially_explicit_population_studies_of_canopy_dynamics_in_Michigan_old-growth_forests/3301757",
                           description="The data set provides stem infomation from a regular grid of 256 permanent plots includes about 20% of a 100-ha old-growth forest at the Dukes Research Natural Area in northern Michigan, USA.")