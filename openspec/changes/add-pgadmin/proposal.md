## Why

A API e o Banco de Dados contam com o Postgres localmente gerenciado em um container Docker. Embora o backend valide através do Swagger (na porta 8000), o gerenciamento do banco de dados relacional seria amplamente beneficiado se contasse com uma interface gráfica acessível facilmente sem a necessidade de baixar softwares desktop de terceiros. Para simplificar a demonstração do TCC e acelerar verificações visuais diretas, a inserção do PgAdmin no Docker é uma melhoria significativa no DX (Developer Experience).

## What Changes

A adição do serviço `pgadmin` ao arquivo raiz `docker-compose.yml`.

## Capabilities

### New Capabilities
- `pgadmin-ui`: Interface web rodando na porta `5050` (`admin@admin.com` - `admin`) que vai conectar via DNS interno da rede diretamente ao container do `db` na porta `5432`.

### Modified Capabilities

## Impact

Afeta apenas os responsáveis pela orquestração do ambiente de desenvolvimento. Não haverá alterações de código do núcleo do projeto em Python.
