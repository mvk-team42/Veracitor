
from database import *

def generate_test_data():
    tag1 = tag.Tag(name="Gardening", description="Hurrr HURRRRRR")
    tag1.save()
    
    tag2 = tag.Tag(name="Cooking", description="Hurrdidurr")
    tag2.parent.append(tag1)
    tag2.save()
    
    user1 = user.User(name="Lasse", password="123")
    user1.save()

    group1 = group.Group(name="KTH", owner=user1, tags=[tag1, tag2],
                            time_created=datetime.datetime.now())
    info1 = information.Information(name="dnledare",url="dn.se/ledare",
                                         time_published=datetime.datetime.now(),
                                         tags=[tag1])
    info2 = information.Information(name="SvDledare",
                                         url="svd.se/ledare",
                                         references=[info1],
                                         time_punlished=datetime.datetime.now(),
                                         tags=[tag1, tag2])
    prod1 = producer.Producer(name="DN", type_="newspaper")
    prod2 = producer.Producer(name="SvD", type_="newspaper")
    info_rating1 = producer.InformationRating(rating=4, information=info1)
    prod2.info_ratings.append(info_rating1)
    group1.save()
    info1.save()
    info2.save()
    prod1.save()
    prod2.save()

