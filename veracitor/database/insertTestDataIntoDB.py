from mongoengine import *
import globalNetwork
import producer
import information
import user
import information
import group
import tag
import extractor
import datetime
connect('mydb')

if __name__ == "__main__":
    globalNetwork.build_network_from_db()
    tag1 = tag.Tag(name="Gardening",
                            description="Hurrr HURRRRRR")
    tag1.save()

    tag2 = tag.Tag(name="Cooking",
                            description="Hurrdidurr")
    tag2.parent.append(tag1)
    tag2.save()

    user1 = user.User(name="Lasse", password="123")
    user1.save()

    group1 = group.Group(name="KTH",
                         owner=user1,
                         tags=[tag1, tag2],
                         time_created=datetime.\
                             datetime.now())

    info1 = information.Information(title="dnledare",
                                    url="dn.se/ledare",
                                    time_published=datetime.datetime.now(),
                                    tags=[tag1])
    info2 = information.Information(title="SvDledare",
                                    url="svd.se/ledare",
                                    references=[info1],
                                    time_punlished=datetime.datetime.now(),
                                    tags=[tag1, tag2])
    prod1 = producer.Producer(name="DN",
                                       type_of="newspaper")
    prod2 = producer.Producer(name="SvD",
                                       type_of="newspaper")
    info_rating1 = producer.InformationRating(rating=4,
                                              information=info1)
    source_rating1 = producer.SourceRating(rating=3, source=prod2,
                                           tag=tag1)
    prod2.info_ratings.append(info_rating1)
    prod1.source_ratings.append(source_rating1)
    group1.save()
    info1.save()
    info2.save()
    prod2.save()
    prod1.save()

    
