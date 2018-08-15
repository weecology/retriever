# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.1",
                           name="predator-prey-body-ratio",
                           title="Body sizes of consumers and their resources",
                           citation="Ulrich Brose, Lara Cushing, Eric L. Berlow, Tomas Jonsson, Carolin Banasek-Richter, Louis-Felix Bersier, Julia L. Blanchard, Thomas Brey, Stephen R. Carpenter, Marie-France Cattin Blandenier, Joel E. Cohen, Hassan Ali Dawah, Tony Dell, Francois Edwards, Sarah Harper-Smith, Ute Jacob, Roland A. Knapp, Mark E. Ledger, Jane Memmott, Katja Mintenbeck, John K. Pinnegar, Bjorn C. Rall, Tom Rayner, Liliane Ruess, Werner Ulrich, Philip Warren, Rich J. Williams, Guy Woodward, Peter Yodzis, and Neo D. Martinez10. 2005. Body sizes of consumers and their resources. Ecology 86:2545.",
                           retriever_minimum_version="2.0.0-dev",
                           tables={},
                           urls={u'bodysizes': u'https://ndownloader.figshare.com/files/5595857'},
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3525119",
                           description="Body size ratios between predators and their prey,")