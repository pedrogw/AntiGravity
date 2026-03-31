## FASE 1: Admin Seed Script
- [ ] 1.1 Criar rotina `admin_seed.py` na raiz do backend que insere um usuário-mestre (`admin@antigravity.com`, senha `admin`) no banco de dados.
- [ ] 1.2 Cuidar de limpar a conta antiga se já existir (tratamento de idempotência).
- [ ] 1.3 Rodar o comando `sudo docker compose exec api python admin_seed.py` e verificar a completude no terminal.

## FASE 2: API Integration Tests (E2E)
- [ ] 2.1 Criar pasta `backend/tests/api/` e `test_integration.py`.
- [ ] 2.2 Configurar um cliente HTTP assíncrono padrão do FastAPI (`httpx.AsyncClient`) vinculado ao `app.main:app`.
- [ ] 2.3 Validar Rota (`POST /auth/register`): Inserir um usuário teste via payload json e certificar-se que a API retorna código HTTP 201.
- [ ] 2.4 Validar Rota (`POST /auth/login`): Testar credenciais inválidas (recebendo 401) e credenciais válidas, testar token formatado.
- [ ] 2.5 Validar Fluxo (`POST /places/factories`): Testar inclusão de locais.
- [ ] 2.6 Executar globalmente com `sudo docker compose exec api pytest tests/api -v` para certificar `PASS` em todas asserções HTTP conectando direto com endpoints vivos.
