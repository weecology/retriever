# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.1",
                           archived=gz,
                           description="GloBI contains code to normalize and integrate existing species-interaction datasets and export the resulting integrated interaction dataset.",
                           title="Global Biotic Interactions (GloBI) data",
                           citation="Poelen, J.H., Simons, J.D. and Mungall, C.J., 2014. Global biotic interactions: an open infrastructure to share and analyze species-interaction datasets. Ecological Informatics, 24, pp.148-159.",
                           name="globi-interaction",
                           retriever_minimum_version="2.1.dev",
                           tables={'interactions': Table('interactions', header_rows=1,columns=[(u'sourceTaxonId', (u'char',)), (u'sourceTaxonIds', (u'char',)), (u'sourceTaxonName', (u'char',)), (u'sourceTaxonRank', (u'char',)), (u'sourceTaxonPathNames', (u'char',)), (u'sourceTaxonPathIds', (u'char',)), (u'sourceTaxonPathRankNames', (u'char',)), (u'sourceId', (u'char',)), (u'sourceOccurrenceId', (u'char',)), (u'sourceCatalogNumber', (u'char',)), (u'sourceBasisOfRecordId', (u'char',)), (u'sourceBasisOfRecordName', (u'char',)), (u'sourceLifeStageId', (u'char',)), (u'sourceLifeStageName', (u'char',)), (u'sourceBodyPartId', (u'char',)), (u'sourceBodyPartName', (u'char',)), (u'sourcePhysiologicalStateId', (u'char',)), (u'sourcePhysiologicalStateName', (u'char',)), (u'interactionTypeName', (u'char',)), (u'interactionTypeId', (u'char',)), (u'targetTaxonId', (u'char',)), (u'targetTaxonIds', (u'char',)), (u'targetTaxonName', (u'char',)), (u'targetTaxonRank', (u'char',)), (u'targetTaxonPathNames', (u'char',)), (u'targetTaxonPathIds', (u'char',)), (u'targetTaxonPathRankNames', (u'char',)), (u'targetId', (u'char',)), (u'targetOccurrenceId', (u'char',)), (u'targetCatalogNumber', (u'double',)), (u'targetBasisOfRecordId', (u'char',)), (u'targetBasisOfRecordName', (u'char',)), (u'targetLifeStageId', (u'char',)), (u'targetLifeStageName', (u'char',)), (u'targetBodyPartId', (u'char',)), (u'targetBodyPartName', (u'char',)), (u'targetPhysiologicalStateId', (u'char',)), (u'targetPhysiologicalStateName', (u'char',)), (u'decimalLatitude', (u'double',)), (u'decimalLongitude', (u'double',)), (u'localityId', (u'char',)), (u'localityName', (u'char',)), (u'eventDateUnixEpoch', (u'char',)), (u'referenceCitation', (u'char',)), (u'referenceDoi', (u'char',)), (u'referenceUrl', (u'char',)), (u'sourceCitation', (u'char',)), (u'sourceNamespace', (u'char',)), (u'sourceArchiveURI', (u'char',)), (u'sourceDOI', (u'char',)), (u'sourceLastSeenAtUnixEpoch', (u'char',))])},
                           urls={u'interactions': u'https://s3.amazonaws.com/globi/snapshot/target/data/tsv/interactions.tsv.gz'},
                           keywords=[u'source', u'target'],
                           ref="https://github.com/jhpoelen/eol-globi-data/wiki",
                           retriever=True)