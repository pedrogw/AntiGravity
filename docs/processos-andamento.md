# Processos em Andamento

## Fase Final — Infraestrutura

### F.1 — Dockerfile Otimizado

**Objetivo:** Refatorar o Dockerfile para produção com multi-stage build, `uv` em vez de `pip`, e imagem reduzida.

**Análise de Impacto:**

| Aspecto | Atual | Proposto |
|---|---|---|
| Estágios | Single-stage (1.2GB+) | Multi-stage (builder + runtime, ~300MB) |
| Gerenciador | `pip` | `uv` (consistente com `uv run alembic`) |
| Entrypoint | wait PostgreSQL + migrations + `--reload` | migrations + uvicorn (sem wait, sem reload) |
| CMD | `--reload` (dev) | Sem `--reload` (produção) |
| Sistema | `build-essential` + `libpq-dev` mantidos | Só runtime libs no estágio final |

**Plano:**

```dockerfile
# === Stage 1: Builder ===
FROM python:3.11-slim AS builder
RUN pip install uv
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# === Stage 2: Runtime ===
FROM python:3.11-slim
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Estratégia de entrypoint:**

| Ambiente | Comportamento | docker-compose |
|---|---|---|
| Dev | Wait PostgreSQL + migrations + `--reload` | `docker-compose.yml` atual (db local) |
| Produção | Migrations + uvicorn (sem wait) | `docker-compose.prod.yml` (Neon) |

**Entrypoint modificado para produção** (sem wait, fallback seguro):

```bash
#!/bin/bash
set -e

# Só aguarda PostgreSQL se DATABASE_URL apontar para um host local
if echo "$DATABASE_URL" | grep -qE '(localhost|127\.0\.0\.1|db)'; then
  echo "==> Aguardando PostgreSQL local..."
  # ... wait logic existente ...
fi

echo "==> Executando migrações..."
alembic upgrade head

echo "==> Iniciando servidor..."
exec "$@"
```

**Arquivos afetados:**

| Arquivo | Ação |
|---|---|
| `backend/Dockerfile` | Reescrever com multi-stage + uv |
| `backend/entrypoint.sh` | Adicionar condicional de wait |
| `docker-compose.yml` | Sem alterações (dev continua igual) |

**Verificação:**
- `docker build -t antigravity:latest ./backend` — build bem-sucedido
- `docker run antigravity:latest` — app sobe sem erros
- Tamanho da imagem reduzido (~300MB vs ~1.2GB)

### Diagnóstico por Arquivo

| # | Arquivo | Linha(s) | Regra | Problema | Solução |
|---|---|---|---|---|---|
| 1 | `components/ui/dropdown-menu.tsx` | 27 | `no-explicit-any` | `React.ReactElement<any>` | Tipar com `{ onClick?: () => void }` |
| 2 | `hooks/useAuth.test.ts` | 22 | `no-explicit-any` | `let mockExecute: any` | Usar `ReturnType<typeof vi.fn>` |
| 3 | `hooks/useAuth.test.ts` | 29 | `no-explicit-any` | `} as any` no mock | Usar `as unknown as LoginUseCase` |
| 4 | `infra/repositories/ApiDeliveryRepository.ts` | 5 | `no-explicit-any` | `raw: any` | Criar interface `DeliveryApiResponse` |
| 5 | `mocks/handlers.ts` | 7 | `no-explicit-any` | `req.body as any` | Tipar como `{ email: string; password: string }` |
| 6 | `mocks/handlers.ts` | 42 | `no-explicit-any` | `req.body as any` | Tipar como `{ refresh_token: string }` |
| 7-16 | `hooks/useDeliveries.test.ts` | 4 locais | `no-explicit-any` | `as any` nos mocks | Usar `as unknown as UseCaseType` |
| 17-24 | `hooks/usePlaces.test.ts` | 2 locais | `no-explicit-any` | `as any` nos mocks | Usar `as unknown as UseCaseType` |
| W1 | `components/ui/avatar.tsx` | 17 | `no-img-element` | `<img>` sem `alt` | Comentário `eslint-disable` seletivo (shadcn) |
| W2 | `components/ui/dialog.tsx` | 48 | `no-unused-vars` | `asChild` prop não usada | Remover `asChild` da interface |
| W3 | `utils/jwt.ts` | 24 | `no-unused-vars` | `e` no `catch` não usado | Remover parâmetro: `catch {` |

**Total:** 16 erros + 8 warnings → solucionados sem `any` em produção, sem supressões genéricas.

### Análise de Impacto Detalhada

#### P9.1 — `dropdown-menu.tsx:27` (shadcn)

**Arquivo:** `src/components/ui/dropdown-menu.tsx`
**Antes:** `React.cloneElement(child as React.ReactElement<any>, {`
**Depois:** `React.cloneElement(child as React.ReactElement<{ onClick?: () => void }>, {`
**Impacto:** Mínimo. Apenas o tipo genérico foi refinado para o que realmente usamos (`onClick`). Zero alteração de runtime.

#### P9.2 — `useAuth.test.ts:22,29`

**Arquivo:** `src/hooks/useAuth.test.ts`
**Antes:**
```typescript
let mockExecute: any;
vi.mocked(makeLoginUseCase).mockReturnValue({
  execute: mockExecute,
} as any);
```
**Depois:**
```typescript
import { LoginUseCase } from '../application/use_cases/LoginUseCase';
let mockExecute: ReturnType<typeof vi.fn>;
vi.mocked(makeLoginUseCase).mockReturnValue({
  execute: mockExecute,
} as unknown as LoginUseCase);
```
**Impacto:** Zero em produção. Testes mais seguros com tipo real do use case.

#### P9.3 — `ApiDeliveryRepository.ts:5`

**Arquivo:** `src/infrastructure/repositories/ApiDeliveryRepository.ts`
**Antes:** `function toDelivery(raw: any): Delivery {`
**Depois:**
```typescript
interface DeliveryApiResponse {
  id?: string;
  factory_id?: string;
  factoryId?: string;
  store_id?: string;
  storeId?: string;
  driver_id?: string;
  driverId?: string;
  status?: string;
  eta_original?: string;
  etaOriginal?: string;
  eta_current?: string;
  etaCurrent?: string;
  departed_at?: string;
  departedAt?: string;
  current_lat?: number;
  currentLat?: number;
  current_lng?: number;
  currentLng?: number;
}

function toDelivery(raw: DeliveryApiResponse): Delivery {
```
**Impacto:** Zero em runtime. Documenta o formato esperado da API. Interface pode ser exportada se reutilizada.

#### P9.4 — `handlers.ts:7,42`

**Arquivo:** `src/mocks/handlers.ts`
**Antes:**
```typescript
const { email, password } = req.body as any;
const { refresh_token } = req.body as any;
```
**Depois:**
```typescript
const { email, password } = req.body as { email: string; password: string };
const { refresh_token } = req.body as { refresh_token: string };
```
**Impacto:** Zero em runtime. Apenas refinei a asserção.

#### P9.5 — Testes criados no P7 (`useDeliveries.test.ts`, `usePlaces.test.ts`)

**Arquivos:** `src/hooks/useDeliveries.test.ts`, `src/hooks/usePlaces.test.ts`
**Problema:** 6 ocorrências de `as any` nos mocks das factories
**Solução:** Substituir por `as unknown as CreateDeliveryUseCase` etc., importando os tipos reais dos use cases.
**Impacto:** Apenas import adicional + cast explícito. Zero alteração de lógica de teste.

#### P9.6 — `avatar.tsx:17` (shadcn)

**Arquivo:** `src/components/ui/avatar.tsx`
**Problema:** `<img>` em vez de `<Image>` do Next.js.
**Solução:** `// eslint-disable-next-line @next/next/no-img-element` — comentário seletivo de uma linha.
**Justificativa:** shadcn é gerado por CLI e usa `<img>` com forwardRef. Substituir por `<Image>` quebraria a assinatura de tipos (`Image` não aceita ref de `HTMLImageElement`).
**Impacto:** Nenhum.

#### P9.7 — `dialog.tsx:48` (shadcn)

**Arquivo:** `src/components/ui/dialog.tsx`
**Problema:** Prop `asChild` é destruturada mas não usada.
**Solução:** Remover `asChild` do tipo `DialogTriggerProps`. Se um consumidor passar `asChild`, será ignorado via `...props` (como já acontecia). Alternativamente, implementar o comportamento. Optamos por remover por ser mais simples e o comportamento padrão (sempre wrapper div) ser suficiente.
**Impacto:** Consumidores existentes passando `asChild` não quebram — a prop é absorvida por `...props` e ignorada, mesmo comportamento de antes.

#### P9.8 — `jwt.ts:24`

**Arquivo:** `src/utils/jwt.ts`
**Antes:**
```typescript
} catch (e) {
  return true;
}
```
**Depois:**
```typescript
} catch {
  return true;
}
```
**Impacto:** Zero. Comportamento idêntico.

### Ordem de Execução

```
1. infra/repositories/ApiDeliveryRepository.ts   (P9.3 — tipar raw)
2. hooks/useAuth.test.ts                          (P9.2 — tipar mockExecute)
3. hooks/useDeliveries.test.ts                    (P9.5 — remover any)
4. hooks/usePlaces.test.ts                        (P9.5 — remover any)
5. mocks/handlers.ts                              (P9.4 — tipar req.body)
6. components/ui/dropdown-menu.tsx                (P9.1 — ReactElement<any>)
7. components/ui/avatar.tsx                       (P9.6 — suppress img)
8. components/ui/dialog.tsx                       (P9.7 — remover asChild)
9. utils/jwt.ts                                   (P9.8 — catch sem parâmetro)
```

### Verificação

- ✅ `as any` eliminado de `src/` e `__tests__/`
- ✅ `catch (e)` substituído por `catch`
- ✅ `asChild` removido de dialog
- ✅ shadcn preservado com suppress por linha

---

## Concluídos

| Processo | Status |
|---|---|
| Pendente 3 — Segurança | ✅ Concluído |
| Fase D — Domínio Rico (9/9 tarefas) | ✅ Concluído |
| Pendente 4 — Robustez (Idempotency Key) | ✅ Concluído |
| Pendente 5 — Cache em produção | ✅ Concluído |
| Pendente 6 — Worker Queue Async (3 fases) | ✅ Concluído |
| Pendente 8 — Cobertura Infraestrutura ≥80% | ✅ Concluído |
| Migration `idempotency_keys` | ✅ Concluído |
| **P7 — Housekeeping (Frontend)** | ✅ **Concluído** |
| **P9 — Linting Frontend** | ✅ **Concluído** |
