from django.http import HttpResponse
from django.template import loader
from .models import *

def reportgenerate(request):
  users=Users.objects.all()
  teens=twenties=rest=0
  for i in users:
    age=date.today()-i.dob
    age=age.days//365
    if age>10 and int(age)<20:
      teens+=1
    elif age>20 and int(age)<30:
      twenties+=1
    else:
      rest+=1
  authors=Books.objects.all().values("author").distinct()
  authdist=[]
  for i in authors:
    au=i["author"]
    s=0
    bo=Books.objects.filter(author=au)
    for j in list(bo):
      s+=j.reads
    authdist.append({"name":au,"reads":s})
  d=date.today()
  reps=Reports.objects.get(repmonth=d.month,repyear=d.year)
  template = loader.get_template('reports.html')
  context = {
    "totalusers":users.count(),
    "teens":teens,
    "twenties":twenties,
    "rest":rest,
    "auth":authdist,
    "reps":reps
  }
  return HttpResponse(template.render(context, request))
