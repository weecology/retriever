#retriever
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever import open_fr, open_fw

class main(Script):
    def __init__(self):
        Script.__init__(self,
                        name="Gulf of Maine intertidal density/cover (Petraitis et al. 2008)",
                        citation="Peter S. Petraitis, Harrison Liu, and Erika C. Rhile. 2008. Densities and cover data for intertidal organisms in the Gulf of Maine, USA, from 2003 to 2007. Ecology 89:588.",
                        shortname="intertidal-abund-me",
                        ref="http://www.esapubs.org/archive/ecol/E089/032/",
                        description="The data set provides access to data on densities and percent cover in the 60 experimental plots from 2003 to 2007 and to update data from 1996 to 2002 that are already published in Ecological Archives.It includes densities of mussels, an herbivorous limpet, herbivorous snails, a predatory snail, a barnacle , and fucoid algae and percent cover by mussels, barnacles, fucoids, and other sessile organisms.",
                        retriever_minimum_version='2.0.dev',
                        version='1.3.1',
                        urls={"main": "http://www.esapubs.org/archive/ecol/E089/032/Succession_sampling_03-07_data.txt"},
                        tables={"main": Table("main", cleanup=Cleanup(correct_invalid_value, nulls=[-999.9]))}
                        )

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        self.engine.download_file(self.urls["main"], "Succession_sampling_03-07_data_original.txt")
        data_path = self.engine.format_filename("Succession_sampling_03-07_data.txt")
        old_data = open_fr(self.engine.find_file("Succession_sampling_03-07_data_original.txt"))
        new_data = open_fw(data_path)
        # original file's header contains an end of line charactor in the middle hence creating two lines
        # Read in the two lines and create the full header
        line1 = old_data.readline().strip()
        line2 = old_data.readline()
        newline = line1 + "\t" + line2
        new_data.write(newline)
        for line in old_data:
            new_data.write(line)
        new_data.close()
        old_data.close()

        self.engine.auto_create_table(self.tables["main"],
                                      filename="Succession_sampling_03-07_data.txt")
        self.engine.insert_data_from_file(data_path)

SCRIPT = main()
