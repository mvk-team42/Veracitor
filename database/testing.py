import unittest
from mongoengine import *
import tag
import producer
import user
import information
import group
import extractor
import datetime

connect('mydb')

class GeneralSetup(unittest.TestCase):
    
    def setUp(self):

        self.tearDown()

        self.tag1 = tag.Tag(name="Gardening", 
                            description="Hurrr HURRRRRR")
        self.tag1.save()
        
        self.tag2 = tag.Tag(name="Cooking",
                            description="Hurrdidurr")
        self.tag2.parent.append(self.tag1)
        self.tag2.save()
        
        self.user1 = user.User(name="Lasse", password="123")
        self.user1.save()

        self.group1 = group.Group(name="KTH",
                                  owner=self.user1,
                                  tags=[self.tag1, self.tag2],
                                  time_created=datetime.\
                                      datetime.now())
        self.info1 = information.Information(name="dnledare",
                                             url="dn.se/ledare",
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag1])
        self.info2 = information.Information(name="SvDledare",
                                             url="svd.se/ledare",
                                             references=[self.info1],
                                             time_punlished=datetime.datetime.now(),
                                             tags=[self.tag1, self.tag2])
        self.prod1 = producer.Producer(name="DN",
                                       type_="newspaper")
        self.prod2 = producer.Producer(name="SvD",
                                       type_="newspaper")
        self.info_rating1 = producer.InformationRating(rating=4, 
                                                       information=self.info1)
        self.prod2.info_ratings.append(self.info_rating1)
        self.group1.save()
        self.info1.save()
        self.info2.save()
        self.prod1.save()
        self.prod2.save()
                                                       
                                                       
    def tearDown(self):
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

class TestTagThings(GeneralSetup):

    def test_tag_model(self):
        assert self.tag2.parent[0].name == "Gardening"
        assert tag.Tag.objects(name="Cooking")[0].parent[0].\
            name == "Gardening"

    def test_tag_extractor(self):
        assert self.tag1 == extractor.get_tag("Gardening")
        assert self.tag1 in extractor.get_all_tags() and\
            self.tag2 in extractor.get_all_tags()

    def test_tag_group(self):
        assert self.tag1 in self.group1.tags

class TestInformationThings(GeneralSetup):
    def test_info_extractor(self): 
        date1 = datetime.datetime(year=1970, month=12, day=24)
        date2 = datetime.datetime(year=2017, month=12, day=24)
        assert self.info1 in extractor.search_informations("d", [self.tag1],
                                             date1, date2)
                                         
class TestProducerThings(GeneralSetup):
    
    def test_producer_extractor(self):
        assert self.prod1 in extractor.search_producers('dn', 'newspaper')
        assert self.prod2 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 not in extractor.search_producers('vd', 'newspaper')

if __name__ == "__main__":
    unittest.main()

