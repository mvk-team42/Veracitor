from database import *
networkModel.build_network_from_db()
tag = tag.Tag(name="General")
tag.save()

user1 = user.User(name="Daniel", password="1234")
user2 = user.User(name="John", password="1234")
user3 = user.User(name="Alfred", password="1234")
user4 = user.User(name="Fredrik", password="1234")
user5 = user.User(name="Gustaf", password="1234")
user6 = user.User(name="Jonathan", password="1234")
user7 = user.User(name="Martin", password="1234")
user8 = user.User(name="Anton", password="1234")

"""
user1 = extractor.get_user('Daniel')
user2 = extractor.get_user('John')
user3 = extractor.get_user('Alfred')
user4 = extractor.get_user('Fredrik')
user5 = extractor.get_user('Gustaf')
user6 = extractor.get_user('Jonathan')
user7 = extractor.get_user('Martin')
user8 = extractor.get_user('Anton')
"""

user1.save()
user2.save()
user3.save()
user4.save()
user5.save()
user6.save()
user7.save()
user8.save()

user7.rate_source(user8, tag, 4)
user1.rate_source(user2, tag, 3)
user7.rate_source(user8, tag, 3)
user8.rate_source(user6, tag, 4)
user2.rate_source(user6, tag, 5)
user6.rate_source(user5, tag, 5)
user6.rate_source(user4, tag, 4)
user5.rate_source(user3, tag, 4)
user5.rate_source(user3, tag, 3)
user4.rate_source(user3, tag, 5)

user1.save()
user2.save()
user3.save()
user4.save()
user5.save()
user6.save()
user7.save()
user8.save()



