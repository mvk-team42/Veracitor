from mongoengine import *
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
tag2.name = "Cooking"
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
