import openpyxl.reader.excel
import openpyxl.workbook as workbook
from pprint import pprint
from datetime import datetime
from time import strptime, mktime
from os.path import realpath, dirname
import sys
from ..database import *

_GTD_INCIDENT_URL = "http://www.start.umd.edu/gtd/search/IncidentSummary.aspx?gtdid="
_GTD_PRODUCER_NAME = "GTD"

_column_names = {
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

def add_GTD_to_database():
    if not extractor.contains_producer_with_name(_GTD_PRODUCER_NAME):
        new_producer = producer.Producer(
                name = _GTD_PRODUCER_NAME,
                description = "Global Terrorism Database",
                url = "http://www.start.umd.edu/gtd/",
                type_of = "Database")
        new_producer.save()

def parseGTD(filepath, **kwargs):
    workbook = openpyxl.reader.excel.load_workbook(filepath, use_iterators=True)
    sheet = workbook.get_active_sheet()
    acts = _parse_sheet(sheet, **kwargs)
    
    GTD = extractor.get_producer(_GTD_PRODUCER_NAME)

    for act in acts:
        _save_act_in_gtd_object(act,GTD)
    
    try:
        GTD.save()
    except:
        print "EXCEPTION! Printing infos"
        for info in GTD.infos:
            print unicode(info)
        sys.exit()

def _save_act_in_gtd_object(act,gtd_producer):
    act_url = _GTD_INCIDENT_URL + act["id"]
    act_tag = _safe_get_tag(act["attacktype"])
    source_strings = [ _strip_source(src) for src in [act["source1"], act["source2"], act["source3"]] if src != None]
    sources = []

    if act["summary"] == None:
        act["summary"] = act["attacktype"] + " - ATTACKER: " + act["attacker"] + " - TARGET: " + act["target"]

    for source_string in source_strings:
        source = None
        if not extractor.contains_producer_with_name(source_string): #db-method
            source = producer.Producer(name = source_string,
                description = "No description. (found through GTD)",
                url = None,
                type_of = "Unknown")
                
            source.save()
            sources.append(source)
        else:
            source = extractor.get_producer(source_string)
            
        gtd_producer.rate_source(source, terrorism_tag, 5)
        gtd_producer.rate_source(source, act_tag, 5)

    if not extractor.contains_information(act_url):
        information_object = information.Information(url = act_url,
            title = "GTD Entry",
            summary = act["summary"],
            time_published = _get_datetime(act),
            tags = [terrorism_tag, act_tag],
            publishers = [gtd_producer] + sources,
            references =  [])
        information_object.save()
    else:
        information_object = extractor.get_information(act_url)

    print "information type: " + str(type(information_object))

    gtd_producer.infos.append(information_object)
    print "saved act: " + str(act["summary"])

def _safe_get_tag(name):
    try:
        return extractor.get_tag(name)
    except:
        new_tag = tag.Tag(
                name = name,
                valid_strings = [name])
        new_tag.save()
        return new_tag

def _get_datetime(act):
    year = int(float(act["year"]))
    month = min(max(int(float(act["month"])),1),12)
    day = min(max(int(float(act["day"])), 1), 31)
    datetime.fromtimestamp(mktime(strptime(year+"-"+month+"-"+day,"%Y-%m-%d")))


""" 
    Receives a openpyxl.reader.iter_worksheet, parses it and returns a list of 
    terrorist-acts where every act is represented as a dict of attributes
"""
def _parse_sheet(sheet, limit_number_rows = 0, print_acts = False):
    row_number = 1
    for row in sheet.iter_rows():
        if row_number == 1
            continue
        if limit_number_rows == row_number:
            break
        act = {}
        for cell in row:
            if cell.column in _column_names:
                if cell.internal_value == None:
                    act[_column_names[cell.column]] = None
                else:
                    act[_column_names[cell.column]] = unicode(cell.internal_value)
        yield act
        if print_acts:
            print act
    
def _strip_source(source):
    source = source.split('"')[-1]
    source = source.split(',')[0]
    return source
    
    
if __name__ == "__main__":
    parse()

def parse():
    global terrorism_tag
    terrorism_tag = _safe_get_tag("Terrorism")
    add_GTD_to_database()

    current_dir = dirname(realpath(__file__))
    acts = parseGTD(current_dir + '/globalterrorismdb_1012dist.xlsx', limit_number_rows = 0)
    pprint(acts)
