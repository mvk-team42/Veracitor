import unittest
from mongoengine import *
import globalNetwork
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

        self.graph = globalNetwork.build_network_from_db()

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
        self.info1 = information.Information(title="dnledare",
                                             url="dn.se/ledare",
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag1])
        self.info2 = information.Information(title="SvDledare",
                                             url="svd.se/ledare",
                                             references=[self.info1],
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag1, self.tag2])
        self.info3 = information.Information(title="AftonbladetEntertainment",
                                             url="aftonbladet.se/sksdfsd",
                                             references=[],
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag2])

        self.info4 = information.Information(title="EnDingDingVaerldArticle2",
                                             url="dfkdslfk-.com",
                                             references=[],
                                             time_published=datetime.datetime.now(),
                                             tags=[self.tag1, self.tag2])

        self.prod1 = producer.Producer(name="DN",
                                       type_of="newspaper")
        self.prod2 = producer.Producer(name="SvD",
                                       type_of="newspaper")
        self.prod3 = producer.Producer(name="Aftonbladet",
                                       type_of="newspaper")
        self.prod4 = producer.Producer(name="USSR",
                                       type_of="propaganda")
        self.prod5 = producer.Producer(name="FOX",
                                       type_of="network")
        self.info_rating1 = producer.InformationRating(rating=4, 
                                                       information=self.info1)
        self.info_rating2 = producer.InformationRating(rating=2,
                                                       information=self.info1)
        self.info_rating3 = producer.InformationRating(rating=1,
                                                       information=self.info2)
        self.info_rating4 = producer.InformationRating(rating=5,
                                                       information=self.info2)
        self.info_rating5 = producer.InformationRating(rating=3,
                                                       information=self.info3)
        self.info_rating6 = producer.InformationRating(rating=4,
                                                       information=self.info4)
        self.info_rating7 = producer.InformationRating(rating=5,
                                                       information=self.info4)

        self.prod2.save()
        self.source_rating1 = producer.SourceRating(rating=3,
                                                    source=self.prod2,
                                                    tag=self.tag1)
        
        self.prod1.info_ratings.append(self.info_rating1)
        self.prod2.info_ratings.append(self.info_rating2)
        self.prod2.info_ratings.append(self.info_rating3)
        self.prod3.info_ratings.append(self.info_rating4)
        self.prod3.info_ratings.append(self.info_rating5)
        self.prod3.info_ratings.append(self.info_rating1)
        self.prod3.info_ratings.append(self.info_rating6)
        self.prod4.info_ratings.append(self.info_rating7)

        self.prod1.source_ratings.append(self.source_rating1)
        self.group1.save()
        self.info1.save()
        self.info2.save()
        self.info3.save()
        self.info4.save()
        self.prod2.save()
        self.prod1.save()
        self.prod3.save()
        self.prod4.save()
        self.prod5.save()
        self.prod5.delete()
        self.prod1.delete()

        self.group1.producers.append(self.prod1)
        self.group1.producers.append(self.prod2)
        self.group1.producers.append(self.prod3)
        self.group1.save()

        multi = "Multi"
        self.prod_list = []
        for i in range(100):
            self.prod_list.append(producer.Producer(name=multi+str(i),
                                               type_of="TestPlaceHolder"))
            if i > 1:
                self.prod_list[i].source_ratings.append(producer.SourceRating(rating=1,
                                                                          tag=self.tag1,
                                                                          source=self.prod_list[i-1]))
        for i in range(len(self.prod_list)):
            self.prod_list[i].save()
          

    def tearDown(self):
        globalNetwork.build_network_from_db()
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

    def test_tag_group(self):
        assert self.tag1 in self.group1.tags

class TestInformationThings(GeneralSetup):
    def test_info_extractor(self): 
        date1 = datetime.datetime(year=1970, month=12, day=24)
        date2 = datetime.datetime(year=2017, month=12, day=24)
        
        assert self.info1 in extractor.search_informations("d", [self.tag1],
                                                           date1, date2)
        assert extractor.contains_information(self.info1.title) == True
        assert extractor.contains_information("DEUS EX!!!") == False
        self.assertRaises(Exception, extractor.get_information, "Woo")
                                         
class TestProducerThings(GeneralSetup):
    
    def test_producer_extractor(self):
        assert self.prod1 in extractor.search_producers('dn', 'newspaper')
        assert self.prod2 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 in extractor.search_producers('d', 'newspaper')
        assert self.prod1 not in extractor.search_producers('vd', 'newspaper')
        assert extractor.contains_producer(self.prod1.name) == True
        assert extractor.contains_producer("Should not exist!") == False

class TestGroupThings(GeneralSetup):
    
    def test_group_extractor(self):
        assert extractor.contains_group(self.group1.name) == True
        assert extractor.contains_group("Not a group!!") == False
        assert extractor.get_group(self.group1.owner.name, self.group1.name).producers[0]\
            == self.prod1
        self.assertRaises(Exception, extractor.get_group, "Hurrman", self.group1.name) 
 

class TestGlobalNetworkThings(GeneralSetup):
    """
    def test_global_network(self):
        assert globalNetwork.neighbours(self.prod1) == [self.prod2]
    """
    def test_global_network_performance(self):
        self.prod_list[35].save()
        assert 1 == 1
        
    def test_global_info_ratings(self):
        assert globalNetwork.get_common_info_ratings(self.prod1.name, self.prod2.name,[self.tag1.name])\
            == [(self.info_rating1, self.info_rating2,)]
        assert globalNetwork.get_common_info_ratings(self.prod1.name, self.prod2.name,[self.tag2.name])\
            == []
        assert globalNetwork.get_common_info_ratings(self.prod1.name, self.prod3.name,[self.tag1.name, self.tag2.name])\
            == [(self.info_rating1, self.info_rating1,)]
        assert globalNetwork.get_common_info_ratings(self.prod2.name, self.prod3.name,[self.tag2.name])\
            == [(self.info_rating3, self.info_rating4,)]

    def test_get_extreme_info_ratings(self):
        res = globalNetwork.get_extreme_info_ratings(self.prod3.name, [self.tag1.name, self.tag2.name])
        assert self.info_rating4 in res
        assert self.info_rating5 in res
        assert len(res) == 2
    
    def test_get_max_rating_differnce(self):
        test1 = globalNetwork.get_max_rating_difference(self.prod1.name, self.prod4.name, [self.tag1.name, self.tag2.name])
        assert test1 == -1
        test2 = globalNetwork.get_max_rating_difference(self.prod1.name, self.prod2.name, [self.tag1.name])
        assert test2 == 2
        test3 = globalNetwork.get_max_rating_difference(self.prod1.name, self.prod2.name, [self.tag2.name])
        assert test3 == -1

if __name__ == "__main__":
    unittest.main()


