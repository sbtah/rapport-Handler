from core.operator import base
from datetime import datetime

projects = ["meowbaby", "kiddymoon", "misioohandmade", "ajababy"]


for name in projects:
    a = base.BaseOperator(website=name)


    a.find_or_create_website_directory(directory=a.project_directory)
    if_file = a.find_or_create_xlsx_file(
        directory=a.project_directory,
        date_str=a.time_started_day,
    )
    file = a.open_xlsx_file(
        directory=a.project_directory,
        date_str=a.time_started_day,
    )
    print(file)