import os
import json
import pickle
from config import (GO_BASIC,
                    GO_BASIC_PKL,
                    GO_BASIC_JSON)

ALLOWED_REL = {
    "is_a", "part_of", "regulates", "positively_regulates", "negatively_regulates",
    "occurs_in", "located_in", "capable_of", "capable_of_part_of"
}

def go_basic_obo_parser():
    go_terms = {}
    with open(GO_BASIC, "r") as f:
        current_term = {}
        inside_term = False

        for line in f:
            line = line.strip()
            if line == "[Term]":
                current_term = {}
                inside_term = True
                continue
            if line == "" and inside_term:
                if "id" in current_term:
                    go_id = current_term["id"]
                    go_terms[go_id] = {
                        "name": current_term.get("name", ""),
                        "namespace": current_term.get("namespace", ""),
                        "definition": current_term.get("def", ""),
                        "is_a": current_term.get("is_a", []),
                        "part_of": current_term.get("part_of", [])
                    }
                    inside_term = False
                    continue
            if inside_term:
                if line.startswith("id"):
                    current_term["id"] = line.split("id:")[1].strip()
                elif line.startswith("name:"):
                    current_term["name"] = line.split("name:")[1].strip()
                elif line.startswith("namespace:"):
                    current_term["namespace"] = line.split("namespace:")[1].strip()
                elif line.startswith("def"):
                    definition = line.split("def")[1].strip()
                    if "OBSOLETE" in definition.upper():
                        inside_term = False  # Skip entire term
                        current_term = {}
                        continue
                    current_term["def"] = definition
                elif line.startswith("is_a"):
                    parent_id = line.split("is_a:")[1].split("!")[0].strip()
                    current_term.setdefault("is_a", []).append(parent_id)
                elif line.startswith("relationship: part_of"):
                    parent_id = line.split("relationship: part_of")[1].split("!")[0].strip()
                    current_term.setdefault("part_of", []).append(parent_id)

    return go_terms

def save_go_terms(go_terms):
    with open(GO_BASIC_JSON, "w") as jf:
        json.dump(go_terms, jf, indent=2)
    with open(GO_BASIC_PKL, "wb") as pf:
        pickle.dump(go_terms, pf)

    print(f"Saved {len(go_terms)} GO terms to:")
    print(f"* JSON: {GO_BASIC_JSON.name}")
    print(f"* PICKLE: {GO_BASIC_PKL.name}")

if __name__ == "__main__":
    go_terms = go_basic_obo_parser()
    save_go_terms(go_terms)

