import openpyxl


def sku_reader(path: str) -> list:
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    products = [cell.value for cell in sheet["A"] if cell.value is not None]
    return products
