# Tarefas de Implementação: Add Test Coverage

## 1. Motor de Dependências
- [x] 1.1 Instalar e adicionar bibliotecas `coverage` e `pytest-cov` dentro do ambiente Backend do Docker. Pode ser via update agressivo no container usando `pip install pytest-cov` pra testar agora, ou editando `requirements.txt`.

## 2. Alterações de Base (Ini)
- [x] 2.1 Abrir arquivo `backend/pytest.ini` e adicionar a base: `addopts = --cov=app --cov-report=term-missing`.
- [x] 1.2 Atualização do container enviada ao usuário.

## 3. Emissão de Relatório e Limpeza
- [ ] 3.1 Executar os testes pela base Docker `sudo docker compose exec api pytest` para forçar a renderização do sumário novo no terminal e validarmos nossas métricas percentuais.
