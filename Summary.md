# Protein Function Prediction - Full Dataset Preparation

---

## Objective

Prepare a high-confidence dataset for protein function prediction by extracting and filtering:

- GOA annotations with strong experimental evidence
- Swiss-Prot and TrEMBL protein sequences
- Optional CAFA sequences (carefully separated for validation/testing)
- Full GO term ontology and semantic structure

---

## Files Created or Used

| File Name | Description |
|-----------|-------------|
| `uniprot_sprot.fasta.gz` | Full Swiss-Prot dataset from UniProt (local) |
| `uniprot_trembl.fasta.gz` | Full TrEMBL dataset (downloaded via `wget` on server) |
| `swissprot_subset.fasta` | Swiss-Prot sequences matching GOA IDs |
| `missing_from_swissprot.txt` | GOA proteins missing from Swiss-Prot |
| `trembl_subset.fasta` | 53,019 TrEMBL sequences filtered by ID |
| `goa_parsed.pkl` | GOA protein → GO term mapping (strong evidence only, test proteins excluded) |
| `cafa_test_ids.pkl` | Extracted CAFA test protein IDs |
| `cafa_filtered.pkl` | CAFA training proteins with matched GO terms |
| `goa_plus_cafa.pkl` | Combined GOA + CAFA annotation dictionary |
| `sequences_goa_only.pkl` | Sequences for GOA-only proteins |
| `sequences_full.pkl` | Sequences for GOA + CAFA proteins |
| `go-basic.obo` | Full Gene Ontology DAG file |
| `go_terms.pkl` / `.json` | Parsed GO term name, definition, namespace, parents |
| `go_term_frequency.pkl` / `.tsv` | GO term frequency statistics |
| `rare_go_terms.pkl` | GO terms with <20 proteins (few-shot set) |
| `midfreq_go_terms.pkl` | GO terms with 20–99 proteins |
| `common_go_terms.pkl` | GO terms with ≥100 proteins (well-supported set) |

---

## Scripts Developed

| Script | Description |
|--------|-------------|
| `download_data.py` | Downloads GOA and Swiss-Prot files (TrEMBL is handled manually) |
| `extract_test_ids.py` | Extracts CAFA5 test protein IDs |
| `parse_goa.py` | Parses GOA and filters out test proteins; saves GO annotations |
| `parse_cafa_train.py` | Matches CAFA training proteins with GOA; merges optional training set |
| `check_goa_in_swissprot.py` | Verifies GOA proteins in Swiss-Prot FASTA |
| `filter_trembl_by_id.py` | Extracts TrEMBL subset FASTA based on missing Swiss-Prot IDs |
| `extract_swissprot_sequences_from_goa.py` | Extracts Swiss-Prot subset FASTA from GOA protein IDs |
| `parse_fasta.py` | Loads Swiss-Prot + TrEMBL + CAFA FASTA and extracts final sequences into `.pkl` |
| `go_basic_obo_parser.py` | Parses `go-basic.obo` into structured GO term dicts |
| `analyze_go_term_frequency.py` | Computes GO term frequencies, and separates rare / common term sets |

---

## Final Files for Model Training

The following files will be used directly for model training and evaluation:

| File | Purpose |
|------|---------|
| `sequences_full.pkl` | Amino acid sequences for proteins (GOA + CAFA); input to embedding models (e.g., ESM3b) |
| `goa_plus_cafa.pkl` | Protein → [GO terms] multi-label mapping (strong evidence only) |
| `go_terms.pkl` | GO term metadata including name, definition, namespace, and parent GO IDs |
| `go_term_frequency.pkl` | Frequency dictionary for GO terms (used to stratify or filter classes) |
| `rare_go_terms.pkl` | GO terms with <20 proteins (for few-shot strategies or exclusion) |
| `common_go_terms.pkl` | GO terms with ≥100 proteins (for baseline evaluation or strong supervision) |

These files represent the complete input required for:
- Embedding extraction
- Label assignment
- GO term encoder construction
- Few-shot evaluation


---

## Key Outcomes

- Strong-evidence–filtered GO annotations prepared (EXP, IDA, IPI, etc.)
- Swiss-Prot and TrEMBL subset sequences successfully aligned with GOA
- CAFA benchmark proteins separated to avoid leakage
- GO definitions and `is_a` relationships extracted from `.obo`
- Rare/common GO term sets extracted to support few-shot / balanced training
- Final training-ready sequence dictionaries saved for downstream embedding

---

## Status: Dataset Preparation Complete
The dataset is now ready for downstream usage in protein language model embedding and GO alignment modeling.

---
