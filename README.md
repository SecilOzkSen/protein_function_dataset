# Protein Function Prediction Dataset Preparation

This repository contains scripts and processing steps to prepare a high-confidence dataset for training protein function prediction models. The dataset integrates sequence and annotation data from UniProt (Swiss-Prot, TrEMBL), GOA, and CAFA5, and includes semantic information from the Gene Ontology (GO) structure.

---

## Objective

To prepare a multi-label dataset with:

- Protein sequences (Swiss-Prot + TrEMBL)
- GO term annotations (strong evidence only: EXP, IDA, IPI, etc.)
- GO term definitions and ontology structure (from `go-basic.obo`)
- Optional inclusion of CAFA5 benchmark sequences

---

## Required Input Files

| File | Description |
|------|-------------|
| `uniprot_sprot.fasta.gz` | Full Swiss-Prot FASTA from UniProt |
| `uniprot_trembl.fasta.gz` or `trembl_subset.fasta` | TrEMBL sequences (manually downloaded and filtered) |
| `goa_uniprot_all.gaf.gz` | GOA annotations file |
| `cafa_train_sequences.fasta` | (Optional) CAFA5 training sequences |
| `go-basic.obo` | Gene Ontology definitions and DAG structure |

---

## Note on TrEMBL

Due to its large size (~100 GB), the full TrEMBL FASTA file must be downloaded manually:

```bash
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/uniprot_trembl.fasta.gz
```

After download, use the following script or shell pipeline to extract only the needed subset:

### Bash Script:
`extract_from_trembl.sh`

### Python Alternative:
`filter_by_trembl_id.py`

Both scripts take `missing_from_swissprot.txt` as input.

---

## Dataset Preparation Pipeline

Run the following scripts **in order**:

1. Download required data (Swiss-Prot and GOA):
```bash
python download_data.py
```

2. Extract CAFA test protein IDs:
```bash
python extract_test_ids.py
```

3. Parse GOA annotations and filter by evidence code and test set:
```bash
python parse_goa.py
```

4. Match CAFA training proteins with GOA annotations:
```bash
python parse_cafa_train.py
```

5. Check which GOA proteins are present in Swiss-Prot:
```bash
python check_goa_in_swissprot.py
```

6. Filter TrEMBL using missing IDs from Swiss-Prot:
```bash
python filter_trembl_by_id.py
# or run extract_from_trembl.sh manually
```

7. Extract matching sequences from Swiss-Prot:
```bash
python extract_swissprot_sequences_from_goa.py
```

8. Combine Swiss-Prot, TrEMBL, and CAFA sequences into final `.pkl` files:
```bash
python parse_fasta.py
```

9. Parse GO term definitions and relationships from OBO file:
```bash
python go_basic_obo_parser.py
```

10. Analyze GO term frequency and separate rare/common terms:
```bash
python analyze_go_term_frequency.py
```

---

## Final Output Files (for downstream model training)

| File | Description |
|------|-------------|
| `sequences_full.pkl` | Protein ID → amino acid sequence (GOA + CAFA) |
| `goa_plus_cafa.pkl` | Protein ID → list of GO terms |
| `go_terms.pkl` | GO ID → name, definition, namespace, and parent GO terms |
| `go_term_frequency.pkl` | GO ID → protein count |
| `rare_go_terms.pkl` | GO terms with <20 associated proteins |
| `common_go_terms.pkl` | GO terms with ≥100 associated proteins |

---

## Notes

- All annotations are filtered to include only strong experimental evidence (EXP, IDA, IPI, etc.).
- CAFA test proteins are excluded from training.
- TrEMBL full file must be manually downloaded and filtered.
- Scripts are Python 3.5+ compatible.

---
