import openpyxl.reader.excel
import openpyxl.workbook as workbook
from pprint import pprint
from time import strptime
from ..database import *

GTD_INCIDENT_URL = "http://www.start.umd.edu/gtd/search/IncidentSummary.aspx?gtdid="

column_names = {
    "A":"id",
    "B":"year",
    "C":"month",
    "D":"day",
    "I":"country",
    "S":"summary",
    "DP":"source1",
    "DQ":"source2",
    "DR":"source3",
    "AD":"attacktype",
    "BA":"attacker",
    "AL":"target",
}


def parseGTD(filepath, **kwargs):
    workbook = openpyxl.reader.excel.load_workbook(filepath, use_iterators=True)
    sheet = workbook.get_active_sheet()
    acts = _parse_sheet(sheet, **kwargs)
    acts = acts[1:] #Labels on first row
    for act in acts:
        acturl = GTD_INCIDENT_URL + act["id"]
        raw_sources = [act["source1"], act["source2"], act["source3"]]
        for source in raw_sources:
            # hur blir det om source == None?
            #TODO gör koppling mellan GTD och denna source
            if not extractor.contains_producer_with_name(source): #db-method
                    new_producer = producer.Producer(name = source,
                        description = "No description. (found through GTD)",
                        url = None,
                        infos = [],
                        source_ratings = [],
                        info_ratings = [],
                        type_of = "Unknown")
                    new_producer.save()

        if not extractor.contains_information(acturl):
            new_information = information.Information(url = acturl),
                title = "GTD Entry",
                summary = act["summary"],
                time_published = strptime(act["year"]+"-"+act["mont"]+"-"+act["day"],"%Y-"),
                tags = ["Terrorism"],
                publishers = ["GTD"] + [_strip_source(src) for src in raw_sources if src != None],
                references =  [])


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
    
def _strip_source(source):
    source = source.split('"')[-1]
    source = source.split(',')[0]
    return source
    
    
if __name__ == "__main__":
    acts = parseGTD('Downloads/globalterrorismdb_1012dist.xlsx', limit_number_rows = 4)
    pprint(acts)
