import os
import django
import xlsxwriter

from datetime import datetime
from xlsxwriter import Workbook
from django.db.models import QuerySet

from soil.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soil.settings")
django.setup()

from web.models import Plant


def create_media_xlsx_directory() -> None:
    if not os.path.exists(f"{BASE_DIR}/media/xlsx"):
        os.mkdir(f"{BASE_DIR}/media/xlsx")


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

    now = datetime.now()
    path = f"{BASE_DIR}/media/xlsx/{now.strftime('%M_%H_%d_%m_%Y')}.xlsx"
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

    # writing objects
    for x, obj in enumerate(objects, start=1):
        for y, column in enumerate(headers):
            if type(obj[column]) == str:
                sheet.write_string(x, y, obj[column], cell_format=simple_format)
            elif type(obj[column]) == int or type(obj[column]) == float:
                sheet.write_number(x, y, obj[column], cell_format=simple_format)
            elif type(obj[column]) == bool:
                sheet.write_boolean(x, y, obj[column], cell_format=simple_format)
            elif type(obj[column]) == datetime:
                sheet.write_datetime(x, y, obj[column], cell_format=date_format)
            else:
                raise TypeError(f"Uncultivited type: {type(obj[column])}")

    sheet.autofit()
    workbook.close()

    return path


if __name__ == "__main__":
    queryset_to_xlsx(Plant.objects.all())
