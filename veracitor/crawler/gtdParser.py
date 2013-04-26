import openpyxl.reader.excel
import openpyxl.workbook as workbook
from pprint import pprint
from time import strptime
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
    new_producer = producer.Producer(
            name = _GTD_PRODUCER_NAME,
            description = "Global Terrorism Database",
            url = "http://www.start.umd.edu/gtd/",
            infos = [],
            source_ratings = [],
            type_of = "Database")
    new_producer.save()



def parseGTD(filepath, **kwargs):
    workbook = openpyxl.reader.excel.load_workbook(filepath, use_iterators=True)
    sheet = workbook.get_active_sheet()
    acts = _parse_sheet(sheet, **kwargs)
    acts = acts[1:] #Labels on first row
    terrorism_tag = safe_get_tag("Terrorism")

    for act in acts:
        act_url = _GTD_INCIDENT_URL + act["id"]
        act_tag = safe_get_tag(act["attacktype"])

        sources = [ _strip_source(src) for src in [act["source1"], act["source2"], act["source3"]] if src != None]

        GTD = extractor.get_producer(_GTD_PRODUCER_NAME)

        for source in sources:
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


            source_rating1 = producer.SourceRating(
                    rating = 5,
                    tag = terrorism_tag,
                    source = source)

            source_rating2 = producer.SourceRating(
                    rating = 5,
                    tag = act_tag,
                    source = source)

            # Borde kolla innan!!!!!
            GTD.source_ratings += [source_rating1,source_rating2]

            GTD.save()

        if not extractor.contains_information(act_url):
            #add...
            new_information = information.Information(url = act_url),
                title = "GTD Entry",
                summary = act["summary"],
                time_published = strptime(act["year"]+"-"+act["mont"]+"-"+act["day"],"%Y-"),
                tags = [terrorism_tag, act_tag],
                publishers = ["GTD"] + sources,
                references =  [])

def safe_get_tag(name):
    try:
        return extractor.get_tag(name)
    except:
        new_tag = tag.Tag(
                name = name,
                valid_strings = [name])
        new_tag.save()
        return new_tag


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
            if cell.column in _column_names:
                if cell.internal_value == None:
                    act[_column_names[cell.column]] = None
                else:
                    act[_column_names[cell.column]] = unicode(cell.internal_value)
        acts.append(act)
        if print_acts:
            print act
    return acts
    
def _strip_source(source):
    source = source.split('"')[-1]
    source = source.split(',')[0]
    return source
    
    
if __name__ == "__main__":
    add_GTD_to_database()
    add_terrorism_tag()
    acts = parseGTD('Downloads/globalterrorismdb_1012dist.xlsx', limit_number_rows = 4)
    pprint(acts)
