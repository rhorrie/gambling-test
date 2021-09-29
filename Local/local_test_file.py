import datetime
from datetime import date
import time

test = date(2021, 9, 7) - datetime.date.today()
week = test.days/7
print(week)