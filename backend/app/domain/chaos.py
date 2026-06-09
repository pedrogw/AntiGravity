from datetime import datetime, timedelta, timezone

def apply_chaos_to_eta(current_eta: datetime, impact_factor: float, delay_minutes: int) -> datetime:
    """Aplica fator multiplicativo e atraso fixo ao ETA restante de uma entrega."""
    if impact_factor < 0:
        raise ValueError("Impact factor cannot be negative")
    if delay_minutes < 0:
        raise ValueError("Delay cannot be negative")

    now = datetime.now(timezone.utc)
    if current_eta <= now:
        return current_eta + timedelta(minutes=delay_minutes)

    remaining_time = current_eta - now
    new_remaining = remaining_time * impact_factor
    new_eta = now + new_remaining + timedelta(minutes=delay_minutes)

    return new_eta.replace(microsecond=0)

def remove_chaos_from_eta(current_eta: datetime, previous_eta: datetime, impact_factor: float, delay_minutes: int) -> datetime:
    """Remove efeito do caos restaurando o ETA anterior ao evento."""
    return previous_eta.replace(microsecond=0)
