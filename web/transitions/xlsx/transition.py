import os
import uuid

import django
import xlsxwriter

from datetime import datetime
from xlsxwriter import Workbook
from django.conf import settings
from django.db.models import QuerySet

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soil.settings")
django.setup()

from web.models import Plant


def create_media_xlsx_directory() -> None:
    os.makedirs(f"{settings.BASE_DIR}/media/xlsx", exist_ok=True)


def make_cell_format(wb: Workbook, bold=False, font_color="black", bg_color="white", num_format=None):
    cell_format = wb.add_format({"bold": bold, "font_color": font_color, "bg_color": bg_color, "border": True})
    if num_format:
        cell_format.set_num_format(num_format)
    return cell_format


def queryset_to_xlsx(qs: QuerySet) -> str:
    """
    A function to make QuerySet transition into .xlsx file
    """
    create_media_xlsx_directory()

    file_uuid = uuid.uuid4()
    path = f"{BASE_DIR}/media/xlsx/{file_uuid}.xlsx"
    workbook = xlsxwriter.Workbook(path, {"remove_timezone": True})
    sheet = workbook.add_worksheet("result")

    simple_format = make_cell_format(wb=workbook)
    date_format = make_cell_format(wb=workbook, num_format="dd/mm/yy hh:mm")
    header_format = make_cell_format(wb=workbook, bold=True, bg_color="#c8ed72")

    objects = qs.values()

    # writing headers
    headers = objects.first().keys()
    for x, header in enumerate(headers):
        sheet.write_string(0, x, header, cell_format=header_format)

    type_mapping = {
        str: sheet.write_string,
        int: sheet.write_number,
        float: sheet.write_number,
        bool: sheet.write_boolean,
        datetime: sheet.write_datetime,
    }

    # writing objects
    for x, obj in enumerate(objects, start=1):
        for y, column in enumerate(headers):
            obj_type = type(obj[column])
            if obj_type in type_mapping:
                type_mapping[obj_type](x, y, obj[column], simple_format if obj_type != datetime else date_format)
            else:
                raise TypeError(f"Uncultivited type: {type(obj[column])}")

    sheet.autofit()
    workbook.close()

    return path


if __name__ == "__main__":
    queryset_to_xlsx(Plant.objects.all())
