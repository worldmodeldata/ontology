# LUDO — Serious Games / Game Model Ontology — Source Package

## What this is
- **Source ontology**: LUDO (Inria namespace, game model / serious games related vocabulary)
- **Purpose in our repo**: Treat as an *external source ontology* that we **reference + align** to our universal foundation (`ug:`/`ub:`) via mapping files, rather than directly merging into the flagship ontology.

## Provenance
- **Namespace landing**: `https://ns.inria.fr/ludo/`
- **RDF distribution (RDF/XML)**: `https://ns.inria.fr/ludo/v1/gamemodel.rdf`
- **Local files**
  - `sources/ludo/ludo.rdf` (downloaded RDF/XML)
  - `sources/ludo/ludo.ttl` (normalized Turtle, generated via rdflib)

## License
The RDF includes a Creative Commons license triple:
- **CC-BY 3.0**: `http://creativecommons.org/licenses/by/3.0/`

## Basic statistics (from `ludo.ttl`)
- **Triples**: 950
- **OWL ontology headers**: 2
- **Classes**: 64
- **Object properties**: 43
- **Datatype properties**: 25
- **Annotation properties**: 0

## How we will incorporate LUDO
- Keep LUDO as a source ontology under `sources/ludo/`.
- Create/extend alignment in `mappings/ludo_to_universal.ttl`:
  - map game-model concepts that overlap with our foundation (e.g., actions, rules, objectives, sessions) to `ug:` concepts
  - leave niche serious-game semantics as source-only until we have concrete data sources that require them


