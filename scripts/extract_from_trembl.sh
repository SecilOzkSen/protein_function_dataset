#!/bin/bash

# INPUT FOLDERS
TREMBL_FASTA="uniprot_trembl.fasta.gz"
ID_LIST="missing_from_swissprot.txt"
OUTPUT_FASTA="trembl_subset.fasta"
echo "Filtering $(wc -l < $ID_LIST) from TrEMBL FASTA..."

> "$OUTPUT_FASTA"

# SEARCHING IDS
while read -r ID; do
    zgrep -A1000 "$ID" "$TREMBL_FASTA" >> "$OUTPUT_FASTA"
done < "$ID_LIST"

# END
echo "Finished. Filtered FASTA saved to $OUTPUT_FASTA."
