from veracitor.database import *

# Setup tags
tags = ["General","Crime","Culture","Politics","Sports","Finances"]
for tag in tags:
    extractor.get_tag_create_if_needed(tag)
