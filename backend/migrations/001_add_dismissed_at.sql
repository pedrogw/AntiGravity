-- Adiciona coluna dismissed_at à tabela alert (Bloco 36)
-- A coluna é nullable (TIMESTAMPTZ) — alertas existentes não são afetados.
ALTER TABLE alert ADD COLUMN dismissed_at TIMESTAMPTZ;
