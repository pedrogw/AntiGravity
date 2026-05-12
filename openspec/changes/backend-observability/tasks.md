## 1. Fundamentos e Clean Architecture (Use Cases)

- [ ] 1.1 Criar arquivo `app/core/exceptions.py` com a classe base `DomainException(Exception)` e filhas (ex: `EntityNotFoundException`, `InvalidCredentialsException`)
- [ ] 1.2 Remover o import `fastapi.HTTPException` de todos os arquivos em `app/use_cases/`
- [ ] 1.3 Substituir os `raise HTTPException` dentro dos Use Cases pelos equivalentes em `DomainException`

## 2. Observabilidade & Logging Seguro

- [ ] 2.1 Criar `app/core/logging.py` configurando formatação JSON
- [ ] 2.2 Implementar filtro de **Data Masking** para campos sensíveis (`password`, `token`) antes da injeção no log
- [ ] 2.3 Criar `app/api/middleware.py` com `ObservabilityMiddleware` para injetar `X-Request-ID` e logar status, rota e tempo

## 3. Integração Global de Tratamento (main.py)

- [ ] 3.1 Registrar o `ObservabilityMiddleware` no `app/main.py`
- [ ] 3.2 Remover o block solto de `@app.exception_handler(OperationalError)` atual do `main.py`
- [ ] 3.3 Criar um novo handler global no `main.py` capaz de mapear as `DomainExceptions` nativas e o `OperationalError`, devolvendo respostas JSON puras sem acoplar o Use Case
- [ ] 3.4 Garantir que exceções cruas gerem log do stacktrace atrelado ao `X-Request-ID`, escondendo o trace interno do cliente

## 4. Refatoração das Rotas da API

- [ ] 4.1 Limpar blocos de `try/except` que não lidam diretamente com o negócio nas rotas em `app/api/` (confiando no Global Handler)
- [ ] 4.2 Oficializar a rota `GET /health` garantindo verificação funcional

## 5. Validação da Infraestrutura

- [ ] 5.1 Disparar propositalmente erros de login para validar que senhas aparecem mascaradas no console de testes
- [ ] 5.2 Rodar `pytest -v` e confirmar aderência da arquitetura
