#!/bin/bash
# scripts/setup.sh — Configura o ambiente de desenvolvimento
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "==> Criando virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "==> Instalando dependências..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "==> Setup concluído!"
echo "Use: source $VENV_DIR/bin/activate"
