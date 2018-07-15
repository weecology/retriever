# -*- coding: UTF-8 -*-
#retriever

import os
import re

import requests

from retriever.lib.models import Table
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "The NOAA Fisheries Monthly Commercial Landing Statistic"
        """The NOAA Fisheries, Fisheries Statistics Division is a summary of U.S. commercial fisheries landings"""
        self.name = "noaa-fisheries-landing"
        self.retriever_minimum_version = '2.1.dev'
        self.version = '1.0.0'
        self.ref = "https://www.st.nmfs.noaa.gov/commercial-fisheries/commercial-landings/monthly-landings/index"
        self.citation = "No known Citation"
        self.description = "The NOAA Fisheries, Fisheries Statistics Division " \
                           "is a summary of U.S. commercial fisheries landings"
        self.keywords = ["Fish", "Fisheries", "United States",
                         "Fisheries of the United States"]

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        engine.create_raw_data_dir()

        species = ['ALL SPECIES COMBINED', 'ABALONE, BLACK', 'ABALONE, FLAT', 'ABALONE, GREEN', 'ABALONE, PINK',
                   'ABALONE, PINTO', 'ABALONE, RED', 'ABALONE, THREADED', 'ABALONE, WHITE', 'ABALONES', 'ALEWIFE',
                   'ALFONSIN', 'ALGAE, MARINE', 'ALGAE,GREEN,BRYOPSIDALES', 'ALGAE,GREEN,ULOTRICHALES',
                   'ALGAE,RED,CORALLINACEAE', 'ALLIGATOR, AMERICAN', 'AMBERJACK', 'AMBERJACK, GREATER',
                   'AMBERJACK, LESSER', 'AMOEBOID PROTISTS,FORAMS', 'AMPHIBIANS', 'ANCHOVIES', 'ANCHOVY, BAY',
                   'ANCHOVY, DEEPBODY', 'ANCHOVY, NORTHERN', 'ANCHOVY, SLOUGH', 'ANEMONE,OTHER', 'ANEMONE,RINGED',
                   'ANEMONE,SPECKLED', 'ANEMONE,SUN', 'ANEMONE,SUN ZOANTHID', 'ANENONE,GIANT CARIBBEAN',
                   'ANGELFISH,BLUE', 'ANGELFISH,FRENCH', 'ANGELFISH,GRAY', 'ANGELFISH,QUEEN', 'ANGELFISHES',
                   'ANGELWING', 'ANIMALS,HYDRALIKE', 'ARCTIC CHAR', 'ARGENTINES', 'ARMORHEAD, PELAGIC', 'ATKA MACKEREL',
                   'AUSTRALIAN ROCKLING', 'BALLOONFISH', 'BALLYHOO', 'BARBIER, RED', 'BARRACUDA, PACIFIC',
                   'BARRACUDA,GREAT', 'BARRACUDAS', 'BARRAMUNDI', 'BARRELFISH', 'BASS, BLACKMOUTH', 'BASS, KELP',
                   'BASS, LONGTAIL', 'BASS, ROCK', 'BASS, STRIPED', 'BASS, WHITE', 'BASS, YELLOW', 'BASS,CAVE',
                   'BASS,CHALK', 'BASS,HARLEQUIN', 'BASS,LANTERN', 'BASS,PEPPERMINT', 'BASS,ROUGHTONGUE',
                   'BASS,THREADNOSE', 'BASS,WRASSE', 'BASSLET,CANDY', 'BASSLET,THREELINE', 'BATFISH,OTHER', 'BEARDFISH',
                   'BEAUGREGORY', 'BEAUTY,ROCK', 'BIGEYE', 'BIGEYE, SHORT', 'BILLFISHES', 'BLACK DRIFTFISH',
                   'BLACK MARGATE', 'BLACKSMITH', 'BLENNY,BANDED', 'BLENNY,BARRED', 'BLENNY,FLORIDA', 'BLENNY,GLASS',
                   'BLENNY,HAIRY', 'BLENNY,LONGHORN', 'BLENNY,MARBLED', 'BLENNY,OTHER', 'BLENNY,REDLIP',
                   'BLENNY,SADDLED', 'BLENNY,SAILFIN', 'BLENNY,WRASSE', 'BLEUFER', 'BLOODWORMS', 'BLUEFISH', 'BLUEHEAD',
                   'BONEFISH', 'BONITO, ATLANTIC', 'BONITO, PACIFIC', 'BONITO, STRIPED', 'BONITOS', 'BOWFIN',
                   'BOXFISHES', 'BREAM,RED', 'BRITTLE STAR,OTHER', 'BRITTLE STAR,SERPENT', 'BROTULA, BEARDED',
                   'BROTULA,BLACK', 'BROTULA,KEY', 'BUFFALOFISHES', 'BULLEYE', 'BULLHEAD, BROWN', 'BUMPER,ATLANTIC',
                   'BURBOT', 'BURRFISH,SPOTTED', 'BURRFISH,STRIPED', 'BUTTERFISH', 'BUTTERFLYFISH,BANDED',
                   'BUTTERFLYFISH,BANK', 'BUTTERFLYFISH,FOUREYE', 'BUTTERFLYFISH,FRENCH', 'BUTTERFLYFISH,LONGSNOUT',
                   'BUTTERFLYFISH,REEF', 'BUTTERFLYFISH,SPOTFIN', 'BUTTERFLYFISHES', 'CABEZON', 'CALIFORNIA ROACH',
                   'CAPELIN', 'CARDINALFISH,TWOSPOT', 'CARDINALFISHES', 'CARP, COMMON', 'CARP, GRASS', 'CARP,BIGHEAD',
                   'CARP,SILVER', 'CARPS AND MINNOWS', 'CASSIOPEA,JAMAICAN', 'CATFISH, BLUE', 'CATFISH, CHANNEL',
                   'CATFISH, FLATHEAD', 'CATFISH,GAFFTOPSAIL', 'CATFISH,HARDHEAD', 'CHERUBFISH', 'CHITON',
                   'CHROMIS,BLUE', 'CHROMIS,BROWN', 'CHUB,BERMUDA', 'CHUBS', 'CIGARFISH, CAPE FATHEAD', 'CIGARFISHES',
                   'CLAM, ARC, BLOOD', 'CLAM, ARCTIC SURF (STIMPSON)', 'CLAM, ATLANTIC JACKKNIFE',
                   'CLAM, ATLANTIC RANGIA', 'CLAM, ATLANTIC SURF', 'CLAM, BUTTER', 'CLAM, CALIFORNIA JACKKNIFE',
                   'CLAM, MANILA', 'CLAM, NORTHERN QUAHOG', 'CLAM, OCEAN QUAHOG', 'CLAM, PACIFIC GEODUCK',
                   'CLAM, PACIFIC LITTLENECK', 'CLAM, PACIFIC RAZOR', 'CLAM, PACIFIC, GAPER', 'CLAM, PISMO',
                   'CLAM, QUAHOG', 'CLAM, ROSY JACKKNIFE', 'CLAM, SOFTSHELL', 'CLAM, STOUT TAGELUS',
                   'CLAM, SUNRAY VENUS', 'CLAM, VARIABLE COQUINA', 'CLAM,JEWEL BOX', 'CLAM,SOUTHERN QUAHOG',
                   'CLAMS OR BIVALVES', 'CLINGFISHES', 'COBIA', 'COCKLE, NUTTALL', 'COD, ATLANTIC', 'COD, PACIFIC',
                   'COD, SAFFRON', 'CODFISHES', 'CONCH,CROWN', 'CONCH,FLORIDA FIGHTING', 'CONCH,HAWKWING',
                   'CONCH,HORSE', 'CONCH,MILK', 'CONCH,OTHER', 'CONCH,QUEEN', 'CONEY', 'COOTER,RIVER',
                   'CORAL,DEEPWATER', 'CORALLIMORPH,DISCOSOMA', 'CORALS', 'CORALS,CORALLIMORPHARIA',
                   'CORALS,CORALLIMORPHIDAE', 'CORALS,RICORDEA FLORIDA', 'CORBINA, CALIFORNIA',
                   'CORNETFISH,BLUESPOTTED', 'CORNETFISH,RED', 'CORVINA, SHORTFIN', 'COWFISH,HONEYCOMB',
                   'COWFISH,HONEYCOMBED', 'COWFISH,SCRAWLED', 'COWRIE,ATLANTIC DEER', 'COWRIE,ATLANTIC GRAY',
                   'COWRIE,MEASLED', 'CRAB, ATLANTIC ROCK', 'CRAB, BLUE', 'CRAB, BLUE LAND', 'CRAB, BLUE, PEELER',
                   'CRAB, BLUE, SOFT', 'CRAB, BLUE, SOFT AND PEELER', 'CRAB, CANCER', 'CRAB, DEEPSEA GOLDEN',
                   'CRAB, DEEPSEA RED', 'CRAB, DUNGENESS', 'CRAB, FLORIDA STONE CLAWS', 'CRAB, GOLDEN KING',
                   'CRAB, GREEN', 'CRAB, HAIR', 'CRAB, HORSESHOE', 'CRAB, JONAH', 'CRAB, KING', 'CRAB, RED PA',
                   'CRAB, RED ROCK', 'CRAB, SNOW', 'CRAB, SNOW/TANNER', 'CRAB, SOUTHERN TANNER', 'CRAB, SPIDER',
                   'CRAB,CALICO BOX', 'CRAB,CORAL SPIDER', 'CRAB,FALSE ARROW', 'CRAB,FIDDLER', 'CRAB,FURCATE SPIDER',
                   'CRAB,GREEN CLINGING', 'CRAB,MITHRAX RED', 'CRAB,NIMBLE SPRAY', 'CRAB,PORTLY SPIDER',
                   'CRAB,RED-RIDGED CLINGING', 'CRAB,REDFINGER RUBBLE', 'CRAB,SPOTTED PORCELAIN',
                   'CRAB,YELLOWLINE ARROW', 'CRABS ', 'CRABS,BOX', 'CRABS,BRACHYURA', 'CRABS,CLINGING,MITHRACULUS',
                   'CRABS,HERMIT', 'CRABS,HORSESHOE', 'CRABS,LAND HERMIT', 'CRABS,PORCELAIN', 'CRABS,SAND',
                   'CRABS,SPIDER,MAJOIDEA', 'CRAPPIE', 'CRAWFISH,PROCAMBARUS', 'CRAYFISHES OR CRAWFISHES',
                   'CREOLE-FISH', 'CRIMSON ROVER', 'CROAKER, ATLANTIC', 'CROAKER, BLACK', 'CROAKER, PACIFIC WHITE',
                   'CROAKER, SPOTFIN', 'CROAKER, YELLOWFIN', 'CROAKER,REEF', 'CUBBYU', 'CUCUMBER,FLORIDA SEA', 'CUNNER',
                   'CUSK', 'CUSK-EELS', 'CUTLASSFISH', 'CUTLASSFISH, ATLANTIC', 'CUTTLEFISHES', 'DAMSELFISH,BICOLOR',
                   'DAMSELFISH,COCOA', 'DAMSELFISH,DUSKY', 'DAMSELFISH,LONGFIN', 'DAMSELFISH,THREESPOT',
                   'DAMSELFISH,YELLOWTAIL', 'DAMSELFISHES', 'DEALFISH', 'DICK,SLIPPERY', 'DOCTORFISH', 'DOLLAR,SAND',
                   'DOLLY VARDEN', 'DOLPHIN', 'DOLPHIN, ATLANTIC SPOTTED', 'DOLPHINFISH', 'DORIS,FLORIDA REGAL',
                   'DORY, AMERICAN JOHN', 'DRAGONETS', 'DRUM, BLACK', 'DRUM, FRESHWATER', 'DRUM, RED', 'DRUM,BANDED',
                   'DRUM,SPOTTED', 'DRUMS', 'DURGON,BLACK', 'ECHINODERM', 'EEL, AMERICAN', 'EEL, CONGER', 'EEL, MORAYS',
                   'EEL,GOLDSPOTTED', 'EEL,SHARPTAIL', 'EEL,SPECKLED WORM', 'EELS', 'EELS, CONGER', 'EELS, SNAKE',
                   'EMPERORS', 'ESCOLAR', 'EYE,SHARK', 'FILECLAM,ROUGH', 'FILECLAM,SPINY', 'FILEFISH,ORANGESPOTTED',
                   'FILEFISH,PLANEHEAD', 'FILEFISH,SCRAWLED', 'FILEFISH,UNICORN', 'FILEFISH,WHITESPOTTED', 'FILEFISHES',
                   'FINFISH,OPHIDIIFORMS', 'FINFISHES, ANADROMUS', 'FINFISHES, FW, OTHER',
                   'FINFISHES, GROUNDFISHES, OTHER', 'FINFISHES, MARINE, ORNAMENTAL', 'FINFISHES, MARINE, OTHER',
                   'FINFISHES, PELAGIC, OTHER', 'FINFISHES, UNC BAIT AND ANIMAL FOOD', 'FINFISHES, UNC FOR FOOD',
                   'FINFISHES, UNC GENERAL', 'FINFISHES, UNC SPAWN', 'FISHES,PERCH-LIKE', 'FLAMEFISH', 'FLATFISH',
                   'FLOUNDER, ARROWTOOTH', 'FLOUNDER, FOURSPOT', 'FLOUNDER, PACIFIC, SANDDAB', 'FLOUNDER, SOUTHERN',
                   'FLOUNDER, STARRY', 'FLOUNDER, SUMMER', 'FLOUNDER, WINDOWPANE', 'FLOUNDER, WINTER',
                   'FLOUNDER, WITCH', 'FLOUNDER, YELLOWTAIL', 'FLOUNDER,ATLANTIC,PLAICE', 'FLOUNDER,GULF',
                   'FLOUNDER,PACIFIC,SANDDAB', 'FLOUNDER,PACIFIC,SANDDAB,LONGFIN', 'FLOUNDER,PACIFIC,SANDDAB,SPECKLE',
                   'FLOUNDERS, RIGHTEYE', 'FLYINGFISHES', 'FROGFISH,OCELLATED', 'FROGFISHES', 'FROGS', 'GAG',
                   'GAMBUSIA,MANGROVE', 'GAR,ALLIGATOR', 'GAR,LONGNOSE', 'GAR,SHORTNOSE', 'GAR,SPOTTED', 'GARS',
                   'GLASSEYE SNAPPER', 'GOATFISH,SPOTTED', 'GOATFISH,YELLOW', 'GOATFISHES', 'GOBY,GREENBANDED',
                   'GOBY,NAKED', 'GOBY,NEON', 'GOBY,OTHER', 'GOBY,TIGER', 'GOBY,YELLOWLINE', 'GOLDFISH', 'GOOSEFISH',
                   'GOOSEFISH, BLACKFIN', 'GORGONIAN,SEA BLADES', 'GRAMMA,ROYAL', 'GRAYSBY', 'GREENLING, KELP',
                   'GREENLINGS', 'GRENADIERS', 'GROUNDFISH (PROCESSED PRODUCTS ONLY)', 'GROUPER, BLACK',
                   'GROUPER, BROOMTAIL', 'GROUPER, GOLIATH', 'GROUPER, MARBLED', 'GROUPER, MISTY', 'GROUPER, NASSAU',
                   'GROUPER, RED', 'GROUPER, SNOWY', 'GROUPER, TIGER', 'GROUPER, WARSAW', 'GROUPER, YELLOWEDGE',
                   'GROUPER, YELLOWFIN', 'GROUPER, YELLOWMOUTH', 'GROUPERS', 'GRUNT, BARRED', 'GRUNT, BLUESTRIPED',
                   'GRUNT, COTTONWICK', 'GRUNT, FRENCH', 'GRUNT, SAILORS CHOICE', 'GRUNT, SMALLMOUTH', 'GRUNT, SPANISH',
                   'GRUNT, TOMTATE', 'GRUNT, WHITE', 'GRUNTS', 'GULF SIERRA', 'GUNNEL, ROCK', 'GUNNELS', 'HADDOCK',
                   'HAGFISHES', 'HAKE, ATLANTIC, RED/WHITE', 'HAKE, BLUE', 'HAKE, LONGFIN', 'HAKE, OFFSHORE SILVER',
                   'HAKE, PACIFIC (WHITING)', 'HAKE, RED', 'HAKE, SILVER', 'HAKE, SILVER (OFFSHORE MIXED)',
                   'HAKE, SOUTHERN', 'HAKE, SPOTTED', 'HAKE, WHITE', 'HALFMOON', 'HALIBUT, ATLANTIC',
                   'HALIBUT, ATLANTIC/PACIFIC', 'HALIBUT, CALIFORNIA', 'HALIBUT, GREENLAND', 'HALIBUT, PACIFIC',
                   'HAMLET,BUTTER', 'HAMLET,MUTTON', 'HARE,SEA', 'HARVESTFISH', 'HARVESTFISHES', 'HAWKFISH,REDSPOTTED',
                   'HERMIT CRAB,RED BANDED', 'HERMIT CRAB,WHITE SPECKLED', 'HERMIT,GIANT', 'HERMIT,ORANGECLAW',
                   'HERMIT,POLKADOTTED', 'HERMIT,STAREYE', 'HERMIT,THINSTRIPE', 'HERMIT,TRICOLOR', 'HERRING, ATLANTIC',
                   'HERRING, ATLANTIC THREAD', 'HERRING, BLUEBACK', 'HERRING, LAKE OR CISCO', 'HERRING, PACIFIC',
                   'HERRING, PACIFIC, ROE ON KELP', 'HERRING, ROUND', 'HERRING, SEA', 'HERRINGS', 'HIGH-HAT',
                   'HIND, RED', 'HIND, ROCK', 'HIND, SPECKLED', 'HOGCHOKER', 'HOGFISH', 'HOGFISH,SPANISH',
                   'HOGFISH,SPOTFIN', 'HOKI', 'HOUNDFISH', 'INCONNU', 'ISOPOD,GIANT', 'JACK MACKEREL', 'JACK, ALMACO',
                   'JACK, BAR', 'JACK, BLACK', 'JACK, CREVALLE', 'JACK, HORSE-EYE', 'JACK, YELLOW', 'JACK,BLUNTNOSE',
                   'JACKKNIFE-FISH', 'JACKS', 'JAWFISH,DUSKY', 'JAWFISH,OTHER', 'JAWFISH,YELLOWHEAD',
                   'JAWFISHES,SPOTFIN', 'JELLY,CANNONBALL', 'JELLYFISH', 'JOBFISH, GREEN (UKU)', 'KILLIFISHES',
                   'KING WHITING', 'KINGFISH, NORTHERN', 'KINGFISH,GULF', 'KINGFISH,SOUTHERN', 'LADYFISH',
                   'LAMPREY, PACIFIC', 'LAMPREY, SEA', 'LANCETFISHES', 'LAUNCE, AMERICAN SAND', 'LEAFFISH,AFRICAN',
                   'LEATHER-SKIN', 'LEATHERJACKET', 'LIMPETS', 'LINGCOD', 'LIONFISH', 'LIONFISH,HAWAIIAN TURKEYFISH',
                   'LIONFISHES', 'LIVE ROCK,ORNAMENTAL AQUACULTURE', 'LIZARDFISH,INSHORE', 'LIZARDFISHES',
                   'LOBSTER, AMERICAN', 'LOBSTER, BANDED SPINY', 'LOBSTER, CALIFORNIA SPINY',
                   'LOBSTER, CARIBBEAN SPINY', 'LOBSTER, SLIPPER', 'LOBSTER,SPANISH', 'LOBSTER,SPOTTED SPINY',
                   'LOOKDOWN', 'LOUVAR', 'LUMPFISH', 'MACKEREL (SCOMBER)', 'MACKEREL, ATLANTIC', 'MACKEREL, BULLET',
                   'MACKEREL, CERO', 'MACKEREL, CHUB', 'MACKEREL, FRIGATE', 'MACKEREL, KING', 'MACKEREL, KING AND CERO',
                   'MACKEREL, SPANISH', 'MACKEREL,ATLANTIC CHUB', 'MAJOR,SERGEANT', 'MAMMALS, AQUATIC', 'MANTAS',
                   'MANTIS SHRIMP,SEA SCORPION', 'MANTIS SHRIMPS', 'MAPLELEAF', 'MARGATE', 'MARLIN, BLACK',
                   'MARLIN, BLUE', 'MARLIN, STRIPED', 'MARLIN, WHITE', 'MAT,GREEN SEA', 'MENHADEN', 'MENHADEN,ATLANTIC',
                   'MILKFISH', 'MINNOW, HARDHEAD', 'MINNOW, HITCH', 'MINNOW, SACRAMENTO SQUAWFISH', 'MITER,FLORIDA',
                   'MOJARRAS', 'MOLA, SHARPTAIL', 'MOLLUSKS', 'MOONEYES', 'MOONFISH, ATLANTIC', 'MORAY, CALIFORNIA',
                   'MORAY,BLACKEDGE', 'MORAY,GOLDENTAIL', 'MORAY,GREEN', 'MORAY,SPOTTED', 'MOSS ANIMALS',
                   'MUDSNAIL,EASTERN', 'MUDSUCKER, LONGJAW', 'MULLET, STRIPED (LIZA)', 'MULLET, WHITE', 'MULLETS',
                   'MUMMICHOG', 'MUSSEL, BLUE', 'MUSSEL, CALIFORNIA', 'MUSSEL,RIBBED', 'MUSSELS, FW', 'NASSA,BRUISED',
                   'NEEDLEFISH, ATLANTIC', 'NEEDLEFISHES', 'NILE PERCH', 'NUDIBRANCHS', 'OCEAN SUNFISH',
                   'OCTOCORAL,SEA PENS/PANZIES', 'OCTOPUS', 'OCTOPUS,ATLANTIC PYGMY', 'OCTOPUS,ATLANTIC WHITE-SPOTTED',
                   'OCTOPUS,CARIBBEAN REEF', 'OCTOPUS,COMMON', 'OILFISH', 'OPAH', 'OPALEYE', 'OYSTER, EASTERN',
                   'OYSTER, EASTERN ', 'OYSTER, EUROPEAN FLAT', 'OYSTER, KUMAMOTO', 'OYSTER, MANGROVE',
                   'OYSTER, OLYMPIA', 'OYSTER, PACIFIC', 'OYSTER, SUMINOE', 'OYSTER,ATLANTIC THORNY', 'PACIFIC SIERRA',
                   'PADDLEFISH', 'PARROTFISH,BLUE', 'PARROTFISH,MIDNIGHT', 'PARROTFISH,PRINCESS', 'PARROTFISH,QUEEN',
                   'PARROTFISH,RAINBOW', 'PARROTFISH,REDBAND', 'PARROTFISH,STOPLIGHT', 'PARROTFISH,STRIPED',
                   'PARROTFISHES', 'PATAGONIAN TOOTHFISH', 'PENSHELL', 'PERCH, BLACK', 'PERCH, DWARF', 'PERCH, PILE',
                   'PERCH, SHINER', 'PERCH, WHITE', 'PERCH, YELLOW', 'PERCH,SILVER', 'PERIWINKLES', 'PERMIT', 'PIGFISH',
                   'PIKE, BLUE', 'PIKES', 'PILOTFISH', 'PINFISH', 'PINFISH, SPOTTAIL', 'PIPEFISH,SARGASSUM',
                   'PIPEFISHES', 'PLANT,CAULERPA', 'PLANT,HALIMEDA', "PLANT,MERMAID'S SHAVING BRUSH",
                   'PLANTS,UNCLASSIFIED', 'POLLOCK', 'POLLOCK, WALLEYE', 'POLYCHAETE,FANWORM',
                   'POLYCHAETE,FEATHER-DUSTER', 'POLYCHAETE,FIREWORM', 'POLYCHAETE,HORNED CHRISTMAS-T',
                   'POMFRET,BIGSCALE', 'POMFRETS', 'POMPANO, AFRICAN', 'POMPANO, FLORIDA', 'POMPANO, PACIFIC',
                   'POMPANO,IRISH', 'PORCUPINEFISH', 'PORGY, JOLTHEAD', 'PORGY, KNOBBED', 'PORGY, LITTLEHEAD',
                   'PORGY, LONGSPINE', 'PORGY, RED', 'PORGY, SAUCEREYE', 'PORGY, WHITEBONE', 'PORGY,GRASS', 'PORKFISH',
                   'POUT, OCEAN', 'PRICKLEBACK, MONKEYFACE', 'PUDDINGWIFE (WRASSE)', 'PUFFER, NOTHERN',
                   'PUFFER,SHARPNOSE', 'PUFFER,SOUTHERN', 'PUFFERS', 'PYGMY FILEFISH', 'QUEENFISH', 'QUILLBACK',
                   'RATFISH SPOTTED', 'RAY, BAT', 'RAY, BULLNOSE', 'RAY, EAGLE', 'RAY, MANTA', 'RAY, PACIFIC ELECTRIC',
                   'RAY,COWNOSE', 'RAY,LESSER ELECTRIC', 'RAY,PELAGIC STINGRAY', 'RAY,STINGRAYS', 'RAYS', 'RAZORFISHES',
                   'REDFISH, ACADIAN', 'REEFFISH,PURPLE', 'REEFFISH,YELLOWTAIL', 'REMORA', 'REPTILES, UNC',
                   'ROCK BASSES, PACIFIC', 'ROCKFISH, AURORA', 'ROCKFISH, BANK', 'ROCKFISH, BLACK',
                   'ROCKFISH, BLACK-AND-YELLOW', 'ROCKFISH, BLACKGILL', 'ROCKFISH, BLUE', 'ROCKFISH, BOCACCIO',
                   'ROCKFISH, BRONZESPOTTED', 'ROCKFISH, BROWN', 'ROCKFISH, CALICO', 'ROCKFISH, CANARY',
                   'ROCKFISH, CHAMELEON', 'ROCKFISH, CHILIPEPPER', 'ROCKFISH, CHINA', 'ROCKFISH, COPPER',
                   'ROCKFISH, COWCOD', 'ROCKFISH, DARKBLOTCHED', 'ROCKFISH, DEACON', 'ROCKFISH, FLAG',
                   'ROCKFISH, GOPHER', 'ROCKFISH, GRASS', 'ROCKFISH, GREENBLOTCHED', 'ROCKFISH, GREENSPOTTED',
                   'ROCKFISH, GREENSTRIPED', 'ROCKFISH, HONEYCOMB', 'ROCKFISH, KELP', 'ROCKFISH, OLIVE',
                   'ROCKFISH, PACIFIC OCEAN PERCH', 'ROCKFISH, PINK', 'ROCKFISH, PINKROSE', 'ROCKFISH, REDBANDED',
                   'ROCKFISH, REDSTRIPE', 'ROCKFISH, ROSY', 'ROCKFISH, SHARPCHIN', 'ROCKFISH, SHORTBELLY',
                   'ROCKFISH, SILVERGRAY', 'ROCKFISH, SPECKLED', 'ROCKFISH, SPLITNOSE', 'ROCKFISH, SQUARESPOT',
                   'ROCKFISH, STARRY', 'ROCKFISH, STRIPETAIL', 'ROCKFISH, SWORDSPINE', 'ROCKFISH, TREEFISH',
                   'ROCKFISH, VERMILION', 'ROCKFISH, WHITEBELLY', 'ROCKFISH, WIDOW', 'ROCKFISH, YELLOWEYE',
                   'ROCKFISH, YELLOWMOUTH', 'ROCKFISH, YELLOWTAIL', 'ROCKFISHES', 'ROSEFISH, BLACKBELLY', 'ROUGHIES',
                   'ROUGHY, BIG', 'ROUGHY, ORANGE', 'RUDDERFISH, BANDED', 'RUDDERFISHES', 'RUNNER, BLUE',
                   'RUNNER, RAINBOW', 'SABLEFISH', 'SACRAMENTO BLACKFISH', 'SAILFISH', 'SALMON, ATLANTIC',
                   'SALMON, CHINOOK', 'SALMON, CHUM', 'SALMON, COHO', 'SALMON, PACIFIC', 'SALMON, PINK',
                   'SALMON, SOCKEYE', 'SAND BASS, BARRED', 'SAND BASS, SPOTTED', 'SAND DOLLAR,5-HOLED KEYHOLE',
                   'SAND DOLLAR,6-HOLED KEYHOLE', 'SAND DOLLAR,NOTCHED', 'SAND DOLLAR,OTHER', 'SAND DOLLARS,KEYHOLE',
                   'SAND PERCH', 'SAND PERCH, DWARF', 'SANDFISH,BELTED', 'SANDWORMS', 'SARDINE, PACIFIC',
                   'SARDINE, SPANISH', 'SARDINE,SCALED', 'SARGASSUMFISH', 'SAUGER', 'SAURIES', 'SAURY, ATLANTIC',
                   'SAURY, PACIFIC', 'SAWFISH, SMALLTOOTH', 'SCAD, BIGEYE', 'SCAD, MACKEREL', 'SCAD, ROUGH',
                   'SCAD, ROUND', 'SCADS', 'SCALLOP, BAY', 'SCALLOP, CALICO', 'SCALLOP, ICELAND', 'SCALLOP, SEA',
                   'SCALLOP, SPINY', 'SCALLOP, WEATHERVANE', 'SCALLOP,LIONS-PAW', 'SCALLOPS', 'SCAMP',
                   'SCORPIONFISH, SPINYCHEEK', 'SCORPIONFISH, SPOTTED', 'SCORPIONFISH,LONGSNOUT', 'SCORPIONFISH,REEF',
                   'SCORPIONFISHES', 'SCULPIN, PACIFIC STAGHORN', 'SCULPIN, YELLOWCHIN', 'SCULPINS', 'SCUP',
                   'SCUPS OR PORGIES', 'SEA BASS, BANK', 'SEA BASS, BLACK', 'SEA BASS, GIANT', 'SEA BASS, ROCK',
                   'SEA BASS,MIXED', 'SEA BASS,PAINTED COMBER', 'SEA BISCUIT,INFLATED', 'SEA BISCUIT,OTHER',
                   'SEA CATFISHES', 'SEA CHUBS', 'SEA CUCUMBER', 'SEA RAVEN', 'SEA SQUIRTS', 'SEA URCHINS',
                   'SEABASS, WHITE', 'SEAHORSE,DWARF', 'SEAHORSE,LINED', 'SEAHORSES', 'SEAL, NORTHERN FUR',
                   'SEAPERCH, PINK', 'SEAPERCH, RAINBOW', 'SEAPERCH, RUBBERLIP', 'SEAPERCH, STRIPED', 'SEAPERCH, WHITE',
                   'SEAROBIN,STRIPED', 'SEAROBINS', 'SEATROUT, SAND', 'SEATROUT, SPOTTED', 'SEATROUT,SILVER',
                   'SEAWEED, IRISH MOSS', 'SEAWEED, KELP', 'SEAWEED, ROCKWEED', 'SEAWEEDS', 'SENNET, SOUTHERN',
                   'SHAD, AMERICAN', 'SHAD, GIZZARD', 'SHAD, HICKORY', 'SHAD, THREADFIN', 'SHADS (NK)',
                   'SHARK, ATLANTIC ANGEL', 'SHARK, ATLANTIC SHARPNOSE', 'SHARK, BASKING', 'SHARK, BIGEYE SAND TIGER',
                   'SHARK, BIGEYE THRESHER', 'SHARK, BIGNOSE', 'SHARK, BLACKNOSE', 'SHARK, BLACKTIP', 'SHARK, BLUE',
                   'SHARK, BONNETHEAD', 'SHARK, BROWN SMOOTHHOUND', 'SHARK, BULL', 'SHARK, CARIBBEAN SHARPNOSE',
                   'SHARK, DOGFISH', 'SHARK, DOGFISH COLLARED', 'SHARK, DUSKY', 'SHARK, FINETOOTH', 'SHARK, GALAPAGOS',
                   'SHARK, GRAY SMOOTHHOUND', 'SHARK, GREAT HAMMERHEAD', 'SHARK, GREENLAND', 'SHARK, GULF SMOOTHHOUND',
                   'SHARK, HAMMERHEAD', 'SHARK, HORN', 'SHARK, LEMON', 'SHARK, LEOPARD', 'SHARK, LITTLE GULPER',
                   'SHARK, LONGFIN MAKO', 'SHARK, MAKOS', 'SHARK, NARROWFIN SMOOTHHOUND', 'SHARK, NARROWTHOOTH',
                   'SHARK, NIGHT', 'SHARK, NURSE', 'SHARK, OCEANIC WHITETIP', 'SHARK, PACIFIC ANGEL',
                   'SHARK, PELAGIC THRESHER', 'SHARK, PORBEAGLE', 'SHARK, REEF', 'SHARK, REQUIEM', 'SHARK, SALMON',
                   'SHARK, SAND TIGER', 'SHARK, SANDBAR', 'SHARK, SCALLOPED HAMMERHEAD', 'SHARK, SEVENGILL',
                   'SHARK, SHARPENOSE SEVENGILL', 'SHARK, SHORTFIN MAKO', 'SHARK, SILKY', 'SHARK, SIXGILL',
                   'SHARK, SIXGILL BIGEYE', 'SHARK, SMALLTAIL', 'SHARK, SMOOTH DOGFISH', 'SHARK, SMOOTH HAMMERHEAD',
                   'SHARK, SOUPFIN', 'SHARK, SPINNER', 'SHARK, SPINY DOGFISH', 'SHARK, SWELL', 'SHARK, THRESHER',
                   'SHARK, TIGER', 'SHARK, WHALE', 'SHARK, WHITE', 'SHARK,CROCODILE', 'SHARK,LARGE PELAGIC SPECIES',
                   'SHARK,SMALL COASTAL SPECIES', 'SHARKS', 'SHARKS, COW', 'SHARKS, MACKEREL', 'SHARKSUCKER',
                   'SHEEPHEAD, CALIFORNIA', 'SHEEPSHEAD', 'SHELLFISH', 'SHELLFISH,UNCLASSIFIED,MARINE,ORNAMENTAL',
                   'SHRIMP, BAY', 'SHRIMP, BLUE MUD', 'SHRIMP, BRINE', 'SHRIMP, BROWN', 'SHRIMP, COONSTRIPE',
                   'SHRIMP, FW ', 'SHRIMP, GHOST', 'SHRIMP, MARINE, OTHER', 'SHRIMP, OCEAN', 'SHRIMP, PACIFIC ROCK',
                   'SHRIMP, PENAEID', 'SHRIMP, PENAEID, AQUACULTURE', 'SHRIMP, PINK', 'SHRIMP, PINK-SPECKLED',
                   'SHRIMP, PINKSPOT', 'SHRIMP, ROCK', 'SHRIMP, ROYAL RED', 'SHRIMP, SCARLET', 'SHRIMP, SEABOB',
                   'SHRIMP, SIDESTRIPE', 'SHRIMP, SPOT', 'SHRIMP, WHITE', 'SHRIMP,BANDED CORAL', 'SHRIMP,CLEANER',
                   'SHRIMP,FARFANTEPENAEUS SPP', 'SHRIMP,GOLDEN CORAL', 'SHRIMP,PALAEMONETES', 'SHRIMP,PANDALID',
                   'SHRIMP,PEDERSON CLEANER', 'SHRIMP,PENAEUS SPP', 'SHRIMP,PEPPERMINT', 'SHRIMP,PISTOL OR SNAPPING',
                   'SHRIMP,ROCK', 'SHRIMP,SPOTTED CLEANER', 'SHRIMP,SQUAT', 'SILVERSIDES', 'SKATE, BARNDOOR',
                   'SKATE, BIG', 'SKATE, CALIFORNIA', 'SKATE, LITTLE', 'SKATES', 'SKATES, LITTLE/WINTER MX', 'SKIPPERS',
                   'SLEEPERS', 'SLIDER,COMMON', 'SLUG,LETTUCE', 'SMELT, EULACHON', 'SMELT, NIGHT', 'SMELT, RAINBOW',
                   'SMELT, SURF', 'SMELT, WHITEBAIT', 'SMELTS', 'SNAIL, MOON', 'SNAIL, SHARK EYE',
                   'SNAIL, SLIPPER LIMPET', 'SNAIL,CONE', 'SNAIL,FROGSNAIL', 'SNAIL,HELMET', 'SNAIL,MARGINELLA',
                   'SNAIL,MELAMPUS', 'SNAIL,MUREX', 'SNAIL,NERITES', 'SNAIL,OLIVE', 'SNAIL,OTHER', 'SNAIL,PURPLE SEA',
                   'SNAIL,STAR', 'SNAIL,TOPSNAIL', 'SNAIL,TRITON', 'SNAIL,TURBONELLA', 'SNAIL,WENTLETRAP',
                   'SNAILS (CONCHS)', 'SNAILS,SEA,CERITHIDEA', 'SNAILS,SEA,FIG', 'SNAILS,SEA,NASSARIUS',
                   'SNAILS,SEA,TEGULA', 'SNAILS,TURBIN', 'SNAKE MACKEREL', 'SNAKEHEAD, NORTHERN',
                   'SNAPPER CARIBBEAN RED', 'SNAPPER, BLACK', 'SNAPPER, BLACKFIN', 'SNAPPER, CARDINAL',
                   'SNAPPER, CUBERA', 'SNAPPER, DOG', 'SNAPPER, GRAY', 'SNAPPER, LANE', 'SNAPPER, MAHOGANY',
                   'SNAPPER, MUTTON', 'SNAPPER, PRISTIPOMOIDES', 'SNAPPER, QUEEN', 'SNAPPER, RED',
                   'SNAPPER, SCHOOLMASTER', 'SNAPPER, SILK', 'SNAPPER, VERMILION', 'SNAPPER, YELLOWTAIL', 'SNAPPERS',
                   'SNOOK', 'SOAPFISHES', 'SOLDIERFISH,BLACKBAR', 'SOLE, BIGMOUTH', 'SOLE, BUTTER', 'SOLE, C-O',
                   'SOLE, CURLFIN', 'SOLE, DEEPSEA', 'SOLE, DOVER', 'SOLE, ENGLISH', 'SOLE, FANTAIL', 'SOLE, FLATHEAD',
                   'SOLE, PETRALE', 'SOLE, REX', 'SOLE, ROCK', 'SOLE, SAND', 'SOLE, SLENDER', 'SOLE, YELLOWFIN',
                   'SOLES', 'SOLES,GYMNACHIRUS', 'SPADEFISH,ATLANTIC', 'SPADEFISHES', 'SPANISH FLAG',
                   'SPEARFISH, LONGBILL', 'SPEARFISH, ROUNDSCALE', 'SPEARFISHES', 'SPIDER CRABS,LIBINIA', 'SPLITTAIL',
                   'SPONGE, GLOVE', 'SPONGE, GRASS', 'SPONGE, SHEEPSWOOL', 'SPONGE, WIRE', 'SPONGE, YELLOW',
                   'SPONGE,RED BALL', 'SPONGES', 'SPONGES,DEMOSPONGIAE', 'SPONGES,HALICLONA', 'SPONGES,SHEEPSWOOL',
                   'SPOT', 'SPOTTED CABRILLA', 'SQUAWFISHES', 'SQUID, CALIFORNIA MARKET', 'SQUID, JUMBO',
                   'SQUID, LONGFIN', 'SQUID, NORTHERN SHORTFIN', 'SQUID, ROBUST CLUBHOOK', 'SQUID,ATLANTIC BRIEF',
                   'SQUIDS', 'SQUIRRELFISH,DEEPWATER', 'SQUIRRELFISH,REEF', 'SQUIRRELFISHES', 'STAR,BASKET',
                   'STAR,BLACK BRITTLE', 'STAR,CUSHIONED', 'STAR,SCALY BRITTLE', 'STARFISH', 'STARGAZER, NOTHERN',
                   'STARGAZER,SOUTHERN', 'STARGAZERS', 'STARS,FEATHER', 'STINGRAY,SOUTHERN', 'STINGRAY,YELLOW',
                   'STINGRAYS', 'STURGEON, ATLANTIC', 'STURGEON, GREEN', 'STURGEON, SHORTNOSE', 'STURGEON, SHOVELNOSE',
                   'STURGEON, WHITE', 'STURGEONS', 'SUCKERS', 'SUNFISHES', 'SUNSHINEFISH', 'SURFPERCH, BARRED',
                   'SURFPERCH, CALICO', 'SURFPERCH, REDTAIL', 'SURFPERCH, SILVER', 'SURFPERCH, WALLEYE', 'SURFPERCHES',
                   'SURGEON,OCEAN', 'SURGEONFISHES', 'SWEEPER,GLASSY', 'SWORDFISH', 'TANG,BLUE', 'TARPON',
                   'TARPON, HAWAIIAN', 'TAUTOG', 'THORNBACK', 'THORNYHEAD, LONGSPINE', 'THORNYHEAD, SHORTSPINE',
                   'THREADFINS', 'THREE-RIDGE', 'THRESHER SHARKS', 'TILAPIAS', 'TILEFISH, ANCHOR',
                   'TILEFISH, BLACKLINE', 'TILEFISH, BLUELINE', 'TILEFISH, GOLDEN', 'TILEFISH, GOLDFACE',
                   'TILEFISH, SAND', 'TILEFISHES', 'TILFISH, GOLDFACE', 'TOADFISHES', 'TOBACCOFISH', 'TOMCOD, ATLANTIC',
                   'TOMCOD, PACIFIC', 'TONGUE,FLAMINGO', 'TONGUEFISH, CALIFORNIA', 'TOPSNAIL, WEST INDIAN', 'TOTOABA',
                   'TRIGGERFISH, GRAY', 'TRIGGERFISH, OCEAN', 'TRIGGERFISH, QUEEN', 'TRIGGERFISH,SARGASSUM',
                   'TRIGGERFISHES', 'TRIPLETAIL', 'TRITON,ANGULAR', 'TROUT, BROOK', 'TROUT, BROWN', 'TROUT, CUTTHROAT',
                   'TROUT, LAKE', 'TROUT, RAINBOW', 'TROUTS', 'TRUMPETFISH', 'TRUNKFISH,SPOTTED',
                   'TRUNKFISHES,THREE-ANGLED', 'TULIP,TRUE', 'TUNA, ALBACORE', 'TUNA, BIGEYE', 'TUNA, BLACK SKIPJACK',
                   'TUNA, BLACKFIN', 'TUNA, BLUEFIN', 'TUNA, BLUEFIN PACIFIC', 'TUNA, KAWAKAWA', 'TUNA, LITTLE TUNNY',
                   'TUNA, LONGTAIL', 'TUNA, SKIPJACK', 'TUNA, YELLOWFIN', 'TUNAS', 'TURBAN,CHESTNUT', 'TURBOT, DIAMOND',
                   'TURBOT, HORNYHEAD', 'TURBOT, SPOTTED', 'TURTLE, GREEN SEA', 'TURTLE, HAWKSBILL SEA',
                   "TURTLE, KEMP'S RIDLEY", 'TURTLE, LEATHERBACK', 'TURTLE, LOGGERHEAD SEA', 'TURTLE, SLIDERS',
                   'TURTLE, SNAPPING', 'TURTLE, SOFT-SHELL', 'TURTLE, TERRAPIN', 'TURTLE,ALLIGATOR SNAPPING',
                   'TURTLE,COMMON MUSK', 'TURTLES', 'TURTLES, BABY (YOUNG FW)', 'TURTLES,NORTH AMERICAN SOFTSHELL',
                   'UNICORNFISH', 'UNIDENTIFIED SPECIES', 'URCHIN,GREEN SEA', 'URCHIN,LONG-SPINED SEA',
                   'URCHIN,PURPLE-SPINED SEA', 'URCHIN,ROCK BORING', 'URCHIN,SLATE PENCIL', 'WAHOO', 'WALLEYE',
                   'WASHBOARD', 'WEAKFISH', 'WENCHMAN', 'WHALES', 'WHELK - FAMILY', 'WHELK, CHANNELED',
                   'WHELK, KNOBBED', 'WHELK, LIGHTNING', 'WHELKS,BUSYCON', 'WHITEFISH, LAKE', 'WHITEFISH, OCEAN',
                   'WHITEFISH, ROUND', 'WOLF-EEL', 'WOLFFISH, ATLANTIC', 'WORMS,CODONELLOPSIDAE', 'WRASSE,BLACKEAR',
                   'WRASSE,CLOWN', 'WRASSE,CREOLE', 'WRASSE,OTHER', 'WRASSE,YELLOWHEAD', 'WRECKFISH', 'YELLOWTAIL JACK']

        states = ['All States', 'Atlantic And Gulf', 'Atlantic And Gulf By State', 'Atlantic', 'Atlantic By State',
                  'New England', 'New England By State', 'Maine', 'New Hampshire', 'Massachusetts', 'Rhode Island',
                  'Connecticut', 'Middle Atlantic', 'Middle Atlantic By State', 'New York', 'New Jersey',
                  'Pennsylvania', 'Delaware', 'Chesapeake', 'Chesapeake By State', 'Maryland', 'Virginia',
                  'South Atlantic', 'South Atlantic By State', 'North Carolina', 'South Carolina', 'Georgia',
                  'Florida, East Coast', 'Florida, Inland Waters', 'Florida, State Total', 'Gulf', 'Gulf By State',
                  'Florida, West Coast', 'Alabama', 'Mississippi', 'Louisiana', 'Texas', 'Pacific', 'Pacific By State',
                  'California', 'Oregon', 'Washington', 'At-Sea Process, Pac.', 'Alaska', 'Hawaii', 'Utah',
                  'Great Lakes', 'Great Lakes By State', 'Illinois', 'Indiana', 'Michigan', 'Minnesota', 'Ohio',
                  'Wisconsin']

        # All by states data includes "state" in the columns
        all_by_state = ["Atlantic And Gulf By State", "Atlantic By State",
                        "New England By State", "Middle Atlantic By State",
                        "Chesapeake By State", "South Atlantic By State",
                        "Gulf By State", "Pacific By State",
                        "Great Lakes By State"]

        # Regex used to create acceptable SQL table names
        state_reg = re.compile(r'[,-.\s]')
        species_reg = re.compile(r'[\-()\',\]/\s]')

        for loc in states:

            state_new = state_reg.sub("_", loc.strip().lower()).rstrip("_")
            for species_i in species:
                species_names = species_i.strip()
                species_new = species_reg.sub("_", species_names.lower()).rstrip("_")
                table_name = "{state_n}_{species_n}".format(state_n=state_new, species_n=species_new)
                table_name = table_name.replace("__", "_")

                csv_file_name = "{tab_name}.csv".format(tab_name=table_name)
                temp_file_path = engine.format_filename("temp")
                new_data_path = engine.format_filename(csv_file_name)

                data = {'qspecies': species_i,
                        'qreturn': 'Species Locator',
                        'qyearfrom': '1990',
                        'qyearto': '2016',
                        'qmonth': 'YEAR BY MONTH',
                        'qstate': loc,
                        'qoutput_type': 'DOWNLOAD ASCII FILE - UNIX'}

                # sending post request and saving response as response object
                base_urls = 'https://www.st.nmfs.noaa.gov/pls/webpls/MF_MONTHLY_LANDINGS.RESULTS'
                try:
                    res = requests.post(url=base_urls, data=data)
                except:
                    pass

                result = res.text

                temp_file = open(temp_file_path, 'w')
                temp_file.write(result)
                temp_file.close()
                table = Table(str(table_name), delimiter=',')

                new_data = open(new_data_path, 'w')
                old_data = open(temp_file_path, 'r')

                columns = '''"Year", "Month", "Species", "Metric_Tons", "Pounds", "currency"\n'''
                table.columns = [("year", ("char", '10')),
                                 ("month", ("char", '10')),
                                 ("species", ('char', '150')),
                                 ("metric_tons", ('char', '15')),
                                 ("pounds", ('char', '15')),
                                 ("currency", ('char', '15'))]

                if loc in all_by_state:
                    columns = '''"Year", "Month", "State", "Species", "Metric_Tons", "Pounds", "currency"\n'''
                    table.columns = [("year", ("char", '10')),
                                     ("month", ("char", '10')),
                                     ("state", ('char', '100')),
                                     ("species", ('char', '150')),
                                     ("metric_tons", ('char', '15')),
                                     ("pounds", ('char', '15')),
                                     ("currency", ('char', '15'))]

                if species_i == 'ALL SPECIES COMBINED':
                    columns = '''"Year", "Month", "State", "Metric_Tons", "Pounds", "currency"\n'''
                    table.columns = [("year", ("char", '10')),
                                     ("month", ("char", '10')),
                                     ("state", ('char', '100')),
                                     ("metric_tons", ('char', '15')),
                                     ("pounds", ('char', '15')),
                                     ("currency", ('char', '15'))]

                new_data.write(columns)
                empty_file = False

                with old_data as file_block:
                    if empty_file:
                        break
                    for counter, lines in enumerate(file_block.readlines()):
                        if counter < 7:
                            continue
                        if counter == 7 and "No Matching Data" in lines:
                            file_block.close()
                            new_data.close()
                            os.remove('{tmp}'.format(tmp=temp_file_path))
                            os.remove('{empty}'.format(empty=new_data_path))
                            empty_file = True
                            break
                        new_data.write(lines)

                if not empty_file:
                    file_block.close()
                    new_data.close()
                    os.remove('{tmp}'.format(tmp=temp_file_path))

                    engine.auto_create_table(table, filename=csv_file_name)
                    engine.insert_data_from_file(engine.format_filename(csv_file_name))


SCRIPT = main()
