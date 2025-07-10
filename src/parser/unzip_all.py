import os
import zipfile

RAW_DIR = "data/raw"
UNZIP_DIR = "data/unzipped"

def unzip_all():
    os.makedirs(UNZIP_DIR, exist_ok=True)

    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith(".zip"):
            zip_path = os.path.join(RAW_DIR, filename)
            dest_path = os.path.join(UNZIP_DIR, filename.replace(".zip", ""))

            if os.path.exists(dest_path):
                print(f"[✓] Já extraído: {filename}")
                continue

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(UNZIP_DIR)
                print(f"[↓] Extraído: {filename}")
            except zipfile.BadZipFile:
                print(f"[!] Arquivo ZIP corrompido: {filename}")
            except Exception as e:
                print(f"[!] Erro ao extrair {filename}: {e}")

if __name__ == "__main__":
    unzip_all()
