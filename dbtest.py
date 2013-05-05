
from veracitor.database import dbExceptions
from veracitor.database import *

import datetime

def generate_test_data():

    nm = networkModel.get_global_network()

    trust = extractor.get_tag_create_if_needed("Trust")

    try:
        john = extractor.get_producer('John')
    except dbExceptions.NotInDatabase:
        john = user.User(name='John',password='123')
        john.save()
    prod1 = extractor.producer_create_if_needed("Prod1", "TestProducer")
    prod2 = extractor.producer_create_if_needed("Prod2", "TestProducer")
    prod3 = extractor.producer_create_if_needed("Prod3", "TestProducer")
    prod4 = extractor.producer_create_if_needed("Prod4", "TestProducer")
    prod5 = extractor.producer_create_if_needed("Prod5", "TestProducer")
    prod6 = extractor.producer_create_if_needed("Prod6", "TestProducer")

    john.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod1)]
    john.save()
    prod1.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod2)]
    prod2.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod1),
                            producer.SourceRating(rating=5,tag=trust,source=prod3),
                            producer.SourceRating(rating=5,tag=trust,source=prod4),
                            producer.SourceRating(rating=5,tag=trust,source=prod5)]
    prod3.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod1),
                            producer.SourceRating(rating=5,tag=trust,source=prod5),
                            producer.SourceRating(rating=5,tag=trust,source=prod6)]
    prod5.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod2),
                            producer.SourceRating(rating=5,tag=trust,source=prod3),
                            producer.SourceRating(rating=5,tag=trust,source=prod4)]
    prod6.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod5)]
    prod1.save()
    prod2.save()
    prod3.save()
    prod5.save()
    prod6.save()

def tear_down():
    for t in tag.Tag.objects:
        t.delete()
        for p in producer.Producer.objects:
            p.delete()
        for u in user.User.objects:
            u.delete()
        for g in group.Group.objects:
            g.delete()
        for i in information.Information.objects:
            i.delete()

generate_test_data()
