import os
import psycopg2
import tempfile

UNZIP_DIR = "data/unzipped"

# Tabelas e colunas definidas conforme o schema PostgreSQL
TABLES = {
    "empresas": [
        "cnpj_basico", "razao_social", "natureza_juridica", "qualificacao_responsavel",
        "capital_social", "porte_empresa", "ente_federativo"
    ],
    "estabelecimentos": [
        "cnpj_basico", "cnpj_ordem", "cnpj_dv", "matriz_filial", "nome_fantasia",
        "situacao_cadastral", "data_situacao_cadastral", "motivo_situacao_cadastral",
        "nome_cidade_exterior", "pais", "data_inicio_atividade",
        "cnae_fiscal_principal", "cnae_fiscal_secundaria", "tipo_logradouro",
        "logradouro", "numero", "complemento", "bairro", "cep", "uf", "municipio",
        "ddd1", "telefone1", "ddd2", "telefone2", "ddd_fax", "fax", "email",
        "situacao_especial", "data_situacao_especial"
    ],
    "socios": [
        "cnpj_basico", "identificador_socio", "nome_socio", "cnpj_cpf_socio",
        "qualificacao_socio", "data_entrada_sociedade", "pais",
        "representante_legal", "nome_representante", "qualificacao_representante",
        "faixa_etaria"
    ],
    "simples": [
        "cnpj_basico", "opcao_simples", "data_exclusao_simples", "opcao_mei", "data_exclusao_mei"
    ],
    "cnaes": ["codigo", "descricao"],
    "naturezas": ["codigo", "descricao"],
    "qualificacoes": ["codigo", "descricao"],
    "municipios": ["codigo", "descricao"],
    "paises": ["codigo", "descricao"],
    "motivos": ["codigo", "descricao"],
}

# Substrings dos nomes dos arquivos que identificam a tabela destino
FILENAME_MAP = {
    "EMPRECSV": "empresas",
    "ESTABELE": "estabelecimentos",
    "SOCIOCSV": "socios",
    "SIMPLES": "simples",
    "CNAECSV": "cnaes",
    "NATJUCSV": "naturezas",
    "QUALSCSV": "qualificacoes",
    "MUNICCSV": "municipios",
    "PAISCSV": "paises",
    "MOTICSV": "motivos",
}

def get_table_from_filename(filename):
    for key, table in FILENAME_MAP.items():
        if key in filename.upper():
            return table
    return None

def clean_csv_for_nulls(original_path, expected_columns, merge_last=False):
    temp = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='latin1', newline='')
    with open(original_path, 'r', encoding='latin1') as f_in:
        for line in f_in:
            line = line.replace('""', '').replace('"', '').strip()
            parts = line.split(';')
            if merge_last and len(parts) > len(expected_columns):
                # Junta colunas extras na última (ex: descricao com ;)
                fixed = parts[:len(expected_columns) - 1]
                fixed.append(';'.join(parts[len(expected_columns) - 1:]))
                parts = fixed
            # Garante que a linha tenha exatamente o número de colunas
            if len(parts) != len(expected_columns):
                continue  # ou logar erro, se quiser
            temp.write(';'.join(parts) + '\n')
    temp.flush()
    return temp.name

def import_csv_to_postgres(cursor, path, table_name, columns):
    with open(path, 'r', encoding='latin1') as f:
        next(f)  # pula cabeçalho
        print(f"→ Importando {path} → {table_name}")
        cursor.copy_expert(
            f"""
            COPY {table_name} ({', '.join(columns)})
            FROM STDIN WITH CSV DELIMITER ';' NULL '';
            """,
            f
        )

def preprocess_csv_file(path, expected_columns):
    output_path = path + ".cleaned"
    with open(path, 'r', encoding='latin1') as fin, open(output_path, 'w', encoding='latin1') as fout:
        for i, line in enumerate(fin):
            line = line.replace('""', '').replace('"', '').strip()
            parts = line.split(';')

            if i == 0 and len(parts) == len(expected_columns):
                fout.write(line + '\n')
                continue

            if len(parts) > len(expected_columns):
                # Junta tudo a partir da penúltima coluna (para 'descricao' quebrada)
                fixed = parts[:len(expected_columns) - 1]
                fixed.append(';'.join(parts[len(expected_columns) - 1:]))
                parts = fixed

            if len(parts) != len(expected_columns):
                print(f"[!] Ignorando linha {i + 1} malformada: {parts}")
                continue

            fout.write(';'.join(parts) + '\n')

    print(f"✔ Arquivo CNAE limpo salvo em: {output_path}")
    return output_path

def main():
    conn = psycopg2.connect(
        dbname="zeus",
        user="zeus_user",
        password="your_password",
        host="localhost"
    )

    with conn:
        with conn.cursor() as cursor:
            for file in os.listdir(UNZIP_DIR):
                if not ("CSV" in file.upper()):
                    continue

                table = get_table_from_filename(file)
                if not table:
                    print(f"[!] Nenhuma tabela correspondente para: {file}")
                    continue

                columns = TABLES.get(table)
                if not columns:
                    print(f"[!] Tabela desconhecida no mapeamento: {table}")
                    continue

                path = os.path.join(UNZIP_DIR, file)

                try:
                    # ⚠️ Só aplica limpeza ao arquivo de CNAEs
                    if table == 'cnaes':
                        cleaned_path = preprocess_csv_file(path, columns)
                        import_csv_to_postgres(cursor, cleaned_path, table, columns)
                    else:
                        import_csv_to_postgres(cursor, path, table, columns)

                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"[!] Erro ao importar {file}: {e}")

    print("✅ Importação completa.")

if __name__ == "__main__":
    main()
