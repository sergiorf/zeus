import os
import requests

BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-06/"
OUTPUT_DIR = "data/raw"

FILES = [
    "Cnaes.zip",
    "Empresas0.zip", "Empresas1.zip", "Empresas2.zip", "Empresas3.zip", "Empresas4.zip",
    "Empresas5.zip", "Empresas6.zip", "Empresas7.zip", "Empresas8.zip", "Empresas9.zip",
    "Estabelecimentos0.zip", "Estabelecimentos1.zip", "Estabelecimentos2.zip", "Estabelecimentos3.zip",
    "Estabelecimentos4.zip", "Estabelecimentos5.zip", "Estabelecimentos6.zip",
    "Estabelecimentos7.zip", "Estabelecimentos8.zip", "Estabelecimentos9.zip",
    "Motivos.zip", "Municipios.zip", "Naturezas.zip", "Paises.zip", "Qualificacoes.zip",
    "Simples.zip",
    "Socios0.zip", "Socios1.zip", "Socios2.zip", "Socios3.zip", "Socios4.zip",
    "Socios5.zip", "Socios6.zip", "Socios7.zip", "Socios8.zip", "Socios9.zip",
]

def get_remote_size(url):
    """Returns the content length of the file in bytes (int) or None if not found."""
    try:
        response = requests.head(url)
        if response.status_code == 200 and 'Content-Length' in response.headers:
            return int(response.headers['Content-Length'])
    except requests.RequestException:
        pass
    return None

def download_file(filename):
    url = BASE_URL + filename
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    remote_size = get_remote_size(url)
    local_size = os.path.getsize(path) if os.path.exists(path) else -1

    if remote_size is not None and local_size == remote_size:
        print(f"[✓] Já existe (tamanho OK): {filename}")
        return
        
    if os.path.exists(path):
        print(f"[↻] Tamanho diferente, reiniciando: {filename}")
        os.remove(path)

    print(f"↓ Baixando: {filename}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
        print(f"[✓] Concluído: {filename} ({downloaded / 1024**2:.2f} MB)")
    except Exception as e:
        print(f"[!] Erro durante download de {filename}: {e}")
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    for file in FILES:
        download_file(file)
