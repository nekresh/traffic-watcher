from tastypie import authorization
from tastypie_mongoengine import resources
from graph import models

class TicksResource(resources.MongoEngineResource):
	class Meta:
		queryset = models.Ticks.objects.all()
		allowed_methods = ('get', 'post', 'patch')
		authorization = authorization.Authorization()
