---
schema: spec-driven
status: proposed
---

# Proposta: Adicionar Cobertura de Testes (Test Coverage)

## 1. O Que Vamos Construir?
Um sistema automatizado de checagem e emissão de relatórios de cobertura de código para o Backend (FastAPI). Integrando o `pytest-cov`, faremos com que toda execução de teste imprima no terminal e/ou gere um HTML mostrando a porcentagem exata de código que está protegida.

## 2. Por Que Vamos Construir Isso?
Porque ter testes rodando é 50% da jornada; os outros 50% consistem em saber *o que não foi testado*.
*   **Fundamentação Acadêmica:** Excelente argumento para mostrar maturidade de TCC, provando o nível de confiabilidade do Backend antes de entregar pro Fronte d.
*   **Transparência:** Impede que linhas "fantasmas" de condicionais (como `if/else` complexos na gestão de rotas do caminhão) fiquem em branco.
