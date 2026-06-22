import pytest
from unittest.mock import AsyncMock, patch


class TestDisposeEngine:
    async def test_calls_engine_dispose(self):
        mock_engine = AsyncMock()
        with patch("app.core.bootstrap.engine", mock_engine):
            from app.core.bootstrap import dispose_engine
            await dispose_engine()
            mock_engine.dispose.assert_awaited_once()


class TestGetDb:
    async def test_yields_session(self):
        mock_session = AsyncMock()
        mock_local = AsyncMock()
        mock_local.__aenter__.return_value = mock_session
        mock_local.__aexit__.return_value = None

        with patch("app.core.bootstrap.AsyncSessionLocal", return_value=mock_local):
            from app.core.bootstrap import get_db
            gen = get_db()
            session = await gen.__anext__()
            assert session is mock_session

            with pytest.raises(StopAsyncIteration):
                await gen.__anext__()
