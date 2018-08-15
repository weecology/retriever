# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.2",
                           description="Birds migration data",
                           title="A database on visible diurnal spring migration of birds",
                           citation="Georg F. J. Armbruster, Manuel Schweizer, and Deborah R. Vogt. 2011. A database on visible diurnal spring migration of birds (Central Europe:Lake Constance). Ecology 92:1865.",
                           name="bird-migration-data",
                           keywords=[u'Taxon > Plants'],
                           retriever_minimum_version="2.0.0-dev",
                           tables={},
                           urls={u'BirdMigration': u'https://ndownloader.figshare.com/files/5620119', u'observations': u'https://ndownloader.figshare.com/files/5620122'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3551952",
                           retriever=True)