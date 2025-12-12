# Video Game Ontology (VGO) – External Source Notes

**Discovered via**: Linked Open Vocabularies entry for VGO (Video Game Ontology).  
**Goal**: Add VGO as a reference/source ontology for game metadata (genres, platforms, etc.) and align it to `ug:` where helpful.

## Candidate source links

- LOV portal entry: `https://w3c.lovportal.lirmm.fr/ontologies/VGO`
- Reported canonical IRI: `http://purl.org/net/VideoGameOntology`
 - Downloaded into this repo: `sources/vgo/vgo.ttl`

## License note

The ontology declares a Creative Commons license:

- `http://creativecommons.org/licenses/by-nc-sa/2.0/`

This is **non-commercial** (NC). We can still use it as a *research/reference source* and incorporate *ideas* into our universal ontology, but we should be careful about **shipping** VGO content as part of a commercial “flagship” distribution.

## How we should incorporate it

- Treat VGO as a **metadata ontology** (game catalog / game description), not gameplay telemetry.
- Create a mapping file:
  - `mappings/vgo_to_universal.ttl`
  - Map VGO’s `VideoGame` / `Game` concepts to `ug:Game`
  - Map VGO genre/platform vocabulary into `extensions/cross_game_extension.ttl` (`GameGenre`) or directly into `ug:` if we decide it belongs in the core.

## Status

- ✅ Downloaded and normalized to Turtle: `sources/vgo/vgo.ttl`


