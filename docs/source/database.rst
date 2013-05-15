
:mod:`database`
====================================================
Handles all database interactions

:mod:`extractor` 
---------------------------------------------------------
Specifies functionality to communicate with a database which uses MongoDB.
Enables extraction of entities.

.. automodule:: veracitor.database.extractor
   :members:

:mod:`user`
----------------------------
The user module contains the class needed 
to represent the user entity model. 
Class methods enable functionality related to the user entity.

.. automodule:: veracitor.database.user
   :members:

:mod:`networkModel`
-------------------------------------------------------------------------------------
The purpose of the network model is to ease the accessing of the database
through building a NetworkX DiGraph. Defines a set of convenience
functions performing tasks related to traversing data in the database.

.. automodule:: veracitor.database.networkModel
   :members:

:mod:`group`
------------------------------
The group module contains the Group class needed 
to represent the group entity model.

.. automodule:: veracitor.database.group
   :members:

:mod:`information`
------------------------------------------
The information module contains the Information class needed to represent the information entity model.

.. automodule:: veracitor.database.information
   :members:

:mod:`producer`
------------------------------------
The producer module contains the class needed 
to represent the producer entity model.
Class methods enable functionality related to the producer entity.

.. automodule:: veracitor.database.producer
   :members:

:mod:`tag`
--------------------------
The tag module contains the Tag class needed to represent the tag entity model.

.. automodule:: veracitor.database.tag
   :members:

:mod:`dbExceptions`
-----------------------------------------------------------------------
Exceptions for the database interaction

.. automodule:: veracitor.database.dbExceptions
   :members:
