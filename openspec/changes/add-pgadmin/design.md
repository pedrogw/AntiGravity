## User Experience
Os desenvolvedores e operadores do banco de dados relacional terão uma interface gráfica acessível via web (`http://localhost:5050`) para consulta, modelagem e edição de dados, eliminando a dependência de clientes locais instalados.

## Architecture & Implementation Strategy
### Componentes Chave
1. **Container do PgAdmin**
   - Utilizaremos a imagem oficial `dpage/pgadmin4`.
   - Porta mapeada como `5050` (`5050:80`).
   - Variáveis de ambiente injetadas via Docker Compose definirão a master account root do portal (`PGADMIN_DEFAULT_EMAIL` e `PGADMIN_DEFAULT_PASSWORD`).

2. **Network Connection**
   - O PgAdmin fará parte da `logistics-net` e conseguirá enxergar o hostname `db`.

## Dependencies & API Changes
Nenhuma alteração na API. Adição no arquivo de Docker (`docker-compose.yml`).

## Data Model
Não há mudanças de modelagem.

## Security & Privacy
O PgAdmin não deve ser subido em ambientes de Produção sem travas rigorosas, mas como se trata de um ambiente Local / TCC, as credenciais `admin/admin` padrão são perfeitamente aceitáveis para facilitação.

## Testing Strategy
- Fazer up nos containers `sudo docker compose up -d`.
- Tentar acessar a porta 5050.
- Criar a conexão e executar uma query SELECT.
