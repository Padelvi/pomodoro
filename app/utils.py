from datetime import datetime
from nptime import nptime

def now() -> nptime:
    time = datetime.now().time()
    return nptime(hour=time.hour, minute=time.minute, second=time.second)
