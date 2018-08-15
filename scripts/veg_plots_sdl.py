# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.1",
                           name="veg-plots-sdl",
                           title="Sonoran Desert Lab perennials vegetation plots",
                           citation="Susana Rodriguez-Buritica, Helen Raichle, Robert H. Webb, Raymond M. Turner, and D. Lawrence Venable. 2013. One hundred and six years of population and community dynamics of Sonoran Desert Laboratory perennials. Ecology 94:976.",
                           retriever_minimum_version="2.0.dev",
                           tables={'Stake_info': Table('Stake_info', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA', u'nd'])),'SMDensity': Table('SMDensity', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'Plot_corners': Table('Plot_corners', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'Count1906': Table('Count1906', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'Photo_info': Table('Photo_info', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'Seedling_counts': Table('Seedling_counts', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'Plots': Table('Plots', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'SMCover': Table('SMCover', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'Species': Table('Species', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']))},
                           urls={u'Stake_info': u'https://ndownloader.figshare.com/files/5625351', u'SMDensity': u'https://ndownloader.figshare.com/files/5625348', u'Plot_corners': u'https://ndownloader.figshare.com/files/5625333', u'Count1906': u'https://ndownloader.figshare.com/files/5625342', u'Photo_info': u'https://ndownloader.figshare.com/files/5625354', u'Seedling_counts': u'https://ndownloader.figshare.com/files/5625339', u'Plots': u'https://ndownloader.figshare.com/files/5625330', u'SMCover': u'https://ndownloader.figshare.com/files/5625345', u'Species': u'https://ndownloader.figshare.com/files/5625336'},
                           keywords=[u'plants'],
                           retriever=True,
                           description="The data set constitutes all information associated with the Spalding-Shreve permanent vegetation plots from 1906 through 2012, which is the longest-running plant monitoring program in the world.")