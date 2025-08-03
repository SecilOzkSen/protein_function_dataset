import pickle
from scripts.config import (GOA_PARSED_FILE,
                            GO_TERM_COUNTS_PKL,
                            GO_TERM_COUNTS_TSV,
                            RARE_THRESHOLD,
                            MID_FREQ_THRESHOLD,
                            RARE_GO_TERMS_PKL,
                            MIDFREQ_GO_TERMS_PKL,
                            COMMON_GO_TERMS_PKL)
from collections import Counter
import pandas as pd

def analyse_go_term_frequency():
    with open(GOA_PARSED_FILE, "rb") as f:
        protein2go = pickle.load(f)

    go_counts = Counter(
        go_id for go_terms in protein2go.values()
        for go_id in go_terms
    )

    df = pd.DataFrame(go_counts.items(), columns=["GO_ID", "Protein_Count"])
    df.sort_values(by="Protein_Count", ascending=False, inplace=True)

    #Save
    df.to_csv(GO_TERM_COUNTS_TSV, sep="\t", index=False)
    with open(GO_TERM_COUNTS_PKL, "wb") as f:
        pickle.dump(go_counts, f)

        # Threshold-based term sets
        rare_terms = set(df[df["Protein_Count"] < RARE_THRESHOLD]["GO_ID"])
        midfreq_terms = set(df[(df["Protein_Count"] >= RARE_THRESHOLD) & (df["Protein_Count"] < MID_FREQ_THRESHOLD)]["GO_ID"])
        common_terms = set(df[df["Protein_Count"] >= MID_FREQ_THRESHOLD]["GO_ID"])

        with open(RARE_GO_TERMS_PKL, "wb") as f:
            pickle.dump(rare_terms, f)
        with open(MIDFREQ_GO_TERMS_PKL, "wb") as f:
            pickle.dump(midfreq_terms, f)
        with open(COMMON_GO_TERMS_PKL, "wb") as f:
            pickle.dump(common_terms, f)

        print(f"Total GO terms: {len(df)}")
        print(f"Saved frequency table to {GO_TERM_COUNTS_TSV.name}")
        print(f"Rare (<{RARE_THRESHOLD}): {len(rare_terms)}")
        print(f"Saved rare go terms to {RARE_GO_TERMS_PKL.name}")
        print(f"Mid ({RARE_THRESHOLD}–{MID_FREQ_THRESHOLD-1}): {len(midfreq_terms)}")
        print(f"Saved mid go terms to {MIDFREQ_GO_TERMS_PKL.name}")
        print(f"Common (≥{MID_FREQ_THRESHOLD}): {len(common_terms)}")
        print(f"Saved common go terms to {COMMON_GO_TERMS_PKL.name}")
        print(df.head(10))

if __name__ == "__main__":
    analyse_go_term_frequency()


