
from veracitor.web import app

# crawler variables
app.crawl_id_counter = 0
app.crawl_ids = {}

"""
Callback function for the crawler
"""
def crawl_callback(item, id):
    app.crawl_ids[id] = item

"""
Returns a unique crawl procedure  id.
"""
def get_unique_crawl_id():
    id = '#' + str(app.crawl_id_counter)
    app.crawl_ids[id] = None

    app.crawl_id_counter += 1
    return id
"""
Returns the item related to the given crawl procedure id.
"""
def get_crawl_id_item(id):
    return app.crawl_ids[id]
