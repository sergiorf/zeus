# zeus


tapa 4: Passo a passo inicial
🔹 Semana 1: Montar o pipeline mínimo
 Baixar e extrair a base CNPJ da Receita Federal

 Normalizar os dados (nomes de sócios, CNPJs, atividades)

 Gerar uma tabela com: empresa, sócio, tipo de vínculo, sufixo CPF

🔹 Semana 2: Construir o grafo de relações
 Criar nó para cada empresa

 Criar arestas de sócio → empresa

 Opcional: criar “nó pessoa física” com nome + sufixo CPF como ID

🔹 Semana 3: Dados financeiros e contratos públicos
 Baixar dados da CVM e contratos públicos

 Associar com CNPJs no grafo

 Extrair e armazenar valores de receita, contratos, etc.

🔹 Semana 4: Interface mínima
 Criar frontend básico com busca por CNPJ ou nome

 Exibir:

Empresa e sócios

Conexões com outras empresas

Dados financeiros e contratos

 Visualização do grafo com bibliotecas como D3.js, Sigma.js ou Vis.js

