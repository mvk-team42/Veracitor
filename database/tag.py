from mongoengine import *

connect('mydb')

class TagValidStrings(Document):
    name = StringField()
    valid_strings = ListField(StringField())

class Tag(Document):
    """Provides public fields (except _name)
    mirroring underlying database object.
    Call save() to update database,
    delete() to delete object from database.
    
    """
    
    def set_name(self, new_name):
        """Changes name of Tag if new_name is valid.
        Returns true if change was successful,
        otherwise False.
           
        """
        if(new_name in TagValidStrings.objects(name="Master")[0].valid_strings):
            self._name = new_name
            return True
        else:
            return False
    def get_name(self):
        return self._name
            
    # Private because constrained by valid_strings.
    _name = StringField(required=True)
    description = StringField()
    parent = ListField(ReferenceField('self'))


