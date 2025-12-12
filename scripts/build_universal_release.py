"""
Build a single-file "flagship" Universal Gaming Ontology release TTL.

Goal:
- Absorb useful parts of legacy core ontology (core#) into the universal gaming namespace (ug#)
- Keep legacy IRIs available as deprecated stubs + equivalence axioms (for migration)
- Output a single flattened TTL that ontology specialists can open in Protégé

Inputs (defaults assume repo layout):
- ontology/ontology/gaming_ontology_v1.ttl (legacy)
- ontology/universal/human_behavior_foundation.ttl
- ontology/universal/gaming_foundation_v1.ttl

Outputs:
- ontology/universal/worldmodeldata_universal_gaming_ontology_v1.ttl (canonical release artifact)
- ontology/ontology/worldmodeldata_universal_gaming_ontology_v1.ttl (docker-mounted copy)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional, Set, Tuple

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.namespace import XSD, SKOS, DC


CORE = Namespace("http://ontology.gaming.network/core#")
UG = Namespace("http://ontology.gaming.network/universal/gaming#")
UB = Namespace("http://ontology.gaming.network/universal/human_behavior#")


STRUCTURAL_PREDICATES = {
    RDF.type,
    RDFS.subClassOf,
    RDFS.domain,
    RDFS.range,
    OWL.equivalentClass,
    OWL.equivalentProperty,
    OWL.inverseOf,
}


@dataclass(frozen=True)
class BuildConfig:
    repo_root: Path
    core_ttl: Path
    universal_hb_ttl: Path
    universal_gaming_ttl: Path
    out_canonical: Path
    out_docker_copy: Path


def _is_core_uri(u: URIRef) -> bool:
    return isinstance(u, URIRef) and str(u).startswith(str(CORE))


def _local_name(u: URIRef) -> str:
    s = str(u)
    if "#" in s:
        return s.rsplit("#", 1)[1]
    return s.rsplit("/", 1)[-1]


def _is_testish(local: str) -> bool:
    l = local.lower()
    return l.startswith("test") or "test" in l


def _load(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def _collect_typed_subjects(g: Graph) -> Set[URIRef]:
    """Collect core subjects that define ontology terms (classes/properties/annotationProperties)."""
    wanted_types = {
        OWL.Class,
        OWL.ObjectProperty,
        OWL.DatatypeProperty,
        OWL.AnnotationProperty,
    }
    out: Set[URIRef] = set()
    for t in wanted_types:
        for s in g.subjects(RDF.type, t):
            if _is_core_uri(s):
                out.add(s)  # type: ignore[arg-type]
    return out


def _seed_explicit_equivalences(core_graph: Graph) -> Dict[URIRef, URIRef]:
    """
    If legacy already has owl:equivalentClass/Property to UG/UB, respect that mapping.
    """
    mapping: Dict[URIRef, URIRef] = {}
    for pred in (OWL.equivalentClass, OWL.equivalentProperty):
        for s, _, o in core_graph.triples((None, pred, None)):
            if isinstance(s, URIRef) and isinstance(o, URIRef) and _is_core_uri(s):
                if str(o).startswith(str(UG)) or str(o).startswith(str(UB)):
                    mapping[s] = o
    return mapping


def _resolve_target(
    core_entity: URIRef,
    explicit_map: Dict[URIRef, URIRef],
    existing_ug_ub_locals: Set[str],
) -> URIRef:
    if core_entity in explicit_map:
        return explicit_map[core_entity]

    local = _local_name(core_entity)
    # If universal already has a term with same local name, prefer that.
    if local in existing_ug_ub_locals:
        # Prefer UG over UB unless UB clearly contains it (we can't always tell here).
        # Heuristic: if UB already has the local name, use UB; else UG.
        ub_candidate = URIRef(str(UB) + local)
        if local in existing_ug_ub_locals and (str(ub_candidate).startswith(str(UB))):
            # We still need to check if it actually exists; caller provides locals set only.
            # We'll use a conservative default: UG.
            pass
    return URIRef(str(UG) + local)


def _rewrite_node(node, core_to_target: Dict[URIRef, URIRef]):
    if isinstance(node, URIRef) and _is_core_uri(node) and node in core_to_target:
        return core_to_target[node]
    return node


def _copy_term_triples(
    core_graph: Graph,
    out_graph: Graph,
    core_entity: URIRef,
    target_entity: URIRef,
    core_to_target: Dict[URIRef, URIRef],
) -> None:
    """
    Copy descriptive + structural triples for a legacy term onto the target universal term,
    rewriting core URIs that we mapped.
    """
    for s, p, o in core_graph.triples((core_entity, None, None)):
        # Skip the legacy equivalence triples; we'll add normalized ones ourselves.
        if p in (OWL.equivalentClass, OWL.equivalentProperty):
            continue

        # Avoid copying the legacy ontology header statements onto the term
        if s == URIRef("http://ontology.gaming.network/core") and p == RDF.type and o == OWL.Ontology:
            continue

        new_s = target_entity
        new_p = _rewrite_node(p, core_to_target)
        new_o = _rewrite_node(o, core_to_target)

        # Avoid adding duplicates (rdflib Graph handles this, but keep logic explicit)
        out_graph.add((new_s, new_p, new_o))


def _add_deprecated_stub(
    out_graph: Graph,
    core_entity: URIRef,
    target_entity: URIRef,
    core_graph: Graph,
) -> None:
    """
    Keep the legacy IRI present in the release file as a deprecated stub,
    linked to the new universal IRI.
    """
    # Preserve rdf:type for the legacy entity (Class/Property) so tooling still "sees" it.
    for _, _, t in core_graph.triples((core_entity, RDF.type, None)):
        out_graph.add((core_entity, RDF.type, t))

    out_graph.add((core_entity, OWL.deprecated, Literal(True, datatype=XSD.boolean)))
    out_graph.add(
        (
            core_entity,
            RDFS.comment,
            Literal(
                f"DEPRECATED legacy IRI. Use '{target_entity}' instead.",
                lang="en",
            ),
        )
    )

    # Add equivalence links
    # Decide whether it's class or property based on legacy rdf:type
    is_class = (core_entity, RDF.type, OWL.Class) in core_graph
    if is_class:
        out_graph.add((core_entity, OWL.equivalentClass, target_entity))
    else:
        out_graph.add((core_entity, OWL.equivalentProperty, target_entity))


def build_release(cfg: BuildConfig) -> Tuple[Graph, Dict[str, int]]:
    core_g = _load(cfg.core_ttl)
    hb_g = _load(cfg.universal_hb_ttl)
    ug_g = _load(cfg.universal_gaming_ttl)

    out = Graph()
    out.namespace_manager.bind("core", CORE)
    out.namespace_manager.bind("ug", UG)
    out.namespace_manager.bind("ub", UB)
    out.namespace_manager.bind("owl", OWL)
    out.namespace_manager.bind("rdfs", RDFS)
    out.namespace_manager.bind("skos", SKOS)
    out.namespace_manager.bind("dc", DC)

    # Seed with foundations (flattened into one graph)
    for t in hb_g:
        out.add(t)
    for t in ug_g:
        out.add(t)

    existing_universal_locals: Set[str] = set()
    for s in out.subjects(None, None):
        if isinstance(s, URIRef):
            if str(s).startswith(str(UG)) or str(s).startswith(str(UB)):
                existing_universal_locals.add(_local_name(s))

    core_terms = _collect_typed_subjects(core_g)
    explicit_map = _seed_explicit_equivalences(core_g)

    core_to_target: Dict[URIRef, URIRef] = {}
    absorbed = 0
    skipped = 0

    for core_entity in sorted(core_terms, key=lambda u: str(u)):
        local = _local_name(core_entity)
        if _is_testish(local):
            skipped += 1
            continue

        target = _resolve_target(core_entity, explicit_map, existing_universal_locals)
        core_to_target[core_entity] = target

    # Ontology header for the release artifact
    release_iri = URIRef("http://ontology.gaming.network/universal/gaming_ontology")
    out.add((release_iri, RDF.type, OWL.Ontology))
    out.add((release_iri, DC.title, Literal("WorldModelData Universal Gaming Ontology v1", lang="en")))
    out.add((release_iri, DC.creator, Literal("WorldModelData")))
    out.add((release_iri, OWL.versionInfo, Literal("1.0.0")))
    out.add(
        (
            release_iri,
            RDFS.comment,
            Literal(
                "Flagship universal gaming ontology release. Flattened distribution containing the universal foundations plus absorbed legacy core semantics.",
                lang="en",
            ),
        )
    )
    out.add((release_iri, OWL.imports, URIRef("http://ontology.gaming.network/universal/human_behavior")))
    out.add((release_iri, OWL.imports, URIRef("http://ontology.gaming.network/universal/gaming")))

    # Absorb core term content into universal namespace + add deprecated stubs for legacy IRIs
    for core_entity, target_entity in core_to_target.items():
        _copy_term_triples(core_g, out, core_entity, target_entity, core_to_target)
        _add_deprecated_stub(out, core_entity, target_entity, core_g)
        absorbed += 1

    stats = {
        "triples_out": len(out),
        "core_terms_total": len(core_terms),
        "core_terms_absorbed": absorbed,
        "core_terms_skipped_testish": skipped,
    }
    return out, stats


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    cfg = BuildConfig(
        repo_root=repo_root,
        core_ttl=repo_root / "ontology" / "ontology" / "gaming_ontology_v1.ttl",
        universal_hb_ttl=repo_root / "ontology" / "universal" / "human_behavior_foundation.ttl",
        universal_gaming_ttl=repo_root / "ontology" / "universal" / "gaming_foundation_v1.ttl",
        out_canonical=repo_root / "ontology" / "universal" / "worldmodeldata_universal_gaming_ontology_v1.ttl",
        out_docker_copy=repo_root / "ontology" / "ontology" / "worldmodeldata_universal_gaming_ontology_v1.ttl",
    )

    out_graph, stats = build_release(cfg)
    cfg.out_canonical.parent.mkdir(parents=True, exist_ok=True)
    cfg.out_docker_copy.parent.mkdir(parents=True, exist_ok=True)

    ttl = out_graph.serialize(format="turtle")
    cfg.out_canonical.write_text(ttl, encoding="utf-8")
    cfg.out_docker_copy.write_text(ttl, encoding="utf-8")

    print("Wrote:")
    print(f"- {cfg.out_canonical}")
    print(f"- {cfg.out_docker_copy}")
    print("Stats:", stats)


if __name__ == "__main__":
    main()


