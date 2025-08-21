'''
Created by Secil Sen.
'''
from pathlib import Path

# project root path
ROOT_PATH = Path(__file__).resolve().parent.parent
# base data paths
DATA_PATH = ROOT_PATH / "data"
RAW_DATA_PATH = DATA_PATH / "raw"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
SEQUENCES_DATA_PATH = PROCESSED_DATA_PATH / "sequences"
ANALYSIS_DATA_PATH = DATA_PATH / "analysis"

# Raw Data Paths
CAFA5_TEST_FASTA = RAW_DATA_PATH / "cafa5" / "Test (Targets)" / "testsuperset.fasta"
GOA_GAF_FILE = RAW_DATA_PATH / "goa_uniprot_all.gaf.gz"
UNIPROT_SPROT_PATH = RAW_DATA_PATH / "uniprot_sprot.fasta.gz"
GO_BASIC = RAW_DATA_PATH / "go-basic.obo"
CAFA_TRAIN_TERMS = RAW_DATA_PATH / "cafa5" / "Train" / "train_terms.tsv"
UNIPROT_TREMBL_PATH = RAW_DATA_PATH / "uniprot_trembl.fasta.gz"
CAFA_TRAIN_FASTA_PATH = RAW_DATA_PATH / "cafa5" / "Train" / "train_sequences.fasta"

# Processed Output Paths (GOIDs) & (Ontology)
TEST_IDS_PKL = PROCESSED_DATA_PATH / "test_ids.pkl"
GOA_PARSED_FILE = PROCESSED_DATA_PATH / "goa_parsed.pkl"
CAFA_PARSED_PKL = PROCESSED_DATA_PATH / "cafa_filtered.pkl"
FULL_DATASET_PKL = PROCESSED_DATA_PATH / "goa_plus_cafa.pkl"
MISSING_FROM_SWISSPROT = PROCESSED_DATA_PATH / "missing_from_swissprot.txt"
# Ontology
GO_BASIC_JSON = PROCESSED_DATA_PATH / "go_basic_obo_terms_v2.json"
GO_BASIC_PKL = PROCESSED_DATA_PATH / "go_basic_obo_terms_v2.pkl"
GO_ZERO_SHOT_PKL = PROCESSED_DATA_PATH / "go_zero_shot.pkl"
GO_ZERO_SHOT_TSV = PROCESSED_DATA_PATH / "go_zero_shot.tsv"


# Processed Sequences
UNIPROT_FILTERED_SEQUENCES = SEQUENCES_DATA_PATH / "uniprot_filtered_sequences.pkl"
SEQUENCES_GOA_ONLY_PKL = SEQUENCES_DATA_PATH / "sequences_goa_only.pkl"
SEQUENCES_FULL_PKL = SEQUENCES_DATA_PATH / "sequences_full.pkl"
SWISSPROT_FILTERED_SEQUENCES = SEQUENCES_DATA_PATH / "swissprot_subset.fasta"
TREMBL_PARSED = SEQUENCES_DATA_PATH / "trembl_subset.fasta"


# Analysis
GO_TERM_COUNTS_TSV = ANALYSIS_DATA_PATH / "go_term_frequency.tsv"
GO_TERM_COUNTS_PKL = ANALYSIS_DATA_PATH / "go_term_frequency.pkl"
RARE_GO_TERMS_PKL = ANALYSIS_DATA_PATH / "rare_go_terms.pkl"
MIDFREQ_GO_TERMS_PKL = ANALYSIS_DATA_PATH / "midfreq_go_terms.pkl"
COMMON_GO_TERMS_PKL = ANALYSIS_DATA_PATH / "common_go_terms.pkl"

# === Filters & Settings ===
VALID_EVIDENCE_CODES = {"EXP", "IDA", "IPI", "IMP", "IGI", "IEP"}  # strong evidence
MAX_SEQUENCE_LENGTH = 1500
# Rare go terms analysis
RARE_THRESHOLD = 20
MID_FREQ_THRESHOLD = 100