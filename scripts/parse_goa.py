import gzip
import pickle
from collections import defaultdict
from config import GOA_GAF_FILE, GOA_PARSED_FILE, VALID_EVIDENCE_CODES, TEST_IDS_PKL

def parse_goa():
    # Load test protein ids:
    with open(TEST_IDS_PKL, "rb") as f:
        test_ids = pickle.load(f)

    protein2go = defaultdict(set)

    with gzip.open(GOA_GAF_FILE, "rt") as f:
        for line in f:
            if line.startswith("!"): #Commented line
                continue
            parts = line.strip().split("\t")
            if len(parts) < 7:
                continue
            protein_id = parts[1]
            go_term = parts[4]
            evidence = parts[6]

            if evidence not in VALID_EVIDENCE_CODES:
                continue
            if protein_id in test_ids:
                continue
            protein2go[protein_id].add(go_term)
    with open(GOA_PARSED_FILE, "wb") as f:
        pickle.dump(dict(protein2go), f)

    print(f"Parsed {len(protein2go)} proteins with GO annotations.")
    print(f"Saved to {GOA_PARSED_FILE}")

if __name__ == "__main__":
    parse_goa()
