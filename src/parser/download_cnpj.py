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

def download_file(filename):
    url = BASE_URL + filename
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(path):
        print(f"[✓] Já existe: {filename}")
        return

    print(f"↓ Baixando: {filename}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"[✓] Concluído: {filename}")

if __name__ == "__main__":
    for file in FILES:
        try:
            download_file(file)
        except Exception as e:
            print(f"[!] Erro ao baixar {file}: {e}")
