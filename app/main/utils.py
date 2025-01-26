from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import datetime
import pytz

def get_current_uk_date():
    uk_timezone = pytz.timezone('Europe/London')
    return datetime.now(uk_timezone).strftime('%Y-%m-%d')