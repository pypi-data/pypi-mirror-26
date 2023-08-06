from string import Template
import json
import os
import logging
from greent.service import Service
from greent.triplestore import TripleStore
from greent.util import LoggingUtil
from greent.util import Text
from reasoner.graph_components import KEdge, KNode
from reasoner import node_types
from pprint import pprint
from cachier import cachier
import datetime

logger = LoggingUtil.init_logging (__file__)

class ChemBioKS(Service):
    """ Generic service endpoints for medical and bio-chemical data. This set
        comprises portions of chem2bio2rdf (CTD, KEGG, PubChem, DRUGBANK) """

    def __init__(self, context): #triplestore):
        super(ChemBioKS, self).__init__("chembio", context)
        self.triplestore = TripleStore (self.url)

    def query_chembio (self, query):
        """ Execute and return the result of a SPARQL query. """
        return self.triplestore.execute_query (query)

    def get_exposure_conditions (self, chemicals):
        """ Identify conditions (MeSH IDs) triggered by the specified stressor
            agent ids (also MeSH IDs).

        :param chemicals: List of IDs for substances of interest.
        :type chemicals: list of MeSH IDs, eg. D052638
        """
        id_list = ' '.join (list(map (lambda d : "( mesh:{0} )".format (d),
                            chemicals)))
        text = self.triplestore.get_template ("ctd_gene_expo_disease").\
            safe_substitute (chemicals=id_list)
        results = self.triplestore.execute_query (text)
        return list(map (lambda b : {
            "chemical" : b['chemical'].value,
            "gene"     : b['gene'].value,
            "pathway"  : b['kegg_pathway'].value,
            "pathName" : b['pathway_name'].value,
            "pathID"   : b['pathway_id'].value,
            "human"    : '(human)' in b['pathway_name'].value
        },
                         results.bindings))

    def get_drugs_by_condition (self, conditions):
        """ Get drugs associated with a set of conditions.

        :param conditions: Conditions to find associated drugs for.
        :type conditions: List of MeSH IDs for conditions, eg.: D001249
        """
        if not isinstance (conditions,list):
            conditions = [ conditions ]

        conditions = list(map(lambda v : v.replace ("MESH:", "mesh:"), conditions))
        prefix = "mesh:"
        if any(map(lambda v : v.startswith(prefix), conditions)):
            prefix = ""
        condition_list = ', '.join (list(map (lambda d : " {0}{1} ".format (prefix, d) , conditions)))
        result = self.triplestore.query_template (
            inputs = { "diseaseIds" : condition_list.lower () },
            outputs = [ 'drugID', 'drugGenericName', 'pubChemCID', 'diseasePMIDs' ],
            template_text="""
            prefix mesh:           <http://bio2rdf.org/mesh:> 
            prefix ctd:            <http://chem2bio2rdf.org/ctd/resource/>
            prefix db_resource:    <http://chem2bio2rdf.org/drugbank/resource/>
            select ?drugID ?drugGenericName ?diseasePMIDs ?ctdChemDis ?pubChemCID where {
               values ( ?diseaseId ) { ( $diseaseIds ) }
               ?ctdChemDis  ctd:cid                        ?pubChemCID;
                            ctd:diseaseid                  ?diseaseId;
                            ctd:pubmedids                  ?diseasePMIDs.
               ?dbInter     db_resource:Name               ?name ;
	                    db_resource:DBID               ?drugID .
               ?drugID      db_resource:CID                ?pubChemCID ;
  	                    db_resource:Generic_Name       ?drugGenericName .
            }""")
        return result

    def get_drugs_by_condition_graph (self, conditions):
        drugs = self.get_drugs_by_condition (conditions.identifier)
        results = []
        for r in drugs:
            edge = KEdge ('c2b2r', 'conditionToDrug',
                          { 'cid' : r['pubChemCID'], 'pmids' : r['diseasePMIDs'] })
            node = KNode (r['drugID'].split('/')[-1:][0],
                          #"http://chem2bio2rdf.org/drugbank/resource/drugbank_drug",
                          node_types.DRUG,
                          r['drugGenericName'])
            results.append ( (edge, node) )
        #logger.debug ("chembio drugs by condition: {}".format (results))
        return results

    def get_genes_pathways_by_disease (self, diseases):
        """ Get genes and pathways associated with specified conditions.

        :param diseases: List of conditions designated by MeSH ID.
        :return: Returns a list of dicts containing gene and path information.
        """
        diseaseMeshIDList = ' '.join (list(map (lambda d : "( mesh:{0} )".format (d), diseases)))
        text = self.triplestore.get_template ("genes_pathways_by_disease").safe_substitute (diseaseMeshIDList=diseaseMeshIDList)
        results = self.triplestore.execute_query (text)
        return list(map (lambda b : {
            "uniprotGene" : b['uniprotGeneID'].value,
            "keggPath"    : b['keggPath'].value,
            "pathName"    : b['pathwayName'].value,
            "human"       : '(human)' in b['pathwayName'].value
        },
        results.bindings))

    def get_drug_gene_disease (self, disease_name, drug_name):
        """ Identify targets and diseases assocaited with a drug name.
        :param disease_name: MeSH name of a disease condition.
        :type str: String
        :param drug_name: Name of a drug.
        :type str: String
        """
        text = self.triplestore.get_template ("drug_gene_disease").safe_substitute (
            diseaseName=disease_name,
            drugName=drug_name)
        results = self.triplestore.execute_query (text)
        return list(map (lambda b : {
            "uniprotSymbol" : b['uniprotSym'].value,
            "diseaseId"     : b['diseaseID'].value
        }, results.bindings))

    def drug_name_to_gene_symbol (self, drug_name):
        result = self.triplestore.query_template (
            inputs = { "drugName" : drug_name },
            outputs = [ 'uniprotSym', 'pmids', 'drugID' ],
            template_text="""
            prefix ctd:            <http://chem2bio2rdf.org/ctd/resource/>
            prefix db_resource:    <http://chem2bio2rdf.org/drugbank/resource/>
            select ?drugGenericName ?pmids ?drugID ?uniprotSym where {
               values ( ?drugName ) { ( "$drugName" ) }
               ?ctdChemGene ctd:cid                        ?pubChemCID;
                            ctd:pubmedids                  ?pmids;
                            ctd:gene                       ?uniprotSym .
               ?drugID      db_resource:CID                ?pubChemCID ;
  	                    db_resource:Generic_Name       ?drugGenericName .
               filter regex(lcase(str(?drugGenericName)), lcase(?drugName))
            }""")
        return list(map(lambda r : {
            'uniprotSym'   : r['uniprotSym'],
            'pmids'        : r.get('pmids', None),
            'drugID'       : r['drugID']
        }, result))

    def gene_symbol_to_pathway (self, uniprot_symbol):
        return self.triplestore.query_template (
            inputs = { "uniprotSymbol" : uniprot_symbol },
            outputs = [ "keggPath" ],
            template_text="""
            prefix kegg:           <http://chem2bio2rdf.org/kegg/resource/>
            prefix pharmgkb:       <http://chem2bio2rdf.org/pharmgkb/resource/>
            prefix ctd:            <http://chem2bio2rdf.org/ctd/resource/>
            select ?ctdGene ?uniprotID ?pathwayName ?keggPath where {
               values ( ?ctdGene ) { ( <$uniprotSymbol> ) }
               ?keggPath    kegg:protein    ?uniprotID ; kegg:Pathway_name ?pathwayName .
               ?pharmGene   pharmgkb:Symbol ?ctdGene ; pharmgkb:UniProt_Id ?uniprotID.
               ?ctdChemGene ctd:gene        ?ctdGene.
            } LIMIT 500
            """)

    def uniprot_to_hgnc (self, uniprot_symbol):
        return self.triplestore.query_template (
            inputs = { "uniprotID" : Text.un_curie (uniprot_symbol.identifier) },
            outputs = [ "hgncID" ],
            template_text="""
            prefix uniprot:    <http://chem2bio2rdf.org/uniprot/resource/gene/>
            prefix owl:        <http://www.w3.org/2002/07/owl#>
            prefix hgnc:       <http://chem2bio2rdf.org/rdf/resource/hgnc/>
            select distinct ?hgncID where {
               values ( ?uniprotID ) { ( uniprot:${uniprotID} ) }
               ?uniprotID <http://www.w3.org/2002/07/owl#sameAs> ?hgncID.
               filter ( strstarts (str(?hgncID), "http://bio2rdf.org/gene:"))
            }
            """)

    def graph_uniprot_to_hgnc (self, uniprot_symbol):
        result = self.uniprot_to_hgnc (uniprot_symbol)
        return [ ( self.get_edge (r, predicate='synonym'), KNode('HGNC:{0}'.format (r['hgncID'].split(':')[-1]), node_types.GENE)) for r in result ]

    def graph_get_genes_by_disease (self, disease): #reasoner
        disease = disease.identifier.split (':')[1].lower ()
        response = self.get_genes_pathways_by_disease ([ disease ])
        results = []
        for r in response:
            edge = KEdge ('c2b2r', 'diseaseToGene', { 'keggPath' : r['keggPath'] })
            node = KNode ("UNIPROT:{0}".format (r['uniprotGene'].split('/')[-1:][0]),  node_types.GENE)
            results.append ( (edge, node) )
        return results

    @cachier(stale_after=datetime.timedelta(days=20))
    def graph_get_pathways_by_gene (self, gene): #reasoner        
        response = self.triplestore.query_template (
            inputs = { "gene" : gene.identifier.split(':')[1].upper () },
            outputs = [ 'keggPath' ],
            template_text="""
            prefix kegg:      <http://chem2bio2rdf.org/kegg/resource/>
            prefix drugbank:  <http://chem2bio2rdf.org/drugbank/resource/>
            prefix uniprot:   <http://chem2bio2rdf.org/uniprot/resource/gene/>
            prefix ctd:       <http://chem2bio2rdf.org/ctd/resource/>
            prefix mesh:      <http://bio2rdf.org/mesh:>
            select ?drugGenericName ?uniprotGeneID ?pathwayName ?keggPath where {
               ?keggPath    kegg:protein                ?swissProtID ;
                            kegg:Pathway_name           ?pathwayName .
               ?keggInter   kegg:cid                    ?pubchemCID .
               ?dbInter     drugbank:GeneBank_ID        ?geneBankID ;
                            drugbank:SwissProt_ID       ?swissProtID ;
                            drugbank:gene               ?uniprotGeneID .
               ?drugID      drugbank:CID                ?pubchemCID ;
                            drugbank:Generic_Name       ?drugGenericName .
               ?ctd_disease ctd:diseaseid               ?diseaseID ;
                            ctd:cid                     ?pubchemCID .
               values ( ?uniprotGeneID ) {
                  ( uniprot:$gene )
               }
            } LIMIT 2000""")
        results = []
        for r in response:
            edge = KEdge ('c2b2r', 'geneToPathway', {})
            node = KNode ("KEGG:{0}".format (r['keggPath'].split('/')[-1:][0]), node_types.PATHWAY)
            results.append ( (edge, node) )
        return results

    def graph_drugname_to_gene_symbol (self, drug_name_node):
        drug_name = Text.un_curie (drug_name_node.identifier)
        response = self.drug_name_to_gene_symbol (drug_name)
        results = []
        for r in response:
            edge = self.get_edge (r, predicate="targets")
            node = KNode ("UNIPROT:{0}".format (Text.path_last (r['uniprotSym'])), node_types.GENE)
            results.append ( (edge, node) )
        return results
    
    def graph_name_to_drugbank (self, drug_name_node):
        drug_name = Text.un_curie (drug_name_node.identifier)
        response = self.drug_name_to_gene_symbol (drug_name)
        results = []
        for r in response:
            edge = self.get_edge (r, predicate="drugname")
            node = KNode ("DRUGBANK:{0}".format (Text.path_last (r['drugID'])), node_types.DRUG)
            results.append ( (edge, node) )
        return results

    def graph_get_pathways_by_gene (self, gene): #reasoner        
        response = self.triplestore.query_template (
            inputs = { "gene" : gene.identifier.split(':')[1].upper () },
            outputs = [ 'keggPath' ],
            template_text="""
            prefix kegg:      <http://chem2bio2rdf.org/kegg/resource/>
            prefix drugbank:  <http://chem2bio2rdf.org/drugbank/resource/>
            prefix uniprot:   <http://chem2bio2rdf.org/uniprot/resource/gene/>
            prefix ctd:       <http://chem2bio2rdf.org/ctd/resource/>
            prefix mesh:      <http://bio2rdf.org/mesh:>
            select ?drugGenericName ?uniprotGeneID ?pathwayName ?keggPath where {
               ?keggPath    kegg:protein                ?swissProtID ;
                            kegg:Pathway_name           ?pathwayName .
               ?keggInter   kegg:cid                    ?pubchemCID .
               ?dbInter     drugbank:GeneBank_ID        ?geneBankID ;
                            drugbank:SwissProt_ID       ?swissProtID ;
                            drugbank:gene               ?uniprotGeneID .
               ?drugID      drugbank:CID                ?pubchemCID ;
                            drugbank:Generic_Name       ?drugGenericName .
               ?ctd_disease ctd:diseaseid               ?diseaseID ;
                            ctd:cid                     ?pubchemCID .
               values ( ?uniprotGeneID ) {
                  ( uniprot:$gene )
               }
            } LIMIT 2000""")
        results = []
        for r in response:
            edge = KEdge ('c2b2r', 'geneToPathway', {})
            node = KNode ("KEGG:{0}".format (r['keggPath'].split('/')[-1:][0]), node_types.PATHWAY)
            results.append ( (edge, node) )
        return results

    def graph_drugbank_to_uniprot (self, drugbank):
        response = self.triplestore.query_template (
            inputs = { "drugID" : "DB{0}".format (Text.un_curie (drugbank.identifier)) },
            outputs = [ "uniprotGeneID" ],
            template_text = """
            prefix drugbank:      <http://chem2bio2rdf.org/drugbank/resource/>
            prefix drugbank_drug: <http://chem2bio2rdf.org/drugbank/resource/drugbank_drug/>
            prefix ctd:           <http://chem2bio2rdf.org/ctd/resource/>
            select distinct ?uniprotGeneID where {
               values ( ?drugID ) { ( drugbank_drug:${drugID} ) }
               ?dbInter     drugbank:GeneBank_ID        ?geneBankID ;
                            drugbank:gene               ?uniprotGeneID .
               ?drugID      drugbank:CID                ?pubchemCID ;
                            drugbank:Generic_Name       ?drugGenericName .
               ?ctd_disease ctd:diseaseid               ?diseaseID ;
                            ctd:cid                     ?pubchemCID .
            }""")
        return [ ( self.get_edge (r, predicate='targets'),
                   KNode ("UNIPROT:{0}".format (r['uniprotGeneID'].split('/')[-1:][0]), node_types.GENE) ) for r in response ]

    def graph_diseasename_to_uniprot (self, disease):
        results = []
        response = self.triplestore.query_template (
            inputs = { "diseaseName" : Text.un_curie (disease.identifier) },
            outputs = [ "pubChemCID" ],
            template_text = """
            prefix ctd: <http://chem2bio2rdf.org/ctd/resource/>
            select distinct ?pubChemCID where {
               values ( ?diseaseName ) { ( "$diseaseName" ) }
               ?ctdChemDis  ctd:cid         ?pubChemCID;
                            ctd:diseasename ?diseaseNameRec.
               filter regex(lcase(str(?diseaseNameRec)), lcase(?diseaseName))
            } LIMIT 1""")
        if len(response) > 0: # This is a disease.
            response = self.triplestore.query_template (
                inputs = { "diseaseName" : Text.un_curie(disease.identifier) },
                outputs = [ "disPmids", "chemPmids", "uniprotSym" ],
                template_text = """
                prefix ctd: <http://chem2bio2rdf.org/ctd/resource/>
                select ?disPmids ?ctdChemDis ?chemPmids ?uniprotSym ?diseaseId where {
                  values ( ?diseaseName ) { ( "$diseaseName" ) }
                  ?ctdChemGene ctd:cid         ?pubChemCID;
                               ctd:pubmedids   ?chemPmids;
                               ctd:gene        ?uniprotSym.
                  ?ctdChemDis  ctd:cid         ?pubChemCID;
                               ctd:diseaseid   ?diseaseId;
                               ctd:diseasename ?diseaseNameRec;
                               ctd:pubmedids   ?disPmids.
                  filter regex(lcase(str(?diseaseNameRec)), lcase(?diseaseName))
                } LIMIT 500""")
            for r in response:
                chemPmids = r['chemPmids']
                disPmids = r['disPmids']
                pmids = chemPmids + "|" + disPmids
                edge = self.get_edge (r, predicate='caused_by', pmids=pmids),
                node = KNode ("UNIPROT:{0}".format (r['uniprotSym'].split('/')[-1:][0]), node_types.GENE)
                results.append ( (edge, node) )
        return results

    def graph_diseaseid_to_uniprot (self, drugbank):
        print( drugbank.identifier.lower() )
        response = self.triplestore.query_template (
            inputs = { "diseaseID" : drugbank.identifier.lower () },
            outputs = [ "uniprotGeneID" ],
            template_text = """
            prefix drugbank:      <http://chem2bio2rdf.org/drugbank/resource/>
            prefix drugbank_drug: <http://chem2bio2rdf.org/drugbank/resource/drugbank_drug/>
            prefix ctd:           <http://chem2bio2rdf.org/ctd/resource/>
            prefix mesh.disease:          <http://bio2rdf.org/mesh:> 
            select distinct ?uniprotGeneID where {
               values ( ?diseaseID ) { ( $diseaseID ) }
               ?dbInter     drugbank:gene               ?uniprotGeneID .
               ?drugID      drugbank:CID                ?pubchemCID.
               ?ctd_disease ctd:diseaseid               ?diseaseID ;
                            ctd:cid                     ?pubchemCID .
            }""")
        return [ ( self.get_edge (r, predicate='targets'),
                   KNode ("UNIPROT:{0}".format (r['uniprotGeneID'].split('/')[-1:][0]), node_types.GENE) ) for r in response ]
