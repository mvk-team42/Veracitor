
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
    prod7 = extractor.producer_create_if_needed("Prod7", "TestProducer")

    john.first_name = 'John'
    john.last_name = 'Turesson'
    john.description = 'John Turesson is a web developer in the Veracitor project managed by Team 42, created in the mvk project at KTH.'
    john.url = 'http://www.nada.kth.se/~johntu/'
    john.email = 'johntu@kth.se'
    john.rate_source(prod1, trust, 5)
    john.save()

    prod1.rate_source(prod2, trust, 5)
    try:
        prod1.infos = [information.Information(title='Info1',url='www.info1.com').save(),
                       information.Information(title='Info2',url='www.info2.com').save()]
    except:
        pass

    prod2.rate_source(prod1, trust, 5)
    prod2.rate_source(prod3, trust, 5)
    prod2.rate_source(prod4, trust, 5)
    prod2.rate_source(prod5, trust, 5)
    try:
        prod2.infos = [information.Information(title='Info3',url='www.info3.com').save(),
                       information.Information(title='Info4',url='www.info4.com').save(),
                       information.Information(title='Info5',url='www.info5.com').save()]
    except:
        pass

    prod3.rate_source(prod1, trust, 5)
    prod3.rate_source(prod5, trust, 5)
    prod3.rate_source(prod6, trust, 5)
    prod3.rate_source(prod7, trust, 5)
    try:
        prod3.infos = [information.Information(title='Info6',url='www.info6.com').save(),
                       information.Information(title='Info7',url='www.info7.com').save(),
                       information.Information(title='Info8',url='www.info8.com').save(),
                       information.Information(title='Info9',url='www.info9.com').save()]
    except:
        pass

    prod5.rate_source(prod2, trust, 5)
    prod5.rate_source(prod3, trust, 5)
    prod5.rate_source(prod4, trust, 5)

    prod6.rate_source(prod5, trust, 5)

    prod7.rate_source(prod3, trust, 5)

    prod1.save()
    prod2.save()
    prod3.save()
    prod5.save()
    prod6.save()
    prod7.save()

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
