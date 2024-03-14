from django.db.models import *
from django.contrib.postgres.fields import ArrayField
from datetime import date
from datetime import datetime
# Create your models here.

'''class user(Model):
    id=AutoField(primary_key=True,serialize=True)
    name=CharField(max_length=200)
    cont=CharField(max_length=10)'''
    
class Users(Model):
    id=AutoField(primary_key=True,serialize=True)
    uname=CharField(max_length=200)
    email=CharField(max_length=200)
    passw=CharField(max_length=10)
    dob=DateField(default=date.today)
    gen=CharField(max_length=1,null=True)
    ans=ArrayField(IntegerField(default=0),size=5,null=True)
    wl=ArrayField(IntegerField(default=0),null=True)
    read=ArrayField(IntegerField(default=0),null=True)
    pid=IntegerField(default=0)
    recents=ArrayField(IntegerField(default=0),null=True)
    bio=CharField(max_length=20,default="")
    req=ArrayField(IntegerField(default=0),null=True)
    friend=ArrayField(IntegerField(default=0),null=True)
    isauth=IntegerField(default=0)

class Author(Model):
    id=AutoField(primary_key=True,serialize=True)
    uid=IntegerField(default=0)
    chaps=ArrayField(CharField(max_length=50),null=True)

class Profs(Model):
    id=AutoField(primary_key=True,serialize=True)
    pfile=ImageField(upload_to='media',default='sunny.jpg',null=True)

class OTP(Model):
    id=AutoField(primary_key=True,serialize=True)
    otp=IntegerField(null=True)
    exp=DateTimeField(null=True)
    em=CharField(max_length=200,null=True)

class Books(Model):
    id=AutoField(primary_key=True,serialize=True)
    isbn=CharField(default="",max_length=20)
    bname=CharField(max_length=200)
    author=CharField(max_length=100)
    genre=CharField(max_length=50)
    year=CharField(max_length=20,default="")
    cid=IntegerField(default=0)
    summary=CharField(max_length=500,null=True)
    reads=IntegerField(default=0)
 
class Covers(Model):
    id=AutoField(primary_key=True,serialize=True)
    cfile=ImageField(upload_to="media",default="def.jpg",null=True,max_length=200)

class Reviews(Model):
    id=AutoField(primary_key=True,serialize=True)
    uid=IntegerField(default=0)
    bid=IntegerField(default=0)
    rev=CharField(max_length=200)
    stars=DecimalField(default=0,decimal_places=1,max_digits=3)
    replyto=IntegerField(default=0)
    
class BookClubs(Model):
    id=AutoField(primary_key=True,serialize=True)
    name=CharField(max_length=40)
    admin=IntegerField(default=0)
    members=ArrayField(IntegerField(default=0),null=True,size=50)
    botws=ArrayField(IntegerField(default=0),null=True)

class Feed(Model):
    id=AutoField(primary_key=True,serialize=True)
    uid=IntegerField(default=0)
    bcid=IntegerField(default=0)
    content=CharField(max_length=50)
    botw=IntegerField(default=0)
    time=TimeField(default=datetime.now().time())

class Reports(Model):
    repmonth=IntegerField(default=0)
    repyear=IntegerField(default=0)
    monthacc=IntegerField(default=0)
    monthreads=IntegerField(default=0)
