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
from networkx import nx
connect('mydb')

if __name__ == "__main__":
    globalNetwork.build_network_from_db()
    tag1 = tag.Tag(name="gardening",
                            description="Hurrr HURRRRRR")
    tag1.save()

    tag2 = tag.Tag(name="cooking",
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

    
    ### TEST GRAPH
    G = nx.DiGraph()
    # The same graph as G (graf1.png) but the weights there are here under "cooking"
    # and the "crime" ratings are kind of random.
    # this is how you add edges to the global graph I think y'all
    G.add_edges_from([(1,2,dict(cooking=10, crime=4)),
                      (1,3,dict(cooking=8, crime=7)),
                      (1,4,dict(cooking=9, crime=6)),
                      (2,5,dict(cooking=9, crime=9)),
                      (3,5,dict(cooking=10, crime=5)),
                      (3,6,dict(cooking=10, crime=6)),
                      #(3,7,dict(cooking=7)),
                      (4,5,dict(cooking=8, crime=7)),
                      (4,6,dict(cooking=9, crime=6)),
                      (5,7,dict(cooking=8, crime=5)),
                      (6,7,dict(cooking=6, crime=7)),
                      (6,8,dict(cooking=5, crime=7)),
                      (8,4,dict(cooking=5, crime=7)),
                      (3,2,dict(cooking=5, crime=7)),
                      (2,1,dict(cooking=5, crime=7)),
                      ])

    
    prods = {}
    for n in G.nodes():
        prods[n] = producer.Producer(name=n, type_of="testdummy")

    for n in G.nodes():
        for rated in G[n]:
            for tag in rated:
                source_rating = producer.SourceRating(rating=3, source=prod2,
                                                      tag=tag1)
