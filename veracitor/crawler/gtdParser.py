# -*- coding: utf-8 -*-

""" 
.. module:: gtdParser
    :synopsis: A module for parsing an excel file representation of the GTD-databse. Is probably used only once to gather a big amount of data for the database. Later on in the product lifetime new data will instead be added from the webcrawler.

.. moduleauthor:: Gustaf Lindstedt <glindste@kth.se>
.. moduleauthor:: Jonathan Murray <jmu@kth.se>
"""
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
    """
    Adds the GTD-producer to the database.

    Returns:
        None
    """
    if not extractor.contains_producer_with_name(_GTD_PRODUCER_NAME):
        new_producer = producer.Producer(
                name = _GTD_PRODUCER_NAME,
                description = "Global Terrorism Database",
                url = "http://www.start.umd.edu/gtd/",
                type_of = "Database")
        new_producer.save()

def parseGTD(filepath, **kwargs):
    """
    The method containing the main loop for parsing the acts contained in the excel-file.

    Args:
        *filepath*: The filepath for the excel file.

    Kwargs:
        *limit_number_rows*: A number limiting the number of rows to be parsed. 0 means parse all.

    Returns:
        None
    """
    workbook = openpyxl.reader.excel.load_workbook(filepath, use_iterators=True)
    sheet = workbook.get_active_sheet()
    acts = _parse_sheet(sheet, **kwargs)
    print "Sheet parsed"
    
    GTD = extractor.get_producer(_GTD_PRODUCER_NAME)

    print "before loop"
    for act in acts:
        print "processing act"
        _save_act_in_gtd_object(act,GTD)
    print "after loop"

    try:
        GTD.save()
    except:
        print "EXCEPTION! Printing infos"
        for info in GTD.infos:
            print unicode(info)
        sys.exit()

def _save_act_in_gtd_object(act,gtd_producer):
    """
    Saves the act in the first argument to the producer object in the second argument.

    Args:
        *act*: The act to be saved.

        *gtd_producer*: The producer (GTD) to save the act in.

    Returns:
        None
    """
    act_url = _GTD_INCIDENT_URL + act["id"]
    act_tag = _safe_get_tag(act["attacktype"])
    source_strings = [ _strip_source(src) for src in [act["source1"], act["source2"], act["source3"]] if src != None]
    sources = []

    _fix_summary(act)

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

    print "information type: " + unicode(type(information_object)).encode(encoding="utf-8", errors="replace")

    gtd_producer.infos.append(information_object)
    print "saved act: " + unicode(act["summary"]).encode(encoding="utf-8", errors="replace")

def _safe_get_tag(name):
    """
    Gets the tag object for the tag with the name given as argument.
    Create it if it does not exist.

    Args:
        *name*: The requested tag name.

    Returns:
        A tag object with the name given as argument.
    """
    try:
        return extractor.get_tag(name)
    except:
        new_tag = tag.Tag(
                name = name,
                valid_strings = [name])
        new_tag.save()
        return new_tag

def _fix_summary(act):
    """
    Constructs a summary of the act if the summary field is missing.

    Args:
        *act*: A dict representing an act.

    Returns:
        None
    """
    if act["summary"] == None:
        act["summary"] = _safe_get_string(act["attacktype"]) + " - ATTACKER: " + _safe_get_string(act["attacker"]) + " - TARGET: " + _safe_get_string(act["target"])

def _safe_get_string(string):
    """
    Ensures that a string has a value, sets it to 'unknown' if type is None.

    Args:
        *string*: A variable that supposedly is a string, but might be None.

    Returns:
        A string.
    """
    if string == None:
        return "unknown"
    return string

def _get_datetime(act):
    """
    Parse the date and time of the act.

    Args:
        *act*: A dict representing an act.

    Returns:
        A datetime object.
    """
    year = int(float(act["year"]))
    month = min(max(int(float(act["month"])),1),12)
    day = min(max(int(float(act["day"])), 1), 31)
    return datetime.fromtimestamp(mktime(strptime(unicode(year)+"-"+unicode(month)+"-"+unicode(day),"%Y-%m-%d")))


""" 
    Receives a openpyxl.reader.iter_worksheet, parses it and returns a list of 
    terrorist-acts where every act is represented as a dict of attributes
"""
def _parse_sheet(sheet, limit_number_rows = 0, print_acts = False):
    """
    Parses the excel file and yields a generator for all the acts found within.

    Args:
        *sheet*: An initialized opnepyxl workbook sheet.

    Returns:
        *act*: A generator for the acts contained in the file.
    """
    row_number = 1
    for row in sheet.iter_rows():
        if row_number == 1:
            row_number += 1
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
        row_number += 1
    
def _strip_source(source):
    """
    Parses the source string and returns the relevant part of it.

    Args:
        *source*: The raw source string from the excel file.

    Returns:
        *source*: A string with the relevant information from the input.
    """
    source = source.split('"')[-1]
    source = source.split(',')[0]
    return source

def parse():
    """
    Starts parsing of the excel file.

    Returns:
        None
    """
    global terrorism_tag
    terrorism_tag = _safe_get_tag("Terrorism")
    add_GTD_to_database()

    current_dir = dirname(realpath(__file__))
    acts = parseGTD(current_dir + '/globalterrorismdb_1012dist.xlsx', limit_number_rows = 0)
    pprint(acts)
    
if __name__ == "__main__":
    parse()
