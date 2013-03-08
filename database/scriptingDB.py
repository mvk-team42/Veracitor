from mongoengine import *
#from tag import Tag
#from tag import TagValidStrings
import tag

"""Just some test scripts."""

connect('mydb')

for tvs in tag.TagValidStrings.objects:
    tvs.delete()

tvs = tag.TagValidStrings(valid_strings=["Gardening"])
tvs.name = "Master"
tvs.save()

for shit in tag.TagValidStrings.objects:
    print shit.name

for t in tag.Tag.objects:
    t.delete()

tag1 = tag.Tag(description="Hurrr HURRRRRR")
tag1.set_name("Gardening")
tag1.save()

tag2 = tag.Tag(description="HurrrDiDurr")
tag2.set_name("Gardening")
tag2.parent.append(tag1)
tag2.save()

for t in tag.Tag.objects: 
    print t.get_name()
