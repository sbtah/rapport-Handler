import os
import sys
from datetime import datetime
import pathlib
import openpyxl
import pandas as pd
from handler.settings import BASE_DIR, DATA_ROOT_DIR
from utilites.logger import logger


class BaseOperator:
    BASE_DIR = BASE_DIR
    DATA_ROOT_DIR = DATA_ROOT_DIR

    DAY_DATE_FORMAT = "%d-%m-%Y"
    MONTH_DATE_FORMAT = "%m-%Y"
    YEAR_DATE_FORMAT = "%Y"

    def __init__(self, website=None):
        self.website = website
        self.logger = logger
        self.time_started = datetime.today()
        self.logger.info(f"Started operator for : '{self.website} '")

    # TODO:
    # Move to WebsiteOperator class.
    @property
    def website_directory(self):
        if self.website is not None:
            return self.DATA_ROOT_DIR / self.website
        else:
            return self.DATA_ROOT_DIR

    @property
    def time_started_day(self):
        return self.time_started.strftime(self.DAY_DATE_FORMAT)

    def find_directory(self, directory):
        """
        Searches for specified directory.
        Return directory path if successful.
        """
        try:
            check = os.path.exists(directory)
            if check:
                self.logger.info("Specified directory was found.")
                return directory
            else:
                self.logger.info("Specified directory does not exists.")
                return check
        except Exception as e:
            self.logger.error(f"(find_directory) Some other exception: {e}")
            raise

    # TODO:
    # Move to WebsiteOperator class.
    def find_directory_for_website(self, website: str) -> bool:
        """
        Searches for specified website directory in data folder.
        Return directory path if successful.
        """

        website_directory = self.website_directory

        try:
            check = os.path.exists(website_directory)
            if check:
                self.logger.info("Specified website directory was found.")
                return website_directory
            else:
                self.logger.info("Specified website directory does not exists.")
                return check
        except Exception as e:
            self.logger.error(f"(find_directory_for_website) Some other exception: {e}")
            raise

    def create_directory_for_website(self, directory: str):
        """
        Creates directory for website in data directory,
        where all rapports will be stored.
        """
        website_directory = self.DATA_ROOT_DIR / directory
        try:
            os.mkdir(website_directory)
            self.logger.info(f"Created directory: '{website_directory}'.")
            return True
        except FileExistsError:
            self.logger.info(f"Specified directory exists. Passing...")
            return None
        except Exception as e:
            self.logger.error(f"(create_directory) some other exception: {e}")
            raise

    def find_file_for_website_and_date(
        self,
        website: str,
        date: str,
    ) -> pathlib.PosixPath:
        """
        Finds rapport file for specified website and date.
        Returns path to file.
        - :arg website: Domain of website.
        - :arg date: Date string in proper format.
            Rapport system uses: %d-%m-%Y
        """

        website_directory = self.DATA_ROOT_DIR / website
        list_dir = os.listdir(website_directory)
        pattern = f"{website}-{date}"

        for file in list_dir:
            if pattern in file:
                self.logger.info(f"Found direcotry for website: {website}")
                return os.path.abspath(file)
            else:
                self.logger.error(f"Cannot find {pattern} in {website} directory.")

    def create_xlsx_file_for_date(self, directory, filename, date_str):
        """
        Create an empty XLSX file in specified directory.
        - :arg directory: Path in which file should be stored.
        - :arg filename: Name of the created file.
        - :arg date_str: Date that will be appended to a filename.
        """
        if isinstance(directory, pathlib.PosixPath):
            filepath = directory / f"{filename}-{date_str}.xslx"
            if os.path.exists(filepath):
                self.logger.info(f"Failed creating a file. File aready exists.")
                return True
            else:
                wb = openpyxl.Workbook()
                try:
                    wb.save(filepath)
                    self.logger.info(f"Created file: '{filename}-{date_str}.xslx'")
                    return True
                except FileNotFoundError:
                    self.logger.error("Cannot find specified directory...")
                    return None
                except Exception as e:
                    self.logger.error(
                        f"(find_or_create_xlsx_file) Some other exception: {e}"
                    )
                    return None
        else:
            self.logger.error(
                f"Wrong directory provided. Received: {type(directory)}, should be path."
            )
            return None

    def open_xlsx_file_for_date(self, directory, filename, date_str):
        """
        Open specified file for specified date in provided directory.
        Uses pandas library, returns DataFrame object.
        """
        filepath = directory / f"{filename}-{date_str}.xslx"
        try:
            frame = pd.read_excel(filepath)
            return frame
        except FileNotFoundError:
            self.logger.error("Specified xlsx file was not found.")
            return None
        except Exception as e:
            self.logger.error(f"(open_xlsx_file_for_date) Some other exception: {e}")
            return None
