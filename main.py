from handler.logic.base import BaseOperator
from datetime import datetime
from handler.settings import BASE_DIR, DATA_ROOT_DIR
import os


today = datetime.today().strftime("%d-%m-%Y")

operator = BaseOperator(website="castorama.pl")

# operator.create_directory_for_website("castorama.pl")
# castor_dir = operator.find_directory_for_website('castorama.pl')
# rapport = operator.create_xlsx_file_for_date(castor_dir, "castorama.pl", today)


print(operator.find_file_for_website_and_date("castorama.pl", "05-02-2023"))
