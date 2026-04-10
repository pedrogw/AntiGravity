# Design Técnico: Cobertura de Testes (Coverage)

## 1. Arquitetura e Dependências
O Backend já roda perfeitamente em cima do `Pytest`. Para instanciarmos a métrica estatística, as seguintes extensões serão injetadas:
*   `coverage`: Motor em C/Python nativo que "espiona" a execução de scripts.
*   `pytest-cov`: A ponte que une a experiência maravilhosa do Pytest que já temos ao motor estatístico.

Como operamos no **Docker**, a dependência precisará ser salva no `requirements.txt` (ou script equivalente) do App Backend.  

## 2. Configurações Globais
Toda configuração rodará automaticamente a partir do arquivo existente `backend/pytest.ini`.

**Flags Injetadas:**
*   `--cov=app`: Monitorar exclusivamente o core da nossa regra de negócio e rotas (ignorar bibliotecas de terceiros pra não distorcer o resultado em falso).
*   `--cov-report=term-missing`: Em vez de só imprimir um número final `95%`, ele vai desenhar no terminal exatamente a linha do arquivo que faltou (Exemplo: `places.py - Misses Line 43`).
