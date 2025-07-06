# 🐘 Inicialização do Banco de Dados PostgreSQL — Projeto Zeus

Este documento descreve os comandos necessários para **instalar**, **inicializar**, e **configurar** o banco de dados PostgreSQL no **EndeavourOS (Arch Linux)** para uso no projeto **Zeus**.

---

## ✅ 1. Instalar PostgreSQL

No terminal:

```bash
sudo pacman -S postgresql

## ✅ 2. Inicializar o banco de dados (apenas na primeira vez)

sudo su - postgres
initdb -D /var/lib/postgres/data
exit

## ✅ 3. Iniciar e habilitar o serviço PostgreSQL

sudo systemctl enable --now postgresql

## ✅ 4. Criar o banco de dados e o usuário para o Zeus

sudo -u postgres psql
CREATE DATABASE zeus;
CREATE USER zeus_user WITH PASSWORD 'zeus_pass';
GRANT ALL PRIVILEGES ON DATABASE zeus TO zeus_user;
\q

sudo -u postgres psql -d zeus
GRANT ALL ON SCHEMA public TO zeus_user;
ALTER SCHEMA public OWNER TO zeus_user;
\q

## ✅ 5. Verificar se o banco está funcionando

psql -U zeus_user -d zeus -h localhost

## ✅ 6. Criar a estrutura de tabelas (schema)

psql -U zeus_user -d zeus -f src/database/schema.sql

