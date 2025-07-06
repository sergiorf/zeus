CREATE TABLE IF NOT EXISTS socios (
    cnpj_basico VARCHAR(8),
    nome_socio TEXT,
    tipo_socio TEXT,
    qualificacao_socio TEXT,
    cpf_sufixo TEXT,
    PRIMARY KEY (cnpj_basico, nome_socio, cpf_sufixo)
);
