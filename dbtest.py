
from veracitor.database import *

import datetime

def generate_test_data():

    nm = networkModel.get_global_network()

    trust = extractor.get_tag_create_if_needed("Trust")

    prod1 = extractor.producer_create_if_needed("Prod1", "TestProducer")
    prod2 = extractor.producer_create_if_needed("Prod2", "TestProducer")

    prod1.source_ratings = [producer.SourceRating(rating=5,tag=trust,source=prod2)]
    prod1.save()

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
