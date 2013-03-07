from mongoengine import *
from Tag import Tag
from Tag import TagValidStrings
#import Tag

connect('mydb')

for tvs in TagValidStrings.objects:
    tvs.delete()

tvs = TagValidStrings(valid_strings=["Gardening"])
tvs.name = "Master"
tvs.save()

for shit in TagValidStrings.objects:
    print shit.name

for t in Tag.objects:
    t.delete()

tag = Tag(description="Hurrr HURRRRRR")
tag.set_name("Gardening")
tag.save()

tag2 = Tag(description="HurrrDiDurr")
tag2.set_name("Gardening")
tag2.parent.append(tag)
tag2.save()

for t in Tag.objects:
    print t.get_name()
