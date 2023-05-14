import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path

import xlsxwriter
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from xlsxwriter import Workbook

NoneType = type(None)


def make_cell_format(wb: Workbook, bold=False, font_color="black", bg_color="white", num_format=None):
    cell_format = wb.add_format({"bold": bold, "font_color": font_color, "bg_color": bg_color, "border": True})
    if num_format:
        cell_format.set_num_format(num_format)
    return cell_format


def queryset_to_xlsx(qs: list[dict]) -> Path:
    """
    A function to make QuerySet transition into .xlsx file
    """

    file_uuid = uuid.uuid4()
    buffer_file = BytesIO()

    with xlsxwriter.Workbook(buffer_file, {"remove_timezone": True}) as workbook:
        sheet = workbook.add_worksheet("result")

        simple_format = make_cell_format(wb=workbook)
        date_format = make_cell_format(wb=workbook, num_format="dd/mm/yy hh:mm")
        header_format = make_cell_format(wb=workbook, bold=True, bg_color="#c8ed72")

        objects = qs

        # writing headers
        headers = objects[0].keys()
        for x, header in enumerate(headers):
            sheet.write_string(0, x, header, cell_format=header_format)

        type_mapping = {
            str: sheet.write_string,
            int: sheet.write_number,
            float: sheet.write_number,
            bool: sheet.write_boolean,
            datetime: sheet.write_datetime,
            NoneType: sheet.write_blank,
        }

        # writing objects
        for x, obj in enumerate(objects, start=1):
            for y, column in enumerate(headers):
                obj_type = type(obj[column])
                if obj_type in type_mapping:
                    type_mapping[obj_type](x, y, obj[column], simple_format if obj_type != datetime else date_format)
                else:
                    raise TypeError(f"Unmapped type: {type(obj[column])}")

        sheet.autofit()

    path = default_storage.save(Path("xlsx") / f"{file_uuid}.xlsx", buffer_file)
    return Path(settings.MEDIA_ROOT) / path
