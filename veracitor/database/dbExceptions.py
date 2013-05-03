"""
.. module:: dbExceptions
    :synopsis: Collection of exceptions used to indicate database errors.

"""

class NetworkModelException(Exception):
    """
    Exception to be used when an error occurs in the global network.

    """
    pass

class NotInDatabase(Exception):
    """
    Exception to be used when important to indicate that
    requested item is not present in the database.
    
    
    """
    pass

class AlreadyExists(Exception):
    """
    Exception to be used when trying to add a duplicate of something
    that is meant to be unique.
    
    """
    pass
