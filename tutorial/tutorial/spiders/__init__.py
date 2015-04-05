# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.item import Item, Field 
class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()

