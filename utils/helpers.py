from datetime import datetime, timedelta

def get_expiry_date(duration):
    start_date = datetime.utcnow()
    expiry_date = start_date + timedelta(days=duration)
    return expiry_date