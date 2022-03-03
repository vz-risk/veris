# Imports
import json
from pprint import pprint
from collections import OrderedDict, defaultdict
from rdflib import Graph, Namespace
from rdflib.term import Literal, URIRef#, _castPythonToLiteral
from rdflib.namespace import RDF, RDFS, OWL, XSD
import uuid
from urllib.parse import quote, unquote
import logging
import re
import os
from fnmatch import fnmatch
from tqdm import tqdm
import argparse
from datetime import datetime


class i2af():
    af_ns = None
    veris_ns = None
    exclusions = ["incident_id", "plus.master_id", "plus.created", "plus.analyst", "summary"]
    data_props = None
    obj_props = None
    anchor_map = None
    enum_iterator = dict()


    def __init__(
        self,
        veris_schema_filename,
        attack_flow_namespace="https://vz-risk.github.io/flow/attack-flow#",
        veris_namespace="https://veriscommunity.net/attack-flow#"
        ):

        # create namespace from victim_id
        self.af_ns = Namespace(attack_flow_namespace)
        self.veris_ns = Namespace(veris_namespace)

        # open veris schema
        veris = Graph()
        veris.parse(veris_schema_filename)
        # Get object and data properties so we know which are which when parsing them out of the incident
        query = ("""SELECT DISTINCT  ?p 
        WHERE { 
          ?p rdf:type owl:ObjectProperty .
        }""")
        qres = veris.query(query)
        self.obj_props = list(qres)
        self.obj_props = [item[0].split("#")[1] for item in self.obj_props]
        query = ("""SELECT DISTINCT  ?p 
        WHERE { 
          ?p rdf:type owl:DatatypeProperty .
        }""")
        qres = veris.query(query)
        self.data_props = list(qres)
        self.data_props = [item[0].split("#")[1] for item in self.data_props]   
        # all we needed were the property lists
        del(veris)

        # to map from veris_ns to attack flow ns
        self.anchor_map = {
            "action": self.af_ns["action"],
            "asset": self.af_ns["asset"],
            "extra": self.af_ns["property"]
        }


    def recurse_instances(self, d, lbl, owl, i_ns, flowURI, incident, exclusions=[]):
        for k, v in d.items():
            try:
                if type(v) in [OrderedDict, dict]:
                    #keys = keys.union(recurse_keys(v, (lbl + (k,)), keys))
                    self.recurse_instances(v, (lbl + (k,)), owl, i_ns=i_ns, flowURI=flowURI, incident=incident, exclusions=exclusions)
                elif type(v) is list: 
                    for item in v:
                        if type(item) == dict:
                            #print("label: {0}, key: {1}, item: {2}".format(lbl, k, item))
                            self.recurse_instances(item, (lbl + (k,)), owl, i_ns=i_ns, flowURI=flowURI, incident=incident, exclusions=exclusions)
                        elif k == "variety":
                            # convert it to a class instance of the parent class
                            # add it to the incident
                            self.enum_iterator[flowURI][".".join(lbl + (k, item))] += 1 # `lbl + (k, item)` used to be `item`
                            instance_name = quote(item + "_" + str(self.enum_iterator[flowURI][".".join(lbl + (k, item))])) # `".".join(lbl + (k, item))` used to be `item`
                            
                            # define instance as an instance and an instance of something
                            owl.add((i_ns[instance_name], RDF.type, OWL.NamedIndividual))
                            owl.add((i_ns[instance_name], RDF.type, self.anchor_map.get(".".join(lbl), self.veris_ns[quote(".".join(lbl + (k,item)))])))
                            
                            # Connect instance to flow
                            owl.add((i_ns[instance_name], self.af_ns['flow'], flowURI))

                            # if action:
                            if lbl[0] == "action":
                                # (type) = 'action'
                                # name = instance_name
                                # description
                                owl.add((i_ns[instance_name], self.af_ns["description.action"], Literal(incident["action"][lbl[1]].get("notes", "no decription"))))
                                # logic_operator = ""
                                owl.add((i_ns[instance_name], self.af_ns['logic_operator'], Literal("OR")))
                elif k == "variety":
                    # convert it to a class instance of the parent class
                    # add it to the incident
                    instance_name = re.sub("[^0-9a-zA-Z_.\-~]+", "_", ".".join(lbl + (k, v))) # '".".join(lbl + (k, v))' used to be `v`
                    if lbl[0] == "asset" and v not in ["Unknown", "Other"]:
                        instance_name = instance_name[4:]
                    self.enum_iterator[flowURI][instance_name] += 1
                    instance_name = quote(instance_name + "_" + str(self.enum_iterator[flowURI][instance_name]))

                    # define instance as an instance and an instance of something
                    owl.add((i_ns[instance_name], RDF.type, OWL.NamedIndividual))
                    owl.add((i_ns[instance_name], RDF.type, self.anchor_map.get(".".join(lbl), self.veris_ns[quote(".".join(lbl + (k,v)))])))

                    # Connect instance to flow
                    owl.add((i_ns[instance_name], self.af_ns['flow'], flowURI))
            except:
                print("label: {0}, key: {1}, value: {2}".format(lbl, k, v))
                raise
                          
        return owl
                            
                            
    def recurse_properties(self, d, lbl, owl, instances, flowURI, exclusions=[]):
        for k, v in d.items():
            try:
                if type(v) in [OrderedDict, dict]:
                    owl = self.recurse_properties(v, (lbl + (k,)), owl, instances=instances, flowURI=flowURI, exclusions=exclusions)
                    
                elif k == "variety":
                    pass # varieties are all instances and should already be handled
                
                elif (type(v) is list):
                    for item in v:
                        if type(item) == dict:
                            self.recurse_properties(item, (lbl + (k,)), owl, instances=instances, flowURI=flowURI, exclusions=exclusions)
                        else:
                            # define it's flow
                            owl.add((self.veris_ns[quote(".".join(lbl + (k, item)))], self.af_ns['flow'], flowURI))
                            
                            # if we know what instance it goes to, connect it.
                            if str(self.veris_ns[quote(".".join(lbl))]) in instances.keys() and len(instances[str(self.veris_ns[quote(".".join(lbl))])]) == 1:
                                owl.add((instances[str(self.veris_ns[quote(".".join(lbl))])][0], self.veris_ns[quote(".".join(lbl + (k, )))], self.veris_ns[quote(".".join(lbl + (k, item)))]))
                elif (".".join((lbl + (k,str(v)))) in exclusions):
                    pass
                
                else:
                    if quote(".".join(lbl + (k,))) in self.obj_props:
                        if str(self.veris_ns[quote(".".join(lbl))]) in instances.keys() and len(instances[str(self.veris_ns[quote(".".join(lbl))])]) == 1:
                            owl.add((instances[str(self.veris_ns[quote(".".join(lbl))])][0], self.veris_ns[quote(".".join(lbl + (k, )))], self.veris_ns[quote(".".join(lbl + (k, v)))]))
                        else:
                            owl.add((self.veris_ns[quote(".".join(lbl[:-1]))], self.af_ns['flow'], flowURI))
                            owl.add((self.veris_ns[quote(".".join(lbl[:-1]))], self.veris_ns[quote(".".join(lbl + (k, )))], self.veris_ns[quote(".".join(lbl + (k, v)))]))
                    elif quote(".".join(lbl + (k,))) in self.data_props:
                        if str(self.veris_ns[quote(".".join(lbl))]) in instances.keys() and len(instances[str(self.veris_ns[quote(".".join(lbl))])]) == 1:
                            owl.add((instances[str(self.veris_ns[quote(".".join(lbl))])][0], self.veris_ns[quote(".".join(lbl + (k, )))], Literal(v)))
                        else:
                            owl.add((self.veris_ns[quote(".".join(lbl))], self.af_ns['flow'], flowURI))
                            owl.add((self.veris_ns[quote(".".join(lbl))], self.veris_ns[quote(".".join(lbl + (k, )))], Literal(v)))
                    else:
                        logging.warning("{0} is not in the object property or datatype property lists.".format(".".join(lbl + (k,))))
                                  
            except:
                print("label: {0}, key: {1}, value: {2}".format(lbl, k, v))
                raise
                   
        return owl


    def guess_temporal_relationships(self, incident, owl):
        ### Ok, there's going to be a _lot_ going on here...
        
        ### Event chain uses wierd stuff so we'll need to look it up to convert it to what's used 
        #    in the main schema (and hense the graph)
        event_chain_lookup = {
            "ext": "external", "int": "internal", "prt": "partner", "unk": "Unknown",
            "env": "environmental", "err": "Error", "hak": "hacking", "soc": "Social", 
            "mal": "malware", "mis": "misuse", "phy": "Physical",
            "au": "availability", "cp": "confidentiality", "ia": "integrity",
            "emb": "E", "med": "M", "net": "N", "ppl": "P", "srv": "S", "ter": "T", "usr": "U"
        }
        
        
        # We also need to collect all the named individuals for multiple reasons
        query = ("""SELECT DISTINCT  ?inst ?thing
        WHERE { 
          ?inst rdf:type owl:NamedIndividual .
          ?inst rdf:type ?thing .
           FILTER (?thing != owl:NamedIndividual)
        }""")
        qres = owl.query(query)
        res = list(qres)
        
        # NOTE: these are the instances.  They don't tel you what type of action they are.
        # This is mostly useful if there's just 1 action and asset
        actions = [item[0] for item in res if item[1].split("#")[1].startswith("action")]
        assets = [item[0] for item in res if item[1].split("#")[1].startswith("asset")]
        attributes = [item[0] for item in res if item[1].split("#")[1].startswith("attribute")]

        # So we'll start with the event chain
        # Just because it has an event chaind oesn't mean we'll which go in what order...
        if "event_chain" in incident['plus']:
            # first we're going to need to count the number of time each type of actin/asset/attribute occurs
            # this is important because if we have multiple occurrences of any of these things it'll be hard
            # to tell what step they go with.
            occurrence_counts = {
                "oincident": {
                    "action": defaultdict(list),
                    "asset": defaultdict(list),
                    "attribute": defaultdict(list)
                }
            }
            for action in [(item[0], item[1].split("#")[1]) for item in res if item[1].split("#")[1].startswith("action")]:
                occurrence_counts['oincident']['action'][action[1].split(".")[1]].append(action[0])
            for asset in [(item[0], item[1].split("#")[1]) for item in res if item[1].split("#")[1].startswith("asset")]:
                occurrence_counts['oincident']['asset'][asset[1].split(".")[3].split("%20-%20")[0]].append(asset[0])
            for attribute in [(item[0], item[1].split("#")[1]) for item in res if item[1].split("#")[1].startswith("attribute")]:
                occurrence_counts['oincident']['attribute'][attribute[1].split(".")[1]].append(attribute[0])
            
            # If there's more steps, but each action/asset/attribute only occur once in it, we can map instances to it
            if (
                  all([len(v) <= 1 for k,v in occurrence_counts['oincident']['action'].items()]) and 
                  all([len(v) <= 1 for k,v in occurrence_counts['oincident']['asset'].items()]) and 
                  all([len(v) <= 1 for k,v in occurrence_counts['oincident']['attribute'].items()])):
                logging.info("can parse because each item only occurs once.")
                old_asset = None
                for step in incident['plus']['event_chain']:
                    attribute = occurrence_counts['oincident']['attribute'].get(event_chain_lookup[step.get('attribute', "unk")], self.veris_ns + "attribute.unknown")
                    action = occurrence_counts['oincident']['action'].get(event_chain_lookup[step.get('action', "unk")], None)
                    asset = occurrence_counts['oincident']['asset'].get(event_chain_lookup[step.get('asset', "unk")], None)
                    if all([action, asset]):
                        owl.add((URIRef(attribute), RDFS.subPropertyOf, self.af_ns['state_change']))
                        owl.add((URIRef(action), URIRef(attribute), URIRef(asset)))
                    try:
                        if old_asset and action:
                            owl.add((URIRef(old_asset), self.veris_ns["attribute.unknown"], URIRef(action)))
                    except:
                        print(f"{old_asset}, {action}")
                        raise
                    old_asset = asset

        # if only one action & asset, you can assume the sequence
        elif len(assets) == 1 and len(actions) == 1:
            logging.info("Can parse single action/asset.")
            for attribute in attributes:
                owl.add((URIRef(attribute), RDFS.subPropertyOf, self.af_ns['state_change']))
                owl.add((URIRef(actions[0]), URIRef(attribute), URIRef(assets[0])))
                
        else:
            #print("No available logic to sequence actions and assets.")
            logging.warning("No available logic to sequence actions and assets.")
        
        return(owl)


    def incident_to_owl(self, incident):

        # create namespace from victim_id
        i_ns = incident['victim'].get('victim_id', str(uuid.uuid4())).lower()
        i_ns = re.sub("[^0-9a-zA-Z_.\-~]+", "_", i_ns)
        i_ns = Namespace("urn:absolute:" + quote(i_ns) + "#")
        self.i_ns = i_ns
        
        # start the incident's graph
        owl = Graph()
        
        ### create any manditory fields in AF
        # Create flow instance, flow id
        flowURI = i_ns[incident['plus']['master_id']] # to object
        owl.add((flowURI, RDF.type, OWL.NamedIndividual))
        owl.add((flowURI, RDF.type, self.af_ns['attack-flow']))
        # flow name literal
        owl.add((flowURI, self.af_ns['name.attack-flow'], Literal(incident['incident_id'])))
        # flow created literal
        owl.add((flowURI, self.af_ns['created'], Literal(incident['plus'].get("created", "1970-01-01T01:00:00Z"))))
        # flow author literal
        owl.add((flowURI, self.af_ns['author'], Literal(incident['plus'].get("analyst", "Unknown"))))
        # flow description literal
        owl.add((flowURI, self.af_ns['description.attack-flow'], Literal(incident['summary'])))
        self.flowURI = flowURI
        
        # to number instances
        self.enum_iterator[flowURI] = defaultdict(int)


        self.recurse_instances(incident, (), owl, i_ns=i_ns, flowURI=flowURI, incident=incident, exclusions=self.exclusions)

        _ = self.enum_iterator.pop(flowURI) # delete the dictionary of number of instances used for sane naming of instances
        
        query = ("""SELECT DISTINCT  ?inst ?thing
        WHERE { 
          ?inst rdf:type owl:NamedIndividual .
          ?inst rdf:type ?thing .
           FILTER (?thing != owl:NamedIndividual)
        }""")
        qres = owl.query(query)
        instances = defaultdict(set)
        for inst,thing in qres:
            instances[str(thing)].add(str(inst))
        instances = dict()
        instances = {".".join(k.split(".")[:2]):list(v) for k,v in instances.items()}
        
        self.recurse_properties(incident, (), owl, instances=instances, flowURI=flowURI, exclusions=self.exclusions)    
        
        # Determine causal linkages between actions if possible (use value.chain and or single-action)
        owl.add((self.veris_ns["attribute.unknown"], RDFS.subPropertyOf, self.af_ns['state_change']))
        owl = self.guess_temporal_relationships(incident, owl)
        
        return(owl)


    def convert(
        self,
        input_veris,
        output,
        join=False
        ):
        if join:
            g_joined = Graph()

        for root, dirnames, filenames in tqdm(os.walk(input_veris)):
          logging.info("starting parsing of directory {0}.".format(root))
          # filenames = filter(lambda fname: fnmatch(fname, "*.json"), filenames)
          filenames = [fname for fname in filenames if fnmatch(fname, "*.json")] # per 2to3. - GDB 181109
          if filenames:
            dir_ = os.path.join(output, root[len(input_veris):].lstrip("/")) # if we don't strip the input, we get duplicate directories 
            logging.info("Output directory is {0}.".format(dir_))
            if not os.path.isdir(dir_):
                os.makedirs(dir_)
            for fname in filenames:
                in_fname = os.path.join(root, fname)
                out_fname = os.path.join(dir_, (os.path.splitext(fname)[0] + ".jsonld"))

                logging.info("Now processing %s" % in_fname)
                try:
                    #incident = sj.loads(open(in_fname).read())
                    with open(in_fname, 'r') as filehandle:
                        incident = json.load(filehandle)
                except json.JSONDecodeError:
                    logging.warning(
                        "ERROR: %s did not parse properly. Skipping" % in_fname)
                    continue

                g = self.incident_to_owl(incident)
                if join:
                    g_joined.parse(data=g.serialize(format="json-ld"), format="json-ld")
                else:
                    with open(out_fname, 'w') as filehandle:
                        filehandle.write(g.serialize(format="json-ld"))
            if join:
                out_fname = os.path.join(dir_, "joined_veris_graph_{0}.jsonld".format(datetime.now()))
                with open(out_fname, 'w') as filehandle:
                    filehandle.write(g_joined.serialize(format="json-ld"))
                    logging.info(f"output file is {out_fname}.")
 

if __name__ == '__main__':
    descriptionText = """This script creates OWL VERIS incident graphs from JSON VERIS files."""
    parser = argparse.ArgumentParser(description=descriptionText)
    parser.add_argument("-l","--log_level",choices=["critical","error","warning","info","debug"], help="Minimum logging level to display", default="critical")
    parser.add_argument('--log_file', help='Location of log file', default=None)
    parser.add_argument("-i", "--input", required=True,
                        help="top level folder to search for incidents")
    parser.add_argument("-o", "--output", required=True,
                        help="output directory to write new files.")
    parser.add_argument("--veris_schema_graph", help="The veris schema in OWL graph format.", required=True)
    parser.add_argument("--join",help="Join output incident graphs into a single file.",action="store_true")
    parser.add_argument("--veris_ns", help="String representing the namespace for VERIS.", default="https://veriscommunity.net/attack-flow#")
    parser.add_argument("--af_ns", help="String representing the namespace for attack flow. (should match what's in the 'af' file.", default="https://vz-risk.github.io/flow/attack-flow#")

    args = parser.parse_args()
    #args = {k:v for k,v in vars(args).items() if v is not None}

    logging.info("Setting up logging")
    if args.log_file:
        logging.basicConfig(level={"critical": 50, "error": 40, "warning":30, "info":20, "debug":10}.get(args.log_level, 0), filename=args.log_file) 
    else:
        logging.basicConfig(level={"critical": 50, "error": 40, "warning":30, "info":20, "debug":10}.get(args.log_level, 0)) 

    logging.info("Initialize the class.")
    converter = i2af(
        veris_schema_filename = args.veris_schema_graph,
        attack_flow_namespace = args.af_ns,
        veris_namespace = args.veris_ns       
    )

    logging.info("Converting incidents.")
    converter.convert(
        input_veris =args.input,
        output = args.output,
        join=args.join
    )

    logging.info("Conversion complete.")
