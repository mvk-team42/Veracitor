from datetime import datetime

class Level:
    debug = 0
    warning = 1
    
class Area:
    crawler = 0
    algorithms = 1
    web = 2  
    database = 3
    valid_areas = [crawler, algorithms, web, database]
    strings = ["crawler", "algorithms", "web", "database"]

def log(message, level, area):
    if level == Level.warning:
        _log_warning(message, area)
    else:
        _log_debug(message, area)      
        
def _log_warning(message, area):
    f = open("warnings.log", "a")
    f.write(str(datetime.now()) + " [" + Area.strings[area] + "]: " + message + "\n")
    f.close()
           
def _log_debug(message, area):
    if area in Area.valid_areas:
        f = open(Area.strings[area] + "debug.log", "a")
    else:
        raise Exception("Invalid area")
    f.write(str(datetime.now()) + ": " + message + "\n")
    f.close()   
    
def clear_log(level, area=None):
    if level == Level.warning:
        _clear_file("warnings.log")
    elif level == Level.debug:
        if area in Area.valid_areas:
            _clear_file(Area.strings[area] + "debug.log")
        else:
            raise Exception("have to set area when clearing debug")
    
def _clear_file(fname):
    f = open(fname, "w")
    f.write("")
    f.close()
    
