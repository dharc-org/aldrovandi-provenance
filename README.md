# Aldrovandi Provenance

[![Tests](https://github.com/dharc-org/aldrovandi-provenance/actions/workflows/run-tests.yml/badge.svg)](https://github.com/dharc-org/aldrovandi-provenance/actions/workflows/run-tests.yml)
[![Coverage](https://byob.yarr.is/arcangelo7/badges/dharc-org-aldrovandi-provenance-coverage-master)](https://dharc-org.github.io/aldrovandi-provenance/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Repo Size](https://img.shields.io/github/repo-size/dharc-org/aldrovandi-provenance)](https://github.com/dharc-org/aldrovandi-provenance)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE)

This repository contains tools for managing provenance information for cultural heritage data using the CHAD-AP (Cultural Heritage Acquisition and Digitisation Application Profile) model.

## Overview

The project provides tools for generating provenance snapshots from RDF data, conforming to the [CHAD-AP specification](https://dharc-org.github.io/chad-ap/current/chad-ap.html).

The provenance model implemented in this project is based on the OpenCitations Data Model:

> Daquino, Marilena; Massari, Arcangelo; Peroni, Silvio; Shotton, David (2018). The OpenCitations Data Model. figshare. Online resource. [https://doi.org/10.6084/m9.figshare.3443876.v8](https://doi.org/10.6084/m9.figshare.3443876.v8)

The primary feature is generating provenance snapshots from RDF data in various formats, where:
- Provenance information is organized into named graphs
- Each subject in the input data receives its own provenance graph 
- Snapshot entities are created to represent the state of cultural heritage objects
- Provenance metadata includes generation time and responsible agent information

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
python -m aldrovandi_provenance.generate_provenance INPUT_DIRECTORY OUTPUT_FILE --agent AGENT_ORCID --primary-source PRIMARY_SOURCE_URI [--format FORMAT]
```

Arguments:
- `INPUT_DIRECTORY`: Directory containing RDF files to process
- `OUTPUT_FILE`: Output file for provenance snapshots (N-Quads format)
- `--agent`: ORCID of the responsible agent (required)
- `--primary-source`: URI of the primary source for the data (required)
- `--format`: (Optional) Force specific input format instead of auto-detection

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
python -m aldrovandi_provenance.generate_provenance data/ output.nq --agent https://orcid.org/0000-0002-8420-0696 --primary-source https://doi.org/10.5281/zenodo.15102846
```

The output will include provenance metadata in named graphs, with information about when the snapshot was created, by whom, and the primary source from which the data was derived.

## Development

### Running Tests

```bash
pytest -xvs tests/
```
