from sqlalchemy import DateTime, String, Text
from app.db.base import Base


class TestIdempotencyKeysMetadata:
    def test_table_is_registered(self):
        assert "idempotency_keys" in Base.metadata.tables

    def test_table_columns(self):
        table = Base.metadata.tables["idempotency_keys"]
        columns = {c.name: c for c in table.columns}

        assert "key" in columns
        assert columns["key"].primary_key is True
        assert isinstance(columns["key"].type, String)
        assert columns["key"].type.length == 255

        assert "response" in columns
        assert columns["response"].nullable is False
        assert isinstance(columns["response"].type, Text)

        assert "created_at" in columns
        assert isinstance(columns["created_at"].type, DateTime)
