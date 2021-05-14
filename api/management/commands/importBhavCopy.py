from django.core.management.base import BaseCommand
from datetime import datetime
from zipfile import ZipFile
from django.conf import settings
from io import BytesIO
import pandas as pd
import urllib
import redis
import logging


# Connect to Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)
logger = logging.getLogger('django')


class Command(BaseCommand):
    def download_bhavcopy_zip(self, full_todays_date):
        """
        Downloads and returns zip file

        Args:
            full_todays_date (string): Todays' date as string

        Returns:
            ZipFile: Zipfile in memory downloaded from BSE
        """
        todays_date = "".join(full_todays_date.split('-'))
        logger.info(f'todays_date {todays_date}')
        url = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{todays_date}_CSV.ZIP'
        logger.info(f'URL generated {url}')
        # Set user-agent to prevent 403 error
        req = urllib.request.Request(
            url, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)
        return ZipFile(BytesIO(con.read()))

    def import_data_from_csv(self, zipfile, full_todays_date):
        """
        Read csv and import data into appropriate Redis data structure

        Args:
            zipfile (ZipFile): In memory ZipFile
            full_todays_date (st): Todays' date in IST
        """
        with redis_instance.pipeline() as pipe:
            # Open the first and only file in zip
            with zipfile.open(zipfile.namelist()[0]) as f:
                csv_data = pd.read_csv(f)
                for _, data in csv_data.iterrows():
                    code = data['SC_CODE']
                    name = data['SC_NAME'].strip()
                    open_ = data['OPEN']
                    high = data['HIGH']
                    low = data['LOW']
                    close = data['CLOSE']

                    pipe.sadd(name, full_todays_date)

                    # Get all possible search prefixes
                    possible_prefixes = [name[:x]
                                             for x in range(2, len(name))]

                    logger.info(possible_prefixes)
                    # Create a set with prefix as key and add the complete string as member of the set
                    for prefix in possible_prefixes:
                        pipe.sadd(prefix, name)

                    pipe.hmset(
                        f'{name}:{full_todays_date}',
                        {'SC_NAME': name, 'SC_CODE': code, 'OPEN': open_, 'HIGH': high,
                         'LOW': low, 'CLOSE': close})
                    pipe.execute()

    def add_arguments(self, parser):
        parser.add_argument('todays_date', type=str)

    def handle(self, *args, **options):
        todays_date = options['todays_date']
        zipfile = self.download_bhavcopy_zip(todays_date)
        self.import_data_from_csv(zipfile, todays_date)
