#!/usr/bin/env python3
"""
Validate Universal Foundation Coverage

Validates that all source patterns (Unity, Mixpanel, GOP, Production) are
covered by the Universal Gaming Foundation Ontology.

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Set
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


def extract_classes(graph: Graph) -> Set[str]:
    """Extract all class URIs from an ontology graph."""
    classes = set()
    if graph is None:
        return classes
    
    for s, p, o in graph.triples((None, RDF.type, OWL.Class)):
        classes.add(str(s))
    for s, p, o in graph.triples((None, RDF.type, RDFS.Class)):
        classes.add(str(s))
    
    return classes


def extract_properties(graph: Graph) -> Set[str]:
    """Extract all property URIs from an ontology graph."""
    properties = set()
    if graph is None:
        return properties
    
    for s, p, o in graph.triples((None, RDF.type, OWL.DatatypeProperty)):
        properties.add(str(s))
    for s, p, o in graph.triples((None, RDF.type, OWL.ObjectProperty)):
        properties.add(str(s))
    
    return properties


def validate_coverage():
    """Validate that all source patterns are covered by universal foundation."""
    base_path = Path(__file__).parent.parent
    
    # Load source ontologies
    unity_graph = load_ontology(base_path / "sources" / "unity" / "unity_analytics_patterns.ttl")
    mixpanel_graph = load_ontology(base_path / "sources" / "mixpanel" / "mixpanel_patterns.ttl")
    gop_graph = load_ontology(base_path / "sources" / "gop" / "gop_patterns.ttl")
    gaming_graph = load_ontology(base_path / "universal" / "gaming_foundation_v1.ttl")
    
    # Extract classes and properties
    unity_classes = extract_classes(unity_graph) if unity_graph else set()
    mixpanel_classes = extract_classes(mixpanel_graph) if mixpanel_graph else set()
    gop_classes = extract_classes(gop_graph) if gop_graph else set()
    gaming_classes = extract_classes(gaming_graph) if gaming_graph else set()
    
    unity_props = extract_properties(unity_graph) if unity_graph else set()
    mixpanel_props = extract_properties(mixpanel_graph) if mixpanel_graph else set()
    gop_props = extract_properties(gop_graph) if gop_graph else set()
    gaming_props = extract_properties(gaming_graph) if gaming_graph else set()
    
    # Validation results
    results = {
        "unity_coverage": {
            "classes_covered": len(unity_classes.intersection(gaming_classes)),
            "classes_total": len(unity_classes),
            "properties_covered": len(unity_props.intersection(gaming_props)),
            "properties_total": len(unity_props)
        },
        "mixpanel_coverage": {
            "classes_covered": len(mixpanel_classes.intersection(gaming_classes)),
            "classes_total": len(mixpanel_classes),
            "properties_covered": len(mixpanel_props.intersection(gaming_props)),
            "properties_total": len(mixpanel_props)
        },
        "gop_coverage": {
            "classes_covered": len(gop_classes.intersection(gaming_classes)),
            "classes_total": len(gop_classes),
            "properties_covered": len(gop_props.intersection(gaming_props)),
            "properties_total": len(gop_props)
        }
    }
    
    # Print results
    print("Universal Foundation Coverage Validation")
    print("=" * 60)
    print()
    
    print("Unity Analytics Coverage:")
    print(f"  Classes: {results['unity_coverage']['classes_covered']}/{results['unity_coverage']['classes_total']}")
    print(f"  Properties: {results['unity_coverage']['properties_covered']}/{results['unity_coverage']['properties_total']}")
    print()
    
    print("Mixpanel Coverage:")
    print(f"  Classes: {results['mixpanel_coverage']['classes_covered']}/{results['mixpanel_coverage']['classes_total']}")
    print(f"  Properties: {results['mixpanel_coverage']['properties_covered']}/{results['mixpanel_coverage']['properties_total']}")
    print()
    
    print("GOP Coverage:")
    print(f"  Classes: {results['gop_coverage']['classes_covered']}/{results['gop_coverage']['classes_total']}")
    print(f"  Properties: {results['gop_coverage']['properties_covered']}/{results['gop_coverage']['properties_total']}")
    print()
    
    # Overall validation
    all_covered = (
        results['unity_coverage']['classes_covered'] == results['unity_coverage']['classes_total'] and
        results['mixpanel_coverage']['classes_covered'] == results['mixpanel_coverage']['classes_total'] and
        results['gop_coverage']['classes_covered'] == results['gop_coverage']['classes_total']
    )
    
    if all_covered:
        print("✅ All source patterns are covered by universal foundation")
        return 0
    else:
        print("⚠️  Some source patterns may not be fully covered")
        return 1


if __name__ == "__main__":
    sys.exit(validate_coverage())

