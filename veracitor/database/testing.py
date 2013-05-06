import unittest
from mongoengine import *
import networkModel
import tag
import producer
import user
import information
import group
import extractor
import datetime
import time
from dbExceptions import *
connect('testdb')

graph = None

class GeneralSetup(unittest.TestCase):
    
    def setUp(self):

        self.tearDown()
        
        self.tag1 = tag.Tag(name="Gardening")
        self.tag1.save()
        self.tag2 = tag.Tag(name="Cooking")
        self.tag2.save()
        self.tag2.parent.append(self.tag1)
        self.tag2.save()
        
        self.user1 = user.User(name="alfred", password="123")
        self.user1.save()
        self.user1.create_group("Group1", "Gardening")
        self.user1.save()

        self.user2 = user.User(name="fredrik", password="123")
        self.user2.save()
        self.user2.create_group("Group2", "Cooking")
        self.user2.save()
        
        self.group1 = extractor.get_group(self.user1.name,"Group1")
       
        self.info1 = information.Information(title="dn_ledare1", url="www.dn.se",
                                             time_published=datetime.datetime.now())
        self.info1.tags.append(self.tag1)
        self.info1.save()
        self.info2 = information.Information(title="svd_ledare1", url="www.svd.se",
                                             time_published=datetime.datetime.now())
        self.info3 = information.Information(title="cnn_article", url="www.cnn.com",
                                             time_published=datetime.datetime.now())
        self.info2.tags.append(self.tag1) 
        self.info2.tags.append(self.tag2)          
        self.info2.save()
        self.info3.tags.append(self.tag2)
        self.info3.save()

        self.prod1 = producer.Producer(name="DN", type_of="newspaper")
        self.prod1.save() 
        self.prod2 = producer.Producer(name="SvD", type_of="newspaper")
        self.prod2.save()
        self.prod3 = producer.Producer(name="Aftonbladet", type_of="newspaper")
        self.prod3.save()
        self.prod3.rate_source(self.prod2, self.tag2, 5)
        self.prod3.save()

        self.prod1.rate_source(self.prod2, self.tag1, 2)

        self.group1.producers.append(self.prod1)
        self.group1.save()

        self.prod1.rate_information(self.info1, 5)
        self.prod2.rate_information(self.info1, 4)  
        self.prod3.rate_information(self.info1, 3)   
        self.prod1.save()
        self.prod2.save()             
        self.prod3.save()

        self.prod4 = producer.Producer(name="Expressen", type_of="newspaper")
        self.prod4.save()
        self.prod4.rate_information(self.info1, 1)
        self.prod4.rate_information(self.info2, 2)
        self.prod4.rate_information(self.info3, 6)
        self.prod4.save()
        

    def tearDown(self):
        networkModel.build_network_from_db()
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
        assert extractor.contains_tag(self.tag1.name) == True
        assert extractor.contains_tag("Not a tag!") == False

class TestInformationThings(GeneralSetup):
    
    def test_info_extractor(self): 
        date1 = datetime.datetime(year=1970, month=12, day=24)
        date2 = datetime.datetime(year=2017, month=12, day=24)
        
        assert self.info1 in extractor.search_informations("d", [self.tag1],
                                                           date1, date2)
        assert extractor.contains_information(self.info1.url) == True
        assert extractor.contains_information("DEUS EX!!!") == False
        self.assertRaises(Exception, extractor.get_information, "Woo")

class TestProducerThings(GeneralSetup):
    
    def test_producer_extractor(self):
        assert self.prod1 in extractor.search_producers('dn', 'newspaper')
        assert self.prod2 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 not in extractor.search_producers('vd', 'newspaper')
        assert extractor.contains_producer_with_name(self.prod1.name) == True
        assert extractor.contains_producer_with_name("Should not exist!") == False

class TestGroupThings(GeneralSetup):
    
    def test_group_extractor(self):
        assert extractor.contains_group(self.user1.groups[0].name) == True        
        assert extractor.contains_group("Not a group!!") == False
        
        assert extractor.get_group(self.group1.owner.name, self.group1.name).producers[0]\
            == self.prod1
        
        self.assertRaises(Exception, extractor.get_group, "Hurrman", self.group1.name)
        
        assert self.user1.create_group("GHURR", "Gardening") == True
        
        assert self.user1.create_group("GHURR", "Gardening") == False
        
        assert self.user1.rate_group(str(self.group1.name), 1) == True
        assert self.user1.rate_group("Group2", 1) == False
       
class TestNetworkModelThings(GeneralSetup):

    def test_get_overall_difference(self):
        print networkModel.get_overall_difference(self.prod2.name, self.prod3.name,
                                                    [self.tag1.name, self.tag2.name])\
                                                    == 3
    
    def test_global_info_ratings(self):
        #print self.prod1.get_info_rating(self.info1)
        #print self.prod2.get_info_rating(self.info1)
        #print self.prod1.info_ratings
        #print self.prod2.info_ratings
        assert networkModel.get_common_info_ratings(self.prod1.name, self.prod2.name,[self.tag1.name])\
            == [(self.prod1.get_info_rating(self.info1), self.prod2.get_info_rating(self.info1))]
        assert networkModel.get_common_info_ratings(self.prod1.name, self.prod2.name,[self.tag2.name])\
            == []
        
        assert networkModel.get_common_info_ratings(self.prod1.name, self.prod3.name,[self.tag1.name, self.tag2.name])\
            == [(self.prod1.get_info_rating(self.info1), self.prod3.get_info_rating(self.info1))]
        
        assert networkModel.get_common_info_ratings(self.prod2.name, self.prod3.name,[self.tag2.name])\
            == []
        
        
        assert networkModel.get_overall_difference(self.prod1.name, self.prod2.name, [self.tag1.name])\
            == 1.0
        assert networkModel.get_extreme_info_ratings(self.prod4.name, [self.tag1.name, self.tag2.name])\
            == {self.info3.url : 6}

        assert networkModel.get_max_rating_difference(self.prod1.name, self.prod4.name, [self.tag1.name, self.tag2.name])\
            == 4

    

if __name__ == "__main__":
    unittest.main()


