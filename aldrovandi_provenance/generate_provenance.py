#!/usr/bin/env python3
"""
Script to generate provenance snapshots from RDF data.
This script loads RDF data in various formats from all files in a directory, 
extracts all subjects, and creates provenance snapshots as named graphs 
with type prov:Entity.
"""

import os
import argparse
import datetime
from rdflib import ConjunctiveGraph, URIRef, Namespace, Literal, Dataset
from rdflib.namespace import RDF, XSD, DCTERMS
from rdflib.util import guess_format

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate provenance snapshots from RDF data.')
    parser.add_argument('input_directory', help='Directory containing RDF files to process')
    parser.add_argument('output_file', help='Output file for provenance snapshots (N-Quads format)')
    parser.add_argument('--format', help='Force specific input format instead of auto-detection')
    parser.add_argument('--agent', help='ORCID of the responsible agent', default="https://orcid.org/0000-0002-8420-0696")
    return parser.parse_args()

def generate_provenance_snapshots(input_directory, output_file, input_format=None, agent_orcid=None):
    """
    Generate provenance snapshots from RDF data.
    
    Args:
        input_directory: Path to directory containing RDF files
        output_file: Path to output file with provenance snapshots (N-Quads format)
        input_format: Optional format to use for all input files (overrides auto-detection)
        agent_orcid: ORCID of the responsible agent
    """
    # Load all input RDF files into a single graph
    input_graph = ConjunctiveGraph()
    
    file_count = 0
    
    rdf_extensions = {
        '.ttl': 'turtle',
        '.nt': 'nt',
        '.n3': 'n3',
        '.xml': 'xml',
        '.rdf': 'xml',
        '.jsonld': 'json-ld',
        '.nq': 'nquads',
        '.trig': 'trig'
    }
    
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        
        if os.path.isdir(file_path):
            continue
        
        if input_format:
            format_name = input_format
        else:
            _, ext = os.path.splitext(filename.lower())
            if ext in rdf_extensions:
                format_name = rdf_extensions[ext]
            else:
                try:
                    format_name = guess_format(file_path)
                    if not format_name:
                        print(f"Skipping {file_path}: unable to determine RDF format")
                        continue
                except Exception as e:
                    print(f"Skipping {file_path}: {str(e)}")
                    continue
        
        try:
            print(f"Processing {file_path} as {format_name}...")
            input_graph.parse(file_path, format=format_name)
            file_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    if file_count == 0:
        print(f"No valid RDF files found in {input_directory}")
        return
    
    print(f"Processed {file_count} RDF files")
    
    dataset = Dataset()
    
    PROV = Namespace('http://www.w3.org/ns/prov#')
    dataset.namespace_manager.bind('prov', PROV)
    dataset.namespace_manager.bind('dcterms', DCTERMS)
    
    for prefix, namespace in input_graph.namespaces():
        dataset.namespace_manager.bind(prefix, namespace)
    
    subjects = set()
    for s, p, o in input_graph:
        if isinstance(s, URIRef):
            subjects.add(s)
    
    print(f"Found {len(subjects)} subjects in the input files")
    
    generation_time = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    
    responsible_agent = URIRef(agent_orcid)
    
    for subject in subjects:
        prov_graph_uri = URIRef(f"{subject}/prov/")
        
        snapshot_uri = URIRef(f"{subject}/prov/se/1")
        
        prov_graph = dataset.graph(identifier=prov_graph_uri)
        
        prov_graph.add((snapshot_uri, RDF.type, PROV.Entity))
        
        prov_graph.add((snapshot_uri, PROV.generatedAtTime, Literal(generation_time, datatype=XSD.dateTime)))
        
        prov_graph.add((snapshot_uri, PROV.wasAttributedTo, responsible_agent))
        
        description = f"Entity <{str(subject)}> was created"
        prov_graph.add((snapshot_uri, DCTERMS.description, Literal(description, lang="en")))
    
    dataset.serialize(destination=output_file, format='nquads')
    print(f"Provenance snapshots saved to {output_file}")
    

def main():
    """Main function."""
    args = parse_arguments()
    generate_provenance_snapshots(args.input_directory, args.output_file, args.format, args.agent)

if __name__ == "__main__":
    main() 