# Aldrovandi Provenance

[![Tests](https://github.com/dharc-org/aldrovandi-provenance/actions/workflows/run-tests.yml/badge.svg)](https://github.com/dharc-org/aldrovandi-provenance/actions/workflows/run-tests.yml)
[![Coverage](https://byob.yarr.is/arcangelo7/badges/opedharc-org-aldrovandi-provenance-coverage-main)](https://dharc-org.github.io/aldrovandi-provenance/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Repo Size](https://img.shields.io/github/repo-size/dharc-org/aldrovandi-provenance)](https://github.com/dharc-org/aldrovandi-provenance)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE)

This repository contains tools for managing provenance information for cultural heritage data using the CHAD-AP (Cultural Heritage Acquisition and Digitisation Application Profile) model.

## Overview

The project provides tools for generating provenance snapshots from RDF data, conforming to the [CHAD-AP specification](https://dharc-org.github.io/chad-ap/current/chad-ap.html).

The primary feature is generating provenance snapshots from RDF data in various formats, where:
- Each subject in the input data gets a provenance named graph (subject URI + "/prov/")
- Each subject gets a snapshot entity in its provenance graph (subject URI + "/prov/se/1")
- Each snapshot is typed as a prov:Entity
- Provenance metadata is added, including generation time and responsible agent

## Installation

Requirements:
- Python 3.10+
- Poetry (recommended for development)

### Using Poetry

If Poetry is not already installed, please follow the installation instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

```bash
# Clone the repository
git clone https://github.com/dharc-org/aldrovandi-provenance.git
cd aldrovandi-provenance

# Install dependencies with Poetry
poetry install
```

## Usage

### Generating Provenance Snapshots

The script processes all RDF files in a directory and generates provenance snapshots:

```bash
python -m aldrovandi_provenance.generate_provenance INPUT_DIRECTORY OUTPUT_FILE [--format FORMAT] [--agent AGENT_ORCID]
```

Arguments:
- `INPUT_DIRECTORY`: Directory containing RDF files to process
- `OUTPUT_FILE`: Output file for provenance snapshots (N-Quads format)
- `--format`: (Optional) Force specific input format instead of auto-detection
- `--agent`: (Optional) ORCID of the responsible agent (default: "https://orcid.org/0000-0002-8420-0696")

The script automatically detects RDF file formats based on extensions:
- `.ttl` - Turtle
- `.nt` - N-Triples
- `.n3` - Notation3
- `.xml`, `.rdf` - RDF/XML
- `.jsonld` - JSON-LD
- `.nq` - N-Quads
- `.trig` - TriG

## Example

Input directory contains cultural heritage data in Turtle format:

```turtle
@prefix ex: <http://example.org/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:item1 a crm:E22_Human-Made_Object ;
  rdfs:label "Manuscript" .
```

Command:
```bash
python -m aldrovandi_provenance.generate_provenance data/ output.nq
```

The output will include:
- Named graph `<http://example.org/item1/prov/>` containing snapshot metadata
- Information about when the snapshot was created and by whom
- The snapshot will have type prov:Entity

## Development

### Running Tests

```bash
pytest -xvs tests/
```

## License

See the LICENSE file for details. 