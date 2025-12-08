#!/usr/bin/env python3
"""
Validate Extensibility

Validates that extension mechanisms work correctly (video, cross-game, human behavior).

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

import sys
from pathlib import Path
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL


def load_ontology(file_path: Path) -> Graph:
    """Load an ontology file into an RDF graph."""
    g = Graph()
    try:
        g.parse(str(file_path), format="turtle")
        return g
    except Exception as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        return None


def validate_extension(extension_path: Path, base_ontology_path: Path, extension_name: str) -> bool:
    """Validate that an extension properly extends the base ontology."""
    extension_graph = load_ontology(extension_path)
    base_graph = load_ontology(base_ontology_path)
    
    if extension_graph is None or base_graph is None:
        print(f"❌ Failed to load ontologies for {extension_name}")
        return False
    
    # Check that extension imports base ontology
    imports_found = False
    for s, p, o in extension_graph.triples((None, OWL.imports, None)):
        if str(base_ontology_path) in str(o) or extension_name in str(o):
            imports_found = True
            break
    
    if not imports_found:
        print(f"⚠️  {extension_name} may not properly import base ontology")
    
    # Check that extension has classes that extend base classes
    extension_classes = []
    base_classes = []
    
    for s, p, o in extension_graph.triples((None, RDFS.subClassOf, None)):
        extension_classes.append((str(s), str(o)))
    
    for s, p, o in base_graph.triples((None, RDF.type, OWL.Class)):
        base_classes.append(str(s))
    for s, p, o in base_graph.triples((None, RDF.type, RDFS.Class)):
        base_classes.append(str(s))
    
    valid_extensions = 0
    for ext_class, base_class in extension_classes:
        if base_class in base_classes:
            valid_extensions += 1
    
    print(f"{extension_name}:")
    print(f"  Classes extending base: {valid_extensions}/{len(extension_classes)}")
    
    return valid_extensions > 0


def validate_extensibility():
    """Validate all extension mechanisms."""
    base_path = Path(__file__).parent.parent
    
    print("Extensibility Validation")
    print("=" * 60)
    print()
    
    # Universal foundation
    universal_foundation = base_path / "universal" / "human_behavior_foundation.ttl"
    
    # Video extension
    video_extension = base_path / "extensions" / "video_playthrough_extension.ttl"
    video_valid = validate_extension(
        video_extension,
        universal_foundation,
        "Video Extension"
    )
    print()
    
    # Cross-game extension
    cross_game_extension = base_path / "extensions" / "cross_game_extension.ttl"
    gaming_foundation = base_path / "universal" / "gaming_foundation_v1.ttl"
    cross_game_valid = validate_extension(
        cross_game_extension,
        gaming_foundation,
        "Cross-Game Extension"
    )
    print()
    
    # Human behavior extension
    human_behavior_extension = base_path / "extensions" / "human_behavior_extension.ttl"
    human_behavior_valid = validate_extension(
        human_behavior_extension,
        universal_foundation,
        "Human Behavior Extension"
    )
    print()
    
    # Overall validation
    if video_valid and cross_game_valid and human_behavior_valid:
        print("✅ All extensions properly extend base ontologies")
        return 0
    else:
        print("⚠️  Some extensions may have issues")
        return 1


if __name__ == "__main__":
    sys.exit(validate_extensibility())

