from config import (
    UNIPROT_SPROT_PATH,
    GOA_PARSED_FILE,
    FULL_DATASET_PKL,
    SEQUENCES_GOA_ONLY_PKL,
    SEQUENCES_FULL_PKL,
    TREMBL_PARSED,
    CAFA_TRAIN_FASTA_PATH
)
import pickle
import gzip

def load_target_ids(path):
    with open(path, "rb") as f:
        d = pickle.load(f)
    return set(d.keys())

def parse_fasta_file(path, compressed=False):
    open_func = gzip.open if compressed else open
    sequences = {}
    with open_func(path, "rt") as f:
        current_id = None
        current_seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_id:
                    sequences[current_id] = "".join(current_seq)
                try:
                    current_id = line[1:].split()[0].split("|")[1]
                except IndexError:
                    current_id = None
                current_seq = []
            elif current_id:
                current_seq.append(line)
        if current_id:
            sequences[current_id] = "".join(current_seq)
    return sequences

def parse_fasta():
    goa_ids = load_target_ids(GOA_PARSED_FILE)
    full_ids = load_target_ids(FULL_DATASET_PKL)

    print(f"Total GOA ids: {len(goa_ids)}")
    print(f"Total GOA+CAFA ids: {len(full_ids)}")

    master_sequences = {}

    print("Parsing Swiss-Prot...")
    master_sequences.update(parse_fasta_file(UNIPROT_SPROT_PATH, compressed=True))

    try:
        print("Parsing TrEMBL (trembl_subset)...")
        master_sequences.update(parse_fasta_file(TREMBL_PARSED, compressed=False))
    except FileNotFoundError:
        print("TrEMBL subset file not found. Skipping...")

    try:
        print("Parsing CAFA train_sequences.fasta...")
        master_sequences.update(parse_fasta_file(CAFA_TRAIN_FASTA_PATH, compressed=False))
    except FileNotFoundError:
        print("CAFA train_sequences.fasta not found. Skipping...")

    print(f"Total unique sequences parsed: {len(master_sequences)}")

    sequences_goa = {pid: seq for pid, seq in master_sequences.items() if pid in goa_ids}
    sequences_full = {pid: seq for pid, seq in master_sequences.items() if pid in full_ids}

    with open(SEQUENCES_GOA_ONLY_PKL, "wb") as f:
        pickle.dump(sequences_goa, f)
    print(f"Saved GOA sequences : {len(sequences_goa)} to {SEQUENCES_GOA_ONLY_PKL.name}")

    with open(SEQUENCES_FULL_PKL, "wb") as f:
        pickle.dump(sequences_full, f)
    print(f"Saved full GOA + CAFA sequences : {len(sequences_full)} to {SEQUENCES_FULL_PKL.name}")

if __name__ == '__main__':
    parse_fasta()
