# -*- coding: latin-1 -*-
#retriever

"""Retriever script for direct download of vertnet-mammals data"""
from builtins import str
from retriever.lib.models import Table
from retriever.lib.templates import Script
import os
from pkg_resources import parse_version
try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Vertnet Mammals"
        self.name = "vertnet-mammals"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.1.1'
        self.ref = "http://vertnet.org/resources/datatoolscode.html"
        self.urls = {
            'mammals': 'https://de.iplantcollaborative.org/anon-files//iplant/home/shared/commons_repo/curated/Vertnet_Mammalia_Sep2016/VertNet_Mammalia_Sept2016.zip',
        }
        self.citation = "Bloom, D., Wieczorek J., Russell, L. (2016).  VertNet_Mammals_Sept. 2016. CyVerse Data Commons. http://datacommons.cyverse.org/browse/iplant/home/shared/commons_repo/curated/VertNet_Mammals_Sep2016"
        self.description = "Compilation of digitized museum records of mammals including locations, dates of collection, and some trait data."
        self.keywords = ['mammals']

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        filename = 'vertnet_latest_mammals.csv'
        tablename = 'mammals'

        table = Table(str(tablename), delimiter=',')
        table.columns = [
            ("record_id", ("pk-auto",)),
            ("beginrecord", ("char",)),
            ("icode", ("char",)),
            ("title", ("char",)),
            ("citation", ("char",)),
            ("contact", ("char",)),
            ("email", ("char",)),
            ("emlrights", ("char",)),
            ("gbifdatasetid", ("char",)),
            ("gbifpublisherid", ("char",)),
            ("doi", ("char",)),
            ("migrator", ("char",)),
            ("networks", ("char",)),
            ("orgcountry", ("char",)),
            ("orgname", ("char",)),
            ("orgstateprovince", ("char",)),
            ("pubdate", ("char",)),
            ("source_url", ("char",)),
            ("iptrecordid", ("char",)),
            ("associatedmedia", ("char",)),
            ("associatedoccurrences", ("char",)),
            ("associatedorganisms", ("char",)),
            ("associatedreferences", ("char",)),
            ("associatedsequences", ("char",)),
            ("associatedtaxa", ("char",)),
            ("bed", ("char",)),
            ("behavior", ("char",)),
            ("catalognumber", ("char",)),
            ("continent", ("char",)),
            ("coordinateprecision", ("char",)),
            ("coordinateuncertaintyinmeters", ("char",)),
            ("country", ("char",)),
            ("countrycode", ("char",)),
            ("county", ("char",)),
            ("dateidentified", ("char",)),
            ("day", ("char",)),
            ("decimallatitude", ("char",)),
            ("decimallongitude", ("char",)),
            ("disposition", ("char",)),
            ("earliestageorloweststage", ("char",)),
            ("earliesteonorlowesteonothem", ("char",)),
            ("earliestepochorlowestseries", ("char",)),
            ("earliesteraorlowesterathem", ("char",)),
            ("earliestperiodorlowestsystem", ("char",)),
            ("enddayofyear", ("char",)),
            ("establishmentmeans", ("char",)),
            ("eventdate", ("char",)),
            ("eventid", ("char",)),
            ("eventremarks", ("char",)),
            ("eventtime", ("char",)),
            ("fieldnotes", ("char",)),
            ("fieldnumber", ("char",)),
            ("footprintspatialfit", ("char",)),
            ("footprintsrs", ("char",)),
            ("footprintwkt", ("char",)),
            ("formation", ("char",)),
            ("geodeticdatum", ("char",)),
            ("geologicalcontextid", ("char",)),
            ("georeferencedby", ("char",)),
            ("georeferenceddate", ("char",)),
            ("georeferenceprotocol", ("char",)),
            ("georeferenceremarks", ("char",)),
            ("georeferencesources", ("char",)),
            ("georeferenceverificationstatus", ("char",)),
            ("group", ("char",)),
            ("habitat", ("char",)),
            ("highergeography", ("char",)),
            ("highergeographyid", ("char",)),
            ("highestbiostratigraphiczone", ("char",)),
            ("identificationid", ("char",)),
            ("identificationqualifier", ("char",)),
            ("identificationreferences", ("char",)),
            ("identificationremarks", ("char",)),
            ("identificationverificationstatus", ("char",)),
            ("identifiedby", ("char",)),
            ("individualcount", ("char",)),
            ("island", ("char",)),
            ("islandgroup", ("char",)),
            ("latestageorhigheststage", ("char",)),
            ("latesteonorhighesteonothem", ("char",)),
            ("latestepochorhighestseries", ("char",)),
            ("latesteraorhighesterathem", ("char",)),
            ("latestperiodorhighestsystem", ("char",)),
            ("lifestage", ("char",)),
            ("lithostratigraphicterms", ("char",)),
            ("locality", ("char",)),
            ("locationaccordingto", ("char",)),
            ("locationid", ("char",)),
            ("locationremarks", ("char",)),
            ("lowestbiostratigraphiczone", ("char",)),
            ("materialsampleid", ("char",)),
            ("maximumdepthinmeters", ("char",)),
            ("maximumdistanceabovesurfaceinmeters", ("char",)),
            ("maximumelevationinmeters", ("char",)),
            ("member", ("char",)),
            ("minimumdepthinmeters", ("char",)),
            ("minimumdistanceabovesurfaceinmeters", ("char",)),
            ("minimumelevationinmeters", ("char",)),
            ("month", ("char",)),
            ("municipality", ("char",)),
            ("occurrenceid", ("char",)),
            ("occurrenceremarks", ("char",)),
            ("occurrencestatus", ("char",)),
            ("organismid", ("char",)),
            ("organismname", ("char",)),
            ("organismremarks", ("char",)),
            ("organismscope", ("char",)),
            ("othercatalognumbers", ("char",)),
            ("pointradiusspatialfit", ("char",)),
            ("preparations", ("char",)),
            ("previousidentifications", ("char",)),
            ("recordedby", ("char",)),
            ("recordnumber", ("char",)),
            ("reproductivecondition", ("char",)),
            ("samplingeffort", ("char",)),
            ("samplingprotocol", ("char",)),
            ("sex", ("char",)),
            ("startdayofyear", ("char",)),
            ("stateprovince", ("char",)),
            ("typestatus", ("char",)),
            ("verbatimcoordinates", ("char",)),
            ("verbatimcoordinatesystem", ("char",)),
            ("verbatimdepth", ("char",)),
            ("verbatimelevation", ("char",)),
            ("verbatimeventdate", ("char",)),
            ("verbatimlatitude", ("char",)),
            ("verbatimlocality", ("char",)),
            ("verbatimlongitude", ("char",)),
            ("verbatimsrs", ("char",)),
            ("waterbody", ("char",)),
            ("year", ("char",)),
            ("dctype", ("char",)),
            ("modified", ("char",)),
            ("language", ("char",)),
            ("license", ("char",)),
            ("rightsholder", ("char",)),
            ("accessrights", ("char",)),
            ("bibliographiccitation", ("char",)),
            ("dc_references", ("char",)),
            ("institutionid", ("char",)),
            ("collectionid", ("char",)),
            ("datasetid", ("char",)),
            ("institutioncode", ("char",)),
            ("collectioncode", ("char",)),
            ("datasetname", ("char",)),
            ("ownerinstitutioncode", ("char",)),
            ("basisofrecord", ("char",)),
            ("informationwithheld", ("char",)),
            ("datageneralizations", ("char",)),
            ("dynamicproperties", ("char",)),
            ("scientificnameid", ("char",)),
            ("namepublishedinid", ("char",)),
            ("scientificname", ("char",)),
            ("acceptednameusage", ("char",)),
            ("originalnameusage", ("char",)),
            ("namepublishedin", ("char",)),
            ("namepublishedinyear", ("char",)),
            ("higherclassification", ("char",)),
            ("kingdom", ("char",)),
            ("phylum", ("char",)),
            ("class", ("char",)),
            ("order", ("char",)),
            ("family", ("char",)),
            ("genus", ("char",)),
            ("subgenus", ("char",)),
            ("specificepithet", ("char",)),
            ("infraspecificepithet", ("char",)),
            ("taxonrank", ("char",)),
            ("verbatimtaxonrank", ("char",)),
            ("scientificnameauthorship", ("char",)),
            ("vernacularname", ("char",)),
            ("nomenclaturalcode", ("char",)),
            ("taxonomicstatus", ("char",)),
            ("keyname", ("char",)),
            ("haslicense", ("int",)),
            ("vntype", ("char",)),
            ("rank", ("int",)),
            ("mappable", ("int",)),
            ("hashid", ("char",)),
            ("hastypestatus", ("int",)),
            ("wascaptive", ("int",)),
            ("wasinvasive", ("int",)),
            ("hastissue", ("int",)),
            ("hasmedia", ("int",)),
            ("isfossil", ("int",)),
            ("haslength", ("int",)),
            ("haslifestage", ("int",)),
            ("hasmass", ("int",)),
            ("hassex", ("int",)),
            ("lengthinmm", ("double",)),
            ("massing", ("double",)),
            ("lengthunitsinferred", ("char",)),
            ("massunitsinferred", ("char",)),
            ("underivedlifestage", ("char",)),
            ("underivedsex", ("char",))]

        engine.table = table
        if not os.path.isfile(engine.format_filename(filename)):
            engine.download_files_from_archive(self.urls[tablename], [filename], filetype="zip", archivename="vertnet_latest_" + str(tablename))
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename(str(filename)))


SCRIPT = main()
