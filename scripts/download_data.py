import os
import urllib.request
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")

os.makedirs(DATA_DIR, exist_ok=True)

# The files to be downloaded:
files_to_download = {
    # 1. GO Annotations (maps UniProt protein IDs to GO terms; main label source)
    "goa_uniprot_all.gaf.gz": {
        "url": "ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz", #server
        "description": "GOA (Gene Ontology Annotation) dataset — maps UniProt protein IDs to GO terms. Primary source of functional labels."
    },

    # 2. GO Ontology (contains GO term definitions and hierarchical relationships)
    "go-basic.obo": {
        "url": "http://purl.obolibrary.org/obo/go/go-basic.obo",
        "description": "Gene Ontology DAG file — contains GO term definitions and parent–child relationships. Used by the GO encoder."
    },

    # 3. Protein sequences (used to retrieve amino acid sequences for UniProt IDs)
    "uniprot_sprot.fasta.gz": {
        "url": "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz",
        "description": "UniProtKB/Swiss-Prot FASTA — provides amino acid sequences for UniProt IDs referenced in the GOA dataset."
    }
}

def download_file(name, url):
    file_path = os.path.join(DATA_DIR, name)
    if os.path.exists(file_path):
        print(f"{name} already exists, skipping.")
        return
    print(f"Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name} : {e}")

def download_cafa5_dataset():
    print("\nDownloading CAFA5 dataset from Kaggle (as zip)...")
    try:
        api = KaggleApi()
        api.authenticate()

        zip_path = os.path.join(DATA_DIR, "cafa-5-protein-function-prediction.zip")
        cafa5_dir = os.path.join(DATA_DIR, "cafa5")
        os.makedirs(cafa5_dir, exist_ok=True)

        # ZIP zaten varsa atla
        if os.path.exists(zip_path):
            print("✓ CAFA5 zip file already exists, skipping download.")
        else:
            api.competition_download_files(
                "cafa-5-protein-function-prediction",
                path=DATA_DIR,
                quiet=False
            )
            print("CAFA5 zip downloaded.")

        # ZIP varsa içeriğini aç
        print("📂 Extracting CAFA5 zip...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(cafa5_dir)
        print(f"Extracted to {cafa5_dir}")

        # Optional: ZIP dosyasını silmek istersen
        # os.remove(zip_path)

    except Exception as e:
        print(f"Failed to download CAFA5 dataset: {e}")
        print("Tip: Make sure your kaggle.json is located at ~/.kaggle/kaggle.json")

if __name__ == '__main__':
    print(f"Downloading datasets to {DATA_DIR}:\n")
    for name, meta_data in files_to_download.items():
        print(f"----- {name} ------")
        print(f"Description: {meta_data['description']} \n")
        download_file(name, meta_data['url'])
        print()

    download_cafa5_dataset()





