import pickle
from collections import defaultdict
from config import (CAFA_TRAIN_TERMS,
                    TEST_IDS_PKL,
                    GOA_PARSED_FILE,
                    CAFA_PARSED_PKL,
                    FULL_DATASET_PKL)

def parse_cafa_train():
    # Load Test IDs
    with open(TEST_IDS_PKL, "rb") as f:
        test_ids = pickle.load(f)
    # Load Protein - GO mappings
    with open(GOA_PARSED_FILE, "rb") as f:
        goa_dict = pickle.load(f)
    goa_proteins = set(goa_dict.keys())

    # Parse cafa train_terms.tsv
    cafa_dict = defaultdict(set)
    with open(CAFA_TRAIN_TERMS, "r") as f:
        next(f) # Skip Header
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            prot_id = parts[0]
            go_term = parts[1]
            if prot_id in test_ids or prot_id in goa_proteins:
                continue
            cafa_dict[prot_id].add(go_term)

    with open(CAFA_PARSED_PKL, "wb") as f:
        pickle.dump(dict(cafa_dict), f)
    print(f"Filtered CAFA {len(cafa_dict)} proteins saved to {CAFA_PARSED_PKL.name}")

    # Merging CAFA GOA + CAFA into one dict
    full_dict = defaultdict(set)
    for pid, gos in goa_dict.items():
        full_dict[pid].update(gos)
    for pid, gos in cafa_dict.items():
        full_dict[pid].update(gos)

    # Save full dict
    with open(FULL_DATASET_PKL, "wb") as f:
        pickle.dump(dict(full_dict), f)

    print(f"Full dataset merged has {len(full_dict)} proteins and it is saved to {FULL_DATASET_PKL.name}")

if __name__ == "__main__":
    parse_cafa_train()

