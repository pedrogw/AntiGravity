from datetime import datetime, timezone

def is_safe_check_expired(last_ping: datetime, timeout_minutes: int = 10) -> bool:
    """True se o último ping do motorista excedeu o timeout."""
    if last_ping is None:
        return True
    now = datetime.now(timezone.utc)
    diff = now - last_ping
    return diff.total_seconds() > (timeout_minutes * 60)

def evaluate_truck_speed_status(speed: float) -> str:
    """Retorna 'stopped' se velocidade for zero, 'moving' caso contrário."""
    if speed < 0:
        raise ValueError("Speed cannot be negative")
    if speed == 0.0:
        return "stopped"
    return "moving"
