from config import CAFA5_TEST_FASTA, TEST_IDS_PKL
import pickle
def extract_test_ids(fasta_path=CAFA5_TEST_FASTA, output_path=TEST_IDS_PKL):
    test_ids = set()
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                uniprot_id = line.strip().split("\t")[0][1:]
                test_ids.add(uniprot_id)
    with open(output_path, 'wb') as f:
        pickle.dump(test_ids, f)

    print(f"Extracted {len(test_ids)} test protein IDs from {fasta_path}")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    extract_test_ids()