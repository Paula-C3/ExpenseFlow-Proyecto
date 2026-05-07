import pytest

from app.domain.value_objects import Email, Money, RequestTitle


def test_email_valid():
    """Test: Email válido."""
    email = Email("usuario@example.com")
    assert str(email) == "usuario@example.com"


def test_email_invalid():
    """Test: Email inválido lanza excepción."""
    with pytest.raises(ValueError, match="Email inválido"):
        Email("invalid-email")


def test_money_valid():
    """Test: Money válido."""
    money = Money(100.50, "USD")
    assert money.amount == 100.50
    assert money.currency == "USD"
    assert str(money) == "100.5 USD"


def test_money_negative():
    """Test: Money negativo lanza excepción."""
    with pytest.raises(ValueError, match="El monto no puede ser negativo"):
        Money(-50.0)


def test_money_zero():
    """Test: Money cero es válido."""
    money = Money(0.0)
    assert money.amount == 0.0


def test_request_title_valid():
    """Test: RequestTitle válido."""
    title = RequestTitle("Pasaje de avión")
    assert str(title) == "Pasaje de avión"


def test_request_title_empty():
    """Test: RequestTitle vacío lanza excepción."""
    with pytest.raises(ValueError, match="El título no puede estar vacío"):
        RequestTitle("")


def test_request_title_too_long():
    """Test: RequestTitle muy largo lanza excepción."""
    long_title = "a" * 201
    with pytest.raises(ValueError, match="El título no puede exceder 200 caracteres"):
        RequestTitle(long_title)


def test_request_title_max_length():
    """Test: RequestTitle con 200 caracteres es válido."""
    title = RequestTitle("a" * 200)
    assert len(str(title)) == 200


def test_value_objects_immutable():
    """Test: Value objects son inmutables."""
    email = Email("user@example.com")
    
    with pytest.raises(AttributeError):
        email.value = "other@example.com"

