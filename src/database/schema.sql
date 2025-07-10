DROP TABLE IF EXISTS
    socios,
    empresas,
    estabelecimentos,
    simples,
    cnaes,
    naturezas,
    qualificacoes,
    municipios,
    paises,
    motivos
CASCADE;

-- Empresas (basic registration of companies)
CREATE TABLE IF NOT EXISTS empresas (
    cnpj_basico CHAR(8) PRIMARY KEY,
    razao_social TEXT,
    natureza_juridica INTEGER,
    qualificacao_responsavel INTEGER,
    capital_social NUMERIC,
    porte_empresa INTEGER,
    ente_federativo TEXT
);

-- Estabelecimentos (branches and locations)
CREATE TABLE IF NOT EXISTS estabelecimentos (
    cnpj_basico CHAR(8),
    cnpj_ordem CHAR(4),
    cnpj_dv CHAR(2),
    matriz_filial INTEGER,
    nome_fantasia TEXT,
    situacao_cadastral INTEGER,
    data_situacao_cadastral DATE,
    motivo_situacao_cadastral INTEGER,
    nome_cidade_exterior TEXT,
    pais INTEGER,
    data_inicio_atividade DATE,
    cnae_fiscal_principal INTEGER,
    cnae_fiscal_secundaria TEXT,
    tipo_logradouro TEXT,
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cep CHAR(8),
    uf CHAR(2),
    municipio INTEGER,
    ddd1 TEXT,
    telefone1 TEXT,
    ddd2 TEXT,
    telefone2 TEXT,
    ddd_fax TEXT,
    fax TEXT,
    email TEXT,
    situacao_especial TEXT,
    data_situacao_especial DATE,
    PRIMARY KEY (cnpj_basico, cnpj_ordem, cnpj_dv)
);

-- Socios (partners/shareholders)
CREATE TABLE IF NOT EXISTS socios (
    id SERIAL PRIMARY KEY,
    cnpj_basico CHAR(8),
    identificador_socio INTEGER,
    nome_socio TEXT,
    cnpj_cpf_socio TEXT,  -- agora aceita NULL
    qualificacao_socio INTEGER,
    data_entrada_sociedade DATE,
    pais INTEGER,
    representante_legal TEXT,
    nome_representante TEXT,
    qualificacao_representante INTEGER,
    faixa_etaria INTEGER
);

-- Simples (Simplified tax regime info)
CREATE TABLE IF NOT EXISTS simples (
    cnpj_basico CHAR(8) PRIMARY KEY,
    opcao_simples DATE,
    data_exclusao_simples DATE,
    opcao_mei DATE,
    data_exclusao_mei DATE
);

-- CNAEs (National Economic Activity Classification)
CREATE TABLE IF NOT EXISTS cnaes (
    codigo INTEGER PRIMARY KEY,
    descricao TEXT
);

-- Naturezas jurídicas
CREATE TABLE IF NOT EXISTS naturezas (
    codigo INTEGER PRIMARY KEY,
    descricao TEXT
);

-- Qualificações (qualification types for socios and reps)
CREATE TABLE IF NOT EXISTS qualificacoes (
    codigo INTEGER PRIMARY KEY,
    descricao TEXT
);

-- Municípios
CREATE TABLE IF NOT EXISTS municipios (
    codigo INTEGER PRIMARY KEY,
    descricao TEXT
);

-- Países
CREATE TABLE IF NOT EXISTS paises (
    codigo INTEGER PRIMARY KEY,
    descricao TEXT
);

-- Motivos de situação cadastral
CREATE TABLE IF NOT EXISTS motivos (
    codigo INTEGER PRIMARY KEY,
    descricao TEXT
);
