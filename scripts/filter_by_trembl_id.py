import gzip

# Input and output file paths
trembl_path = "uniprot_trembl.fasta.gz"
id_list_path = "missing_from_swissprot.txt"
output_path = "trembl_subset.fasta"

# Load target protein IDs from text file
with open(id_list_path) as f:
    wanted_ids = set(line.strip() for line in f if line.strip())

print("Loaded {} protein IDs.".format(len(wanted_ids)))

# Stream through the gzipped FASTA file and write matching sequences
with gzip.open(trembl_path, "rt") as infile, open(output_path, "w") as outfile:
    write_flag = False
    current_id = None
    found = 0

    for line in infile:
        if line.startswith(">"):
            # Extract UniProt ID depending on header format
            if "|" in line:
                parts = line.split("|")
                if len(parts) > 1:
                    current_id = parts[1].strip()
                else:
                    current_id = line[1:].split()[0]
            else:
                current_id = line[1:].split()[0]

            if current_id in wanted_ids:
                write_flag = True
                found += 1
                outfile.write(line)
            else:
                write_flag = False
        elif write_flag:
            outfile.write(line)

print("Finished filtering. {} sequences written to {}.".format(found, output_path))

