# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.2.1",
                           title="Percentage leaf herbivory across vascular plant species",
                           citation="Martin M. Turcotte, Christina J. M. Thomsen, Geoffrey T. Broadhead, Paul V. A. Fine, Ryan M. Godfrey, Greg P. A. Lamarre, Sebastian T. Meyer, Lora A. Richards, and Marc T. J. Johnson. 2014. Percentage leaf herbivory across vascular plant species. Ecology 95:788. http://dx.doi.org/10.1890/13-1741.1.",
                           name="leaf-herbivory",
                           retriever_minimum_version="2.0.dev",
                           urls={u'Leaf_herbivory': u'https://ndownloader.figshare.com/files/5629563'},
                           keywords=[u'plants', u'literature-compilation'],
                           retriever=True,
                           ref="https://figshare.com/collections/Percentage_leaf_herbivory_across_vascular_plant_species/3306585",
                           description="Spatially explicit measurements of population level leaf herbivory on 1145 species of vascular plants from 189 studies from across the globe.")