import pytz

import numpy as np
from datetime import datetime, time
from dateutil.relativedelta import *

def rules_absensi():
    nilai = 49.5
    jam = datetime.now(pytz.timezone('Asia/Jakarta')).time()
    minimum_masuk = time(8, 30, 0)
    maksimum_masuk = time(9, 00, 0)
    if jam > minimum_masuk:
        nilai = nilai - 0.5
    if jam > maksimum_masuk:
        nilai = nilai - 1.5
    return nilai

def hitung_hari():
    this_date = datetime.now()
    next_date = this_date + relativedelta(months=+1)
    this_year = this_date.year
    this_month = str(this_date.month).rjust(2, "0")
    next_year = next_date.year
    next_month = str(next_date.month).rjust(2, "0")
    # next_month = next_date.month
    this = f"{this_year}-{this_month}"
    next = f"{next_year}-{next_month}"
    bussines_day = np.busday_count(this, next)
    saturday_day = np.busday_count(this, next, weekmask="Sat")
    return bussines_day + saturday_day

def hitung_custom_hari(bulan, tahun):
    this_date = datetime.strptime(f"{tahun}-{bulan}", "%Y-%m")
    next_date = this_date + relativedelta(months=+1)
    this_year = this_date.year
    this_month = this_date.month
    next_year = next_date.year
    next_month = str(next_date.month).rjust(2, "0")
    this = f"{this_year}-{this_month}"
    next = f"{next_year}-{next_month}"
    bussines_day = np.busday_count(this, next)
    saturday_day = np.busday_count(this, next, weekmask="Sat")
    return bussines_day + saturday_day
