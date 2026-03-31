from datetime import datetime, timedelta

def apply_chaos_to_eta(current_eta: datetime, impact_factor: float, delay_minutes: int) -> datetime:
    if impact_factor < 0:
        raise ValueError("Impact factor cannot be negative")
    if delay_minutes < 0:
        raise ValueError("Delay cannot be negative")

    now = datetime.utcnow()
    # If the ETA is already in the past, or very close, just add delay.
    if current_eta <= now:
        return current_eta + timedelta(minutes=delay_minutes)
        
    remaining_time = current_eta - now
    # Multiply the remaining duration by factor, and add literal delays
    new_remaining = remaining_time * impact_factor
    new_eta = now + new_remaining + timedelta(minutes=delay_minutes)
    
    # We strip microseconds because of floating point math issues from timedelta scaling 
    return new_eta.replace(microsecond=0)

def remove_chaos_from_eta(current_eta: datetime, previous_eta: datetime, impact_factor: float, delay_minutes: int) -> datetime:
    # Just mathematically return previous_eta to fulfill pure reverting correctly
    return previous_eta.replace(microsecond=0)
