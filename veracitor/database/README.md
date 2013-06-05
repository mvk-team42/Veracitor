The Database Package
===================

Contains all modules neccessary to communicate with the database.
Also includes the convenience structure networkModel. Changes made directly to
the graph in networkModel will not affect the database.

To import this package simply do 
```Python
from database import *
```
(where database is the folder with the "__init__.py" defining the package).

Dependencies
------------

Needs <b>MongoDB</b> installed, with a mongo server running locally.

Also needs the Python object-document mapper <b>MongoEngine</b>.

Entitymodels
-----------------

The database entities are made up of the following modules:

#####producer
#####user
#####information
#####tag
#####group


To insert a new object into the database, create corresponding entitymodel
(producer, information etc...) and call .save(). The graph in networkModel is automatically
updated by this call. To remove, call .delete().

Example usage:

```Python
test = producer.Producer(name="TestProd", type_of="test")
test.save()
```

Above code inserts the producer TestProd into the database.

Networkmodel
------------

To obtain the graph in networkModel object call get_global_network from the networkModel module.
Forcing an update of the graph can be done by calling build_network_from_db.
