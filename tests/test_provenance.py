#!/usr/bin/env python3
"""
Tests for the provenance generator script.
"""

import os
import sys
import tempfile
import shutil
import pytest
from rdflib import Dataset, URIRef, Namespace
from rdflib.namespace import RDF

# Add the src directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from aldrovandi_provenance.generate_provenance import generate_provenance_snapshots

@pytest.fixture
def test_environment():
    """Set up test data and environment."""
    test_dir = tempfile.mkdtemp(dir='./tests/')
    test_ttl = os.path.join(test_dir, 'test_data.ttl')
    test_output = tempfile.mktemp(suffix='.nq')
    
    # Create test data file
    with open(test_ttl, 'w') as f:
        f.write("""
@prefix ex: <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .

ex:item1 a crm:E22_Human-Made_Object ;
    rdfs:label "Test Manuscript" .

ex:item2 a crm:E21_Person ;
    rdfs:label "John Doe" .
        """)
    
    yield {"test_dir": test_dir, "test_ttl": test_ttl, "test_output": test_output}
    
    # Clean up
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    if os.path.exists(test_output):
        os.remove(test_output)

def test_provenance_generation(test_environment):
    """Test that provenance snapshots are generated correctly."""
    # Get test environment variables
    test_dir = test_environment["test_dir"]
    test_output = test_environment["test_output"]
    
    # Generate provenance snapshots
    agent_orcid = "https://orcid.org/0000-0002-8420-0696"
    generate_provenance_snapshots(test_dir, test_output, agent_orcid=agent_orcid)
    
    # Check that the output file was created
    assert os.path.exists(test_output), "Output file was not created"
    
    # Load the output file
    dataset = Dataset()
    dataset.parse(test_output, format='nquads')
    
    # Define namespaces
    PROV = Namespace('http://www.w3.org/ns/prov#')
    
    # Check that we have the expected named graphs
    expected_graphs = [
        URIRef('http://example.org/item1/prov/'),
        URIRef('http://example.org/item2/prov/')
    ]
    actual_graphs = [g.identifier for g in dataset.contexts()]
    
    for graph in expected_graphs:
        assert graph in actual_graphs, f"Expected graph {graph} not found"
    
    # Check that snapshots are typed as prov:Entity
    item1_prov_graph = dataset.graph(URIRef('http://example.org/item1/prov/'))
    item2_prov_graph = dataset.graph(URIRef('http://example.org/item2/prov/'))
    
    item1_snapshot = URIRef('http://example.org/item1/prov/se/1')
    item2_snapshot = URIRef('http://example.org/item2/prov/se/1')
    
    assert (item1_snapshot, RDF.type, PROV.Entity) in item1_prov_graph, "item1 snapshot is not typed as prov:Entity"
    assert (item2_snapshot, RDF.type, PROV.Entity) in item2_prov_graph, "item2 snapshot is not typed as prov:Entity"
    

if __name__ == '__main__':
    pytest.main() 