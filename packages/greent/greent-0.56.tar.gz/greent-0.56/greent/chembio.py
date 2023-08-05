from string import Template
import json
import os
import logging
from greent.triplestore import TripleStore
from greent.util import LoggingUtil
from reasoner.graph_components import KEdge, KNode
from pprint import pprint

logger = LoggingUtil.init_logging (__file__, logging.DEBUG)

class ChemBioKS(object):
    """ Generic service endpoints for medical and bio-chemical data. This set
        comprises portions of chem2bio2rdf, Monarch, and CTD environmental
        exposures."""
    def __init__(self, triplestore):
        self.triplestore = triplestore

    #@provenance()
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

        #condition_list = ' '.join (list(map (lambda d : "( mesh:{0} )".format (d), conditions)))
        conditions = list(map(lambda v : v.replace ("MESH:", "mesh:"), conditions))
        prefix = "mesh:"
        if any(map(lambda v : v.startswith(prefix), conditions)):
            prefix = ""
        '''
        condition_list = ' '.join (list(map (lambda d : "( {0}{1} )".format (prefix, d) , conditions)))
        text = self.triplestore.get_template ("get_drugs_by_disease").substitute (conditions=condition_list)
        print (text)
        results = self.triplestore.execute_query (text)
        return list(map (lambda b : b['generic_name'].value, results.bindings))
        '''

        #print ("-------- {}".format (conditions))
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
        drugs = self.get_drugs_by_condition (conditions)
        results = []
        for r in drugs:
            edge = KEdge ('c2b2r', 'conditionToDrug',
                          { 'cid' : r['pubChemCID'], 'pmids' : r['diseasePMIDs'] })
            node = KNode (r['drugID'].split('/')[-1:][0],
                          "http://chem2bio2rdf.org/drugbank/resource/drugbank_drug",
                          r['drugGenericName'])
            results.append ( (edge, node) )
        print ("chembio drugs by condition: {}".format (results))
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
#        result = self.query (
        result = self.triplestore.query_template (
            inputs = { "drugName" : drug_name },
            outputs = [ 'uniprotSym' ],
            template_text="""
prefix ctd:            <http://chem2bio2rdf.org/ctd/resource/>
prefix db_resource:    <http://chem2bio2rdf.org/drugbank/resource/>
select ?drugGenericName ?uniprotSym where {
    values ( ?drugName ) { ( "$drugName" ) }
    ?ctdChemGene ctd:cid                        ?pubChemCID;
                 ctd:gene                       ?uniprotSym .
    ?drugID      db_resource:CID                ?pubChemCID ;
  	         db_resource:Generic_Name       ?drugGenericName .
  filter regex(lcase(str(?drugGenericName)), lcase(?drugName))
}""")
        #logger.debug (result)
        return list(map(lambda r : r['uniprotSym'], result)) #result
    
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

    
    def graph_get_genes_by_disease (self, disease): #reasoner
        disease = disease.identifier.split (':')[1].lower ()
        response = self.get_genes_pathways_by_disease ([ disease ])
        results = []
        for r in response:
            edge = KEdge ('c2b2r', 'diseaseToGene', { 'keggPath' : r['keggPath'] })
            node = KNode ("UNIPROT:{0}".format (r['uniprotGene'].split('/')[-1:][0]),  "G")
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
            node = KNode ("KEGG.PATHWAY:{0}".format (r['keggPath'].split('/')[-1:][0]), "P")
            results.append ( (edge, node) )
        return results
    
