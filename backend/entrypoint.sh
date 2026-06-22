#!/bin/bash
set -e

if echo "$DATABASE_URL" | grep -qE '(localhost|127\.0\.0\.1|@db)'; then
  echo "==> Aguardando PostgreSQL local ficar disponível..."

  RETRIES=30
  until python -c "
import asyncio
import asyncpg
import os
import sys

async def check():
    try:
        url = os.environ.get('DATABASE_URL', '')
        conn = await asyncpg.connect(url)
        await conn.close()
        return True
    except Exception:
        return False

sys.exit(0 if asyncio.run(check()) else 1)
" 2>/dev/null; do
    RETRIES=$((RETRIES - 1))
    if [ $RETRIES -le 0 ]; then
      echo "==> ERRO: PostgreSQL não ficou pronto a tempo"
      exit 1
    fi
    echo "==> PostgreSQL não está pronto... tentando novamente em 2s ($RETRIES restantes)"
    sleep 2
  done

  echo "==> PostgreSQL está pronto!"
else
  echo "==> Conectando ao PostgreSQL remoto (Neon)..."
fi

echo "==> Executando migrações..."
alembic upgrade head

echo "==> Iniciando servidor..."
exec "$@"
