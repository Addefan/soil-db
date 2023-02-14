import datetime
import xlsxwriter


def queryset_to_workbook():
    workbook = xlsxwriter.Workbook("example.xlsx")
    worksheet = workbook.add_worksheet()
    workbook.close()


if __name__ == "__main__":
    queryset_to_workbook()
