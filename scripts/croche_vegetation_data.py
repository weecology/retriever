# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.2",
                           description="The Lac Croche data set covers a nine-year period (1998-2006) of detailed understory vegetation sampling of a temperate North American forest located in the Station de Biologie des Laurentides (SBL), Québec, Canada.",
                           title="Croche understory vegetation data set",
                           citation="Alain Paquette, Etienne Laliberté, André Bouchard, Sylvie de Blois, Pierre Legendre, and Jacques Brisson. 2007. Lac Croche understory vegetation data set (1998-2006). Ecology 88:3209.",
                           name="croche-vegetation-data",
                           keywords=[u'Taxon > plants'],
                           retriever_minimum_version="2.0.0-dev",
                           tables={'croche_ba': Table('croche_ba', nulls=[u'-999'])},
                           urls={u'croche_ba': u'https://ndownloader.figshare.com/files/5600489', u'croche_env': u'https://ndownloader.figshare.com/files/5600486', u'croche_seedDens': u'https://ndownloader.figshare.com/files/5600483', u'croche_vegCover': u'https://ndownloader.figshare.com/files/5600480'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3528707",
                           retriever=True)