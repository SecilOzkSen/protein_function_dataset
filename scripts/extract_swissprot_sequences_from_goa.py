import gzip
import pickle
import pandas as pd
from config import (UNIPROT_SPROT_PATH,
                    GOA_PARSED_FILE,
                    SWISSPROT_FILTERED_SEQUENCES)

def extract_uniprot_sequences_from_goa():
    with open(GOA_PARSED_FILE, "rb") as f:
        data = pickle.load(f)

    goa_ids = set(data.keys())
    print(f"Loaded {len(goa_ids)} GOA protein IDs from {GOA_PARSED_FILE.name}")

    #Filter swissprot FASTA
    with gzip.open(UNIPROT_SPROT_PATH, "rt") as infile, open(SWISSPROT_FILTERED_SEQUENCES, "w") as outfile:
        write_flag = False
        current_id = None
        matched = 0
        for line in infile:
            if line.startswith(">"):
                # then parse uniprot id
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) > 1:
                        current_id = parts[1].strip()
                    else:
                        current_id = line[1:].split()[0]
                else:
                    current_id = line[1:].split()[0]
                if current_id in goa_ids:
                    write_flag = True
                    matched += 1
                    outfile.write(line)
                else:
                    write_flag = False
            elif write_flag:
                outfile.write(line)

    print(f"Done. {matched} Swissprot sequences written to {SWISSPROT_FILTERED_SEQUENCES.name}")

if __name__ == '__main__':
    extract_uniprot_sequences_from_goa()

