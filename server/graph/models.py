from mongoengine import *
import datetime

class Ticks(Document):
	tick_date = DateTimeField()
	insert_date = DateTimeField(default=datetime.datetime.now)
	type = StringField()
	data = DynamicField()
