
from veracitor.web import app

app.callback_id_counter = 0
app.callback_ids = {}

"""
Returns a unique crawl procedure  id.
"""
def get_unique_id():
    id = '#' + str(app.callback_id_counter)
    app.callback_ids[id] = None

    app.callback_id_counter += 1
    return id

"""
Sets an item for the specified id.
"""
def set_item(id, item):
    app.callback_ids[id] = item

"""
Returns the item related to the given crawl procedure id.
If an item has been set the id is removed from the dict.
"""
def check_id(id):
    item = app.callback_ids[id]

    if item:
        del app.callback_ids[id]

    return item
