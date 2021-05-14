from django.core.management.base import BaseCommand
from zipfile import ZipFile
import pandas as pd
import json
from django.conf import settings
import redis
from io import BytesIO
import urllib

# Connect to Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


class Command(BaseCommand):
    def download(self):
        # todo:: generate name from current date
        url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ120521_CSV.ZIP'
        req = urllib.request.Request(
            url, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)
        zipfile = ZipFile(BytesIO(con.read()))
        with zipfile.open(zipfile.namelist()[0]) as f:
            csv_data = pd.read_csv(f)
            for _, data in csv_data.iterrows():
                code = data['SC_CODE']
                name = data['SC_NAME'].strip()
                open_ = data['OPEN']
                high = data['HIGH']
                low = data['LOW']
                close = data['CLOSE']
                redis_instance.set(str(name), json.dumps(
                    {'SC_NAME': name, 'SC_CODE': code, 'OPEN': open_, 'HIGH': high, 'LOW': low, 'CLOSE': close}))

    def handle(self, *args, **kwargs):
        self.download()
