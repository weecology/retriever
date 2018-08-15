# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'main': Table('main', columns=[(u'created_at', (u'char',)), (u'tree_id', (u'int',)), (u'block_id', (u'int',)), (u'the_geom', (u'skip',)), (u'tree_dbh', (u'int',)), (u'stump_diam', (u'int',)), (u'curb_loc', (u'char',)), (u'status', (u'char',)), (u'health', (u'char',)), (u'spc_latin', (u'char',)), (u'spc_common', (u'char',)), (u'steward', (u'char',)), (u'guards', (u'char',)), (u'sidewalk', (u'char',)), (u'user_type', (u'char',)), (u'problems', (u'char',)), (u'root_stone', (u'char',)), (u'root_grate', (u'char',)), (u'root_other', (u'char',)), (u'trnk_wire', (u'char',)), (u'trnk_light', (u'char',)), (u'trnk_other', (u'char',)), (u'brnch_ligh', (u'char',)), (u'brnch_shoe', (u'char',)), (u'brnch_othe', (u'char',)), (u'address', (u'char',)), (u'zipcode', (u'int',)), (u'zip_city', (u'char',)), (u'cb_num', (u'int',)), (u'borocode', (u'int',)), (u'boroname', (u'char',)), (u'cncldist', (u'int',)), (u'st_assem', (u'int',)), (u'st_senate', (u'int',)), (u'nta', (u'char',)), (u'nta_name', (u'char',)), (u'boro_ct', (u'int',)), (u'state', (u'char',)), (u'latitude', (u'double',)), (u'longitude', (u'double',)), (u'x_sp', (u'double',)), (u'y_sp', (u'double',))])},
                           version="1.0.1",
                           title="New York City TreesCount",
                           citation="TreeCount 2015 is citizen science project of NYC Parks'[https://www.nycgovparks.org/trees/treescount]. ",
                           name="nyc-tree-count",
                           retriever_minimum_version="2.0.dev",
                           urls={u'main': u'https://data.cityofnewyork.us/api/views/5rq2-4hqu/rows.csv?accessType=DOWNLOAD'},
                           keywords=[u'trees', u'new-york-city', u'biology', u'observational'],
                           retriever=True,
                           ref="https://www.nycgovparks.org/trees/treescount",
                           description="Dataset consist of every street tree of New York City on the block")