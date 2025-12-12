# Core Game Ontology (CGO) — Source Package

## What this is
- **Source ontology**: Core Game Ontology (CGO)
- **Purpose in our repo**: Treat as an *external source ontology* that we **reference + align** to our universal foundation (`ug:`/`ub:`) via mapping files, rather than directly merging into the flagship ontology.

## Provenance
- **Canonical page**: `https://autosemanticgame.institutedigitalgames.com/ontologies/core-game-ontology/`
- **Raw download (as provided by publisher)**: `https://autosemanticgame.institutedigitalgames.com/ontologies/core-game-ontology/source/cgo.rdf`
- **Local files**
  - `sources/cgo/cgo.rdf` (downloaded RDF/XML)
  - `sources/cgo/cgo.ttl` (normalized Turtle, generated via rdflib)

## License
The publisher page states **Creative Commons Attribution 4.0 (CC-BY 4.0)**:
- `http://creativecommons.org/licenses/by/4.0`

## Basic statistics (from `cgo.ttl`)
- **Triples**: 95
- **OWL ontology headers**: 1
- **Classes**: 9
- **Object properties**: 6
- **Datatype properties**: 0
- **Annotation properties**: 2

## How we will incorporate CGO
- **Do not import into** `ontology/ontology/gaming_ontology_v1.ttl` directly.
- Create/extend alignment in `mappings/cgo_to_universal.ttl`:
  - `owl:equivalentClass` / `rdfs:subClassOf` where appropriate
  - property alignments (`owl:equivalentProperty`, domain/range bridges)
- Optionally mirror high-value CGO concepts into `ontology/universal/*` only when:
  - we need them for cross-source integration, and
  - we can support them with data mappings/adapters.


