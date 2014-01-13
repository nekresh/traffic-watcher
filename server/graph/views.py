from django.http import HttpResponse

def index(request):
	return HttpResponse("<html><body>Hello world</body></html>") 
