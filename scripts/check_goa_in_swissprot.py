import gzip
import pickle
from config import GOA_PARSED_FILE, UNIPROT_SPROT_PATH, MISSING_FROM_SWISSPROT

def load_goa_ids():
    with open(GOA_PARSED_FILE, "rb") as f:
        goa_dict = pickle.load(f)
    return set(goa_dict.keys())

def load_sprot_ids(fasta_path):
    ids = set()
    with gzip.open(fasta_path, "rt") as f:
        for line in f:
            if line.startswith(">"):
                try:
                    pid = line[1:].split()[0].split("|")[1]
                    ids.add(pid)
                except IndexError:
                    continue
    return ids

def check_overlap():
    goa_ids = load_goa_ids()
    print(f"GOA protein IDs: {len(goa_ids)}")

    sprot_ids = load_sprot_ids(UNIPROT_SPROT_PATH)
    print(f"Swiss-Prot protein IDs: {len(sprot_ids)}")

    in_swissprot = goa_ids & sprot_ids
    missing = goa_ids - sprot_ids

    print(f"Found in Swiss-Prot: {len(in_swissprot)}")
    print(f"Missing from Swiss-Prot: {len(missing)}")

    with open(MISSING_FROM_SWISSPROT, "w") as f:
        for pid in sorted(missing):
            f.write(pid + "\n")

if __name__ == "__main__":
    check_overlap()