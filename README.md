🤖 ETL Vendas SQL → CSV

Automação ETL desenvolvida em Python para extração de dados de vendas do SQL Server, aplicação de validações e exportação dos dados para arquivos CSV.

O projeto foi desenvolvido com foco em automação de processos, integração com banco de dados, tratamento de erros e geração estruturada de arquivos, simulando um cenário comum de rotina de dados.

---

🎯 Objetivo

Automatizar o processo de extração e disponibilização de dados de vendas, reduzindo atividades manuais e garantindo maior padronização e rastreabilidade durante a execução.

O processo realiza:

- Conexão com o SQL Server
- Execução de consulta SQL
- Extração dos dados
- Validação das informações
- Exportação para CSV
- Registro de logs
- Tratamento de erros e exceções

---

🔄 Fluxo do ETL

SQL Server
    ↓
Extração dos dados
    ↓
Validação
    ↓
Tratamento
    ↓
Exportação CSV
    ↓
Registro de log

---

🧩 Etapas do processo

1. Extração

O processo estabelece uma conexão com o SQL Server e executa a consulta responsável pela obtenção dos dados de vendas.

2. Validação

Os dados extraídos são avaliados antes da geração do arquivo, permitindo identificar situações inesperadas durante o processamento.

3. Tratamento

O processo possui tratamento de exceções para evitar que falhas durante a execução ocorram sem registro.

4. Exportação

Após o processamento, os dados são disponibilizados em formato CSV, facilitando sua utilização por outros processos ou ferramentas de análise.

5. Logging

A execução possui registro de informações relevantes para acompanhamento e identificação de possíveis problemas.

---

🛡️ Tratamento de erros

O projeto utiliza tratamento de exceções para controlar situações de erro durante:

- Conexão com o banco de dados
- Execução da consulta
- Processamento dos dados
- Geração do arquivo CSV

Os erros são registrados em log para facilitar a identificação e análise do problema.

---

🛠️ Tecnologias utilizadas

- Python
- SQL Server
- Pandas
- PyODBC
- CSV
- Logging

---

📂 Estrutura do projeto

etl-vendas-sql-csv/
│
├── etl_vendas_arquivo_csv.py
├── README.md
└── .gitignore

---

💡 Conceitos aplicados

Durante o desenvolvimento foram aplicados conceitos relacionados a:

- ETL
- Automação de processos
- Integração Python + SQL Server
- Manipulação de dados com Pandas
- Exportação de dados
- Tratamento de exceções
- Logging
- Organização de código
- Boas práticas de desenvolvimento

---

🚀 Possíveis aplicações

Esse tipo de automação pode ser utilizado em rotinas de dados nas quais informações armazenadas em bancos relacionais precisam ser extraídas e disponibilizadas periodicamente para outros processos, análises ou ferramentas de BI.

---

👨‍💻 Desenvolvimento

Projeto desenvolvido como parte do meu processo de evolução em Python, Automação e Engenharia de Dados, com foco na aplicação prática de conceitos de ETL e integração com banco de dados.

O projeto também faz parte da construção do meu portfólio na área de Dados e BI.
