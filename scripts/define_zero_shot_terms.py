
import pandas as pd
import pickle
from scripts.config import (GO_BASIC_PKL, FULL_DATASET_PKL, GO_ZERO_SHOT_PKL, GO_ZERO_SHOT_TSV)

def load_go_terms():
    """
    Expect either a pickle produced by your OBO parser (GO_ID keys) or a TSV with a GO_ID column.
    :return: GO_ID
    """

    with open(GO_BASIC_PKL, 'rb') as f:
        obj = pickle.load(f)
    return set(obj.keys())


def load_train_terms():
    """
    Expect a mapping ProteinID -> list[GO_ID] (pkl) or a TSV with columns [ProteinID, GO_ID].
    :return: set of GO_ID observed in training.
    """
    with open(FULL_DATASET_PKL, 'rb') as f:
        mapping = pickle.load(f)
    terms = set()
    for lst in mapping.values():
        terms.update(map(str, lst))
    return terms

def main():

    all_terms = load_go_terms()
    train_terms = load_train_terms()

    zero_shot = sorted(all_terms - train_terms)

    # Save outputs
    with open(GO_ZERO_SHOT_PKL, 'wb') as f:
        pickle.dump(zero_shot, f)
    pd.DataFrame({"GO_ID": zero_shot}).to_csv(GO_ZERO_SHOT_TSV, sep="\t", index=False)

    print(f"Total ontology terms: {len(all_terms)}")
    print(f"Seen in training:     {len(train_terms)}")
    print(f"Zero-shot terms:      {len(zero_shot)}")
    print(f"Saved: {GO_ZERO_SHOT_PKL} and {GO_ZERO_SHOT_TSV}")

if __name__ == "__main__":
    main()
