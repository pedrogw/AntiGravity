from app.domain.entities.user import User, UserRole


def test_user_is_motorista():
    user = User(email="m@t.com", password_hash="x", role=UserRole.motorista)
    assert user.is_motorista() is True
    assert user.is_lojista() is False


def test_user_is_lojista():
    user = User(email="l@t.com", password_hash="x", role=UserRole.lojista)
    assert user.is_lojista() is True
    assert user.is_motorista() is False
