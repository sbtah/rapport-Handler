import pandas as pd
import openpyxl
import logging
import os
import sys
from datetime import datetime
from logging import StreamHandler, Formatter
from core.settings import BASE_DIR, DATA_ROOT_DIR



class BaseOperator():

    BASE_DIR = BASE_DIR
    DATA_ROOT_DIR = DATA_ROOT_DIR
    DATE_FORMAT = '.'
    
    def __init__(self, website):
        self.website = website
        self.logger = logging.getLogger(website)
        self.logger.setLevel(logging.DEBUG)
        self.handler = StreamHandler(stream=sys.stdout)
        self.handler.setFormatter(
            Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s')
        )
        self.logger.addHandler(self.handler)
        self.time_started = datetime.now()
        self.logger.info(f"Started Operator for : '{self.website}'")

    @property
    def project_directory(self):
        return self.DATA_ROOT_DIR / self.website
    
    @property
    def time_started_day(self):
        return self.time_started.strftime("%Y-%m-%d")

    def find_or_create_website_directory(self, directory):
        """
        Looks if provided project's direcory path exists.
        Creates directory after check.
        """    
        try:
            os.mkdir(directory)
            self.logger.info(
                f"Created directory for Website: '{self.website}'."
            )
            return True
        except FileExistsError:
            self.logger.info(
                f"Specified directory for: '{self.website}' exists. Passing..."
            )
            return None
        except Exception as e:
            self.logger.info(
                f"(find_or_create_website_directory) some other exception: {e}"
            )
            raise
    
    def find_or_create_xlsx_file(self, directory, date_str):
        """
        Tries to create an empy XLSX file in specified directory.
        """

        filepath = directory / f'{self.website}-{date_str}.xslx'

        if os.path.exists(filepath):
            self.logger.info(f'Failed creating a file. File aready exists.')
            return True
        else:        
            wb = openpyxl.Workbook()
            try:
                wb.save(filepath)
                self.logger.info(f'Creation of file successful.')
                return True
            except Exception as e:
                self.logger.error(
                    f'(find_or_create_xlsx_file) Some other exception: {e}'
                )
                return None
    
    def open_xlsx_file(self, directory, date_str):
        filepath = directory / f'{self.website}-{date_str}.xslx'
        frame = pd.read_excel(filepath)
        return frame