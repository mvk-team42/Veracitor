from mongoengine import *
<<<<<<< HEAD
#from tag import Tag
#from tag import TagValidStrings
import tag
import producer
import user
import information
import datetime
import group

"""Just some test scripts."""

connect('mydb')

for t in tag.Tag.objects:
    t.delete()

tag1 = tag.Tag(description="Hurrr HURRRRRR")
tag1.name = "Gardening"
tag1.save()

tag2 = tag.Tag(description="HurrrDiDurr")
tag2.name = "Gardening"
tag2.parent.append(tag1)
tag2.save()

for t in tag.Tag.objects: 
    print t.name

for prod in producer.Producer.objects:
    prod.delete()

p1 = producer.Producer(name="DN", description="Swedeish nespaper", url="dn.se", 
                       type_="newspaper")

p2 = producer.Producer(name="SvD", description="Swedeish nespaper", url="svd.se", 
                       type_="newspaper")

u1 = user.User(name="goran", password="123")


p1.save()
p2.save()
u1.save()

for info in information.Information.objects:
    info.delete()

i1 = information.Information(name="dnledare",
                             description="hurr durr",
                             time_published=datetime.datetime.now(),
                             tags=[tag1],
                             publishers=[p1],
                             url = "dn.se")

i2 = information.Information(name="dnledare2",
                             description="hurr durr",
                             time_published=datetime.datetime.now(),
                             tags=[tag2],
                             publishers=[p1],
                             url="dn.se")

i1.save()
i2.save() 

for info in information.Information.objects:
    print info.name
=======
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
>>>>>>> First EntityModel
