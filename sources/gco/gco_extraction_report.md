# Game Character Ontology (GCO) — Source Package

## What this is
- **Source ontology**: Game Character Ontology (GCO)
- **Purpose in our repo**: Treat as an *external source ontology* that we **reference + align** to our universal foundation (`ug:`/`ub:`) via mapping files, rather than directly merging into the flagship ontology.

## Provenance
- **Canonical page**: `https://autosemanticgame.institutedigitalgames.com/ontologies/game-character-ontology/`
- **Raw download (as provided by publisher)**: `https://autosemanticgame.institutedigitalgames.com/ontologies/game-character-ontology/source/gco.rdf`
- **Local files**
  - `sources/gco/gco.rdf` (downloaded RDF/XML)
  - `sources/gco/gco.ttl` (normalized Turtle, generated via rdflib)

## License
The publisher page states **Creative Commons Attribution 4.0 (CC-BY 4.0)**:
- `http://creativecommons.org/licenses/by/4.0`

## Basic statistics (from `gco.ttl`)
- **Triples**: 1337
- **OWL ontology headers**: 1
- **Classes**: 109
- **Object properties**: 113
- **Datatype properties**: 23
- **Annotation properties**: 2

## How we will incorporate GCO
- **Do not import into** `ontology/ontology/gaming_ontology_v1.ttl` directly.
- Create/extend alignment in `mappings/gco_to_universal.ttl`:
  - `owl:equivalentClass` / `rdfs:subClassOf` where appropriate
  - property alignments (`owl:equivalentProperty`, domain/range bridges)
- When we need “character” semantics universally, prefer:
  - keep rich character-specific semantics in the source ontology + mapping, and
  - mirror only minimal cross-domain hooks into `ontology/universal/*` (e.g., `ug:Character`, `ug:hasCharacter`, etc.).


