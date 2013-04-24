import openpyxl.reader.excel
import openpyxl.workbook as workbook
from pprint import pprint



column_names = {
    "B":"year",
    "C":"month",
    "D":"day",
    "I":"country",
    "S":"summary",
    "DP":"source",
    "AD":"attacktype",
    "BA":"attacker",
    "AL":"target",
}


def parseGTD(filepath, **kwargs):
    workbook = openpyxl.reader.excel.load_workbook(filepath, use_iterators=True)
    sheet = workbook.get_active_sheet()
    acts = _parse_sheet(sheet, **kwargs)
    return acts[1:] #Labels on first row


""" 
    Receives a openpyxl.reader.iter_worksheet, parses it and returns a list of 
    terrorist-acts where every act is represented as a dict of attributes
"""
def _parse_sheet(sheet, limit_number_rows = 0, print_acts = False):
    acts = []
    for row in sheet.iter_rows():
        act = {}
        for cell in row:
            if limit_number_rows > 0 and cell.row > limit_number_rows:
                return acts
            if cell.column in column_names:
                if cell.internal_value == None:
                    act[column_names[cell.column]] = None
                else:
                    act[column_names[cell.column]] = unicode(cell.internal_value)
        acts.append(act)
        if print_acts:
            print act
    return acts
    
    
if __name__ == "__main__":
    acts = parseGTD('Downloads/globalterrorismdb_1012dist.xlsx', limit_number_rows = 4)
    pprint(acts)
