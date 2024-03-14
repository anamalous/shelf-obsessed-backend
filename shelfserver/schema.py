import graphene
from graphene_django import DjangoObjectType
import json
from userdata.models import *
from graphene_file_upload.scalars import Upload
import os 
from .settings import MEDIA_ROOT
from random import randint
from django.core.mail import send_mail
from datetime import datetime,timedelta
import pandas as pd
from sklearn.cluster import KMeans
import csv
import os

class UserType(DjangoObjectType):
    class Meta:
        model = Users
        fields = "__all__"
    
class ProfType(DjangoObjectType):
    class Meta:
        model=Profs
        fields="__all__"

class BookType(DjangoObjectType):
    class Meta:
        model=Books
        fields="__all__"

class ReviewType(DjangoObjectType):
    class Meta:
        model=Reviews
        fields="__all__"
    
class FeedType(DjangoObjectType):
    class Meta:
        model=Feed
        fields="__all__"
    
class BookClubType(DjangoObjectType):
    class Meta:
        model=BookClubs
        fields="__all__"

class AuthorType(DjangoObjectType):
    class Meta:
        model=Author
        fields="__all__"

class Query(graphene.ObjectType):
    send_otp=graphene.Field(graphene.Int,em=graphene.String(required=True))
    verify_user=graphene.Field(graphene.String,pw=graphene.String(required=True),rid=graphene.Int(required=True),otp=graphene.Int(required=True))
    login_user=graphene.Field(graphene.Int,em=graphene.String(required=True),pw=graphene.String(required=True))
    user_by_id=graphene.Field(UserType,uid=graphene.Int(required=True))
    prof_by_uid=graphene.Field(graphene.String,uid=graphene.Int(required=True))
    book_by_col=graphene.Field(graphene.List(BookType),val=graphene.String(required=True),col=graphene.String(required=True))
    cover_by_cid=graphene.Field(graphene.String,cid=graphene.Int(required=True))
    book_by_id=graphene.Field(BookType,bid=graphene.Int(required=True))
    reviews_for_bid=graphene.Field(graphene.List(ReviewType),bid=graphene.Int(required=True))
    is_added=graphene.Field(graphene.String,uid=graphene.Int(required=True),bid=graphene.Int(required=True))
    overall_rating=graphene.Field(graphene.Float,bid=graphene.Int(required=True))
    suggested_profiles=graphene.Field(graphene.List(UserType),uid=graphene.Int(required=True))
    recents=graphene.Field(graphene.List(BookType),uid=graphene.Int(required=True))
    recent_author=graphene.Field(graphene.List(BookType),uid=graphene.Int(required=True))
    posts_for_uid=graphene.Field(graphene.List(FeedType),uid=graphene.Int(required=True))
    feed_for_uid=graphene.Field(graphene.List(FeedType),uid=graphene.Int(required=True))
    club_by_uid=graphene.Field(graphene.List(BookClubType),uid=graphene.Int(required=True))
    club_by_bcid=graphene.Field(BookClubType,bcid=graphene.Int())
    get_club_feed=graphene.Field(graphene.List(FeedType),bcid=graphene.Int())
    botw_for_bcid=graphene.Field(graphene.List(BookType),bcid=graphene.Int())
    all_clubs=graphene.Field(graphene.List(BookClubType),uid=graphene.Int())
    create_book_db=graphene.Field(graphene.String())
    check_uname=graphene.Field(graphene.Int(),uname=graphene.String())
    review_for_id=graphene.Field(ReviewType,rid=graphene.Int())
    post_for_id=graphene.Field(FeedType,fid=graphene.Int())
    all_chaps=graphene.Field(AuthorType,uid=graphene.Int())
    get_chap_content=graphene.Field(graphene.String(),cname=graphene.String())
    get_auths=graphene.Field(graphene.List(AuthorType))

    def resolve_get_auths(self,info):
        return list(Author.objects.all())

    def resolve_get_chap_content(self,info,cname):
        f=open("./chapters/"+cname+".txt","r")
        return f.read()

    def resolve_all_chaps(self,info,uid):
        return Author.objects.get(uid=uid)

    def resolve_post_for_id(self,info,fid):
        return Feed.objects.get(id=fid)
    def resolve_review_for_id(self,info,rid):
        return Reviews.objects.get(id=rid)

    def resolve_check_uname(self,info,uname):
        try:
            u=Users.objects.get(uname=uname)
            return 0
        except:
            return 1
        
    def resolve_create_book_db(self,info):
        with open('./userdata/books.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))
        return "done"

    def resolve_feed_for_uid(self,info,uid):
        u=Users.objects.get(id=uid)
        if u.friend is None:
            return []
        else:
            f=Feed.objects.filter(uid__in=u.friend,bcid=0)
            return list(f)
    
    def resolve_recent_author(self,info,uid):
        u=Users.objects.get(id=uid)
        l=u.recents
        b=Books.objects.get(id=l[-1])
        res=Books.objects.filter(author=b.author)
        return list(res)

    def resolve_recents(self,info,uid):
        u=Users.objects.get(id=uid)
        b=Books.objects.filter(id__in=list(u.recents))
        return list(b)

    def resolve_suggested_profiles(self,info,uid):
        u=Users.objects.all()
        l=[]
        for i in u:
            if i.id!=uid and i.ans is not None:
                l.append([i.id]+i.ans)
        if len(l)==0:
            return []
        df = pd.DataFrame(l, columns=['uid','a1', 'a2', 'a3', 'a4','a5'])
        if len(l)<=3:
            u=df["uid"].tolist()
            return Users.objects.filter(id__in=u)
        kmeans = KMeans(n_clusters=2,n_init=10)
        df["type"] = kmeans.fit_predict(df[['a1', 'a2', 'a3', 'a4','a5']])
        user=Users.objects.get(id=uid)
        res=kmeans.predict([user.ans])
        get=df.loc[df["type"] == res[0]]
        uids=get["uid"].tolist()
        ret=Users.objects.filter(id__in=uids[:5])
        ans=[]
        for i in ret:
            if user.friend is None:
                ans.append(i)
            elif i.id not in user.friend:
                ans.append(i) 
        return list(ans)
    
    def resolve_overall_rating(self,info,bid):
        b=Reviews.objects.filter(bid=bid)
        s=0.0
        for i in b:
            s+=float(i.stars)
        if s==0.0:
            return 0.0
        else:
            return round(s/len(b),1)

    def resolve_is_added(self,info,uid,bid):
        u=Users.objects.get(id=uid)
        s=[0,0]
        if u.read is not None and bid in u.read:
            s[0]=1
        if u.wl is not None and bid in u.wl:
            s[1]=1
        return str(s[0])+str(s[1])

    def resolve_reviews_for_bid(self,info,bid):
        return list(Reviews.objects.filter(bid=bid))
    
    def resolve_send_otp(self,info,em):
        if Users.objects.filter(email=em).exists():
            return -1
        message='''E-mail for authentication
        Your otp is: '''
        o=str(randint(1000,9999))
        message+=o
        send_mail("Authentication",message,"adonuts@hotmail.com",[em],fail_silently=False,)
        dt=datetime.now()
        dt += timedelta(minutes=1)
        ot=OTP.objects.create()
        ot.otp=o
        ot.exp=dt
        ot.em=em
        i=ot.id
        ot.save()
        return i
    
    def resolve_verify_user(self,info,rid,otp,pw):
        ot=OTP.objects.get(id=rid)
        if ot.exp.time()<datetime.now().time():
            return "expired"
        elif ot.otp==otp:
            u=Users.objects.create()
            u.email=ot.em   
            u.passw=pw
            i=u.id
            u.save()
            return str(i)
        else:
            return "invalid"
        
    def resolve_login_user(self,info,em,pw):
        r=0
        try:
            u=Users.objects.get(email=em)
            if u.passw==pw:
                r=u.id
            else:
                r=-1
            return r
        except:
            r=-2
            return r
        
    def resolve_user_by_id(self,info,uid):
        try:
            return Users.objects.get(id=uid)
        except:
            return None
    
    def resolve_prof_by_uid(self,info,uid):
        try:
            u=Users.objects.get(id=uid)
            p=Profs.objects.get(id=u.pid)
            return p.pfile
        except:
            return "not found"
    
    def resolve_book_by_col(self,info,val,col):
        try:
            if col=="a":
                b=Books.objects.filter(author__startswith=val)
            elif col=="g":
                b=Books.objects.filter(genre__startswith=val)
            elif col=="y":
                b=Books.objects.filter(year__startswith=val)
            elif col=="i":
                b=Books.objects.filter(isbn__startswith=val)
            else:
                b=Books.objects.filter(bname__startswith=val)
            return list(b)
        except:
            return None   

    def resolve_cover_by_cid(self,info,cid):
        c=Covers.objects.get(id=cid)
        return c.cfile
    
    def resolve_book_by_id(self,info,bid):
        return Books.objects.get(id=bid)

    def resolve_posts_for_uid(self,info,uid):
        p=Feed.objects.filter(uid=uid,bcid=0)
        return list(p)

    def resolve_club_by_uid(self,info,uid):
        p=BookClubs.objects.filter(members__contains=[uid])
        return list(p)
    
    def resolve_club_by_bcid(self,info,bcid):
        return BookClubs.objects.get(id=bcid)
    
    def resolve_get_club_feed(self,info,bcid):
        b=Feed.objects.filter(bcid=bcid)
        return list(b)
    
    def resolve_botw_for_bcid(self,info,bcid):
        c=BookClubs.objects.get(id=bcid)
        if c.botws is None:
            return []
        else:
            b=Books.objects.filter(id__in=c.botws)
            return list(b)

    def resolve_all_clubs(self,info,uid):
        b=BookClubs.objects.all()
        l=[]
        for i in b:
            if uid not in i.members:
                l.append(i)
        return l

class RegUser(graphene.Mutation):
    class Arguments:
        uname = graphene.String(required=True)
        uid = graphene.Int()
        pid=graphene.Int()
        dob=graphene.String(required=True)
        gen=graphene.String(required=True)
        bio=graphene.String(required=True)

    u = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, uid,uname,dob,gen,pid,bio):
        user=Users.objects.get(id=uid)
        if user.pid!=pid:
            Profs.objects.filter(id=user.pid).delete()
        user.pid=pid
        user.uname=uname
        user.bio=bio
        d=[int(x) for x in dob.split("-")]
        user.dob=date(year=d[0],month=d[1],day=d[2])
        user.gen=gen
        i=user.id
        user.save()
        d=date.today()
        try:
            r=Reports.objects.get(repmonth=d.month,repyear=d.year)
        except:
            r=Reports.objects.create()
            r.repmonth=d.month
            r.repyear=d.year
        r.monthacc+=1
        r.save()
        return RegUser(u=True)

class DelUser(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid):
        try:
            Users.objects.filter(id=uid).delete()
            return DelUser(s="deleted")
        except:
            return DelUser(s="user does not exist")
        
class RegAuth(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid):
        u=Users.objects.get(id=uid)
        if u.isauth==0:
            u.isauth=1
            a=Author.objects.create()
            a.uid=uid
            a.chaps=[]
            a.save()
            u.save()
        else:
            u.isauth=0
            a=Author.objects.filter(uid=uid).delete()
            u.save()
        return RegAuth(s="done")

class AddChap(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        chap=graphene.String()
        content=graphene.String()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,chap,content):
        u=Author.objects.get(uid=uid)
        u.chaps.append(chap)
        f=open("./chapters/"+chap+".txt","w+")
        f.write(content)
        f.close()
        u.save()
        return AddChap(s="done")

class SetProfile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    i = graphene.Int()

    @classmethod
    def mutate(cls, root, info, file):
        p=Profs.objects.create()
        p.pfile=file
        i=p.id
        p.save()
        return SetProfile(i=i)
    
class ProfQues(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        a=graphene.List(graphene.Int)

    set=graphene.Boolean()

    @classmethod
    def mutate(cls,root,info,uid,a):
        u=Users.objects.get(id=uid)
        u.ans=list(a)
        u.save()
        return ProfQues(set=True)
    
class EditBook(graphene.Mutation):
    class Arguments:
        bid=graphene.Int()
        uid=graphene.Int()
        set=graphene.String(required=True)

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,bid,uid,set):
        u=Users.objects.get(id=uid)
        if set=="w":
            if u.wl==None:
                u.wl=[bid]
            else:
                l=u.wl
                if bid in l:
                    l.remove(bid)
                else:
                    l.append(bid)
                u.wl=l
        if set=="r":
            if u.read==None:
                u.read=[bid]
            else:
                l=u.read
                if bid in l:
                    l.remove(bid)
                else:
                    l.append(bid)
                u.read=l
        u.save()
        return EditBook(s="done")
 
class AddReview(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        bid=graphene.Int()
        rev=graphene.String()
        st=graphene.Int()
    
    d=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,bid,rev,st):
        r=Reviews.objects.create()
        r.rev=rev
        r.stars=st
        r.uid=uid
        r.bid=bid
        r.save()
        return AddReview(d="added")
    
class AddReviewReply(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        bid=graphene.Int()
        rev=graphene.String()
        st=graphene.Int()
        rt=graphene.Int()
    
    d=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,bid,rev,st,rt):
        r=Reviews.objects.create()
        r.rev=rev
        r.stars=st
        r.uid=uid
        r.bid=bid
        r.replyto=rt
        r.save()
        return AddReviewReply(d="added")

class SendRequest(graphene.Mutation):
    class Arguments:
        send=graphene.Int()
        rec=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(clas,root,info,send,rec):
        u=Users.objects.get(id=rec)
        if u.req is None:
            u.req=[send]
        else:
            if send not in u.req:
                u.req.append(send)
        u.save()
        return SendRequest(s="done")
    
class AccRequest(graphene.Mutation):
    class Arguments:
        acc=graphene.Int()
        send=graphene.Int()
    
    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,acc,send):
        u1=Users.objects.get(id=acc)
        u2=Users.objects.get(id=send)
        l=u1.req
        l.remove(send)
        u1.req=l
        if u2.req is not None and acc in u2.req:
            l=u2.req
            l.remove(acc)
            u2.req=l
        l=u1.friend
        if u1.friend is None:
            u1.friend=[send]
        else:
            if send not in u1.friend:
                l.append(send)
            u1.friend=l
        l=u2.friend
        if u2.friend is None:
            u2.friend=[acc]
        else:
            if acc not in u2.friend:
                l.append(acc)
            u2.friend=l
        u1.save()
        u2.save()
        return AccRequest(s="done")

class DeleteRequest(graphene.Mutation):
    class Arguments:
        dele=graphene.Int()
        send=graphene.Int()
    
    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,dele,send):
        u1=Users.objects.get(id=dele)
        l=u1.req
        l.remove(send)
        u1.req=l
        u1.save()
        return DeleteRequest(s="done")
    
class DeleteFriend(graphene.Mutation):
    class Arguments:
        dele=graphene.Int()
        send=graphene.Int()
    
    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,dele,send):
        u1=Users.objects.get(id=dele)
        u2=Users.objects.get(id=send)
        l=u1.friend
        l.remove(send)
        u1.friend=l
        u1.save()
        l=u2.friend
        l.remove(dele)
        u2.friend=l
        u2.save()
        return DeleteFriend(s="done")

class NewPost(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        cont=graphene.String()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,cont):
        f=Feed.objects.create()
        f.uid=uid
        f.content=cont
        f.date=datetime.now().time()
        f.save()
        return NewPost(s="done")    

class NewRecent(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        bid=graphene.Int()
    
    i=graphene.Int()

    @classmethod
    def mutate(clf,root,info,uid,bid):
        u=Users.objects.get(id=uid)
        l=u.recents
        if l is not None:
            if bid not in l:
                if len(l)>=4:
                    l.pop(0)
                l.append(bid)
        else:
            l=[bid]
        u.recents=l
        u.save()
        b=Books.objects.get(id=bid)
        b.reads+=1
        b.save()
        d=date.today()
        try:
            r=Reports.objects.get(repmonth=d.month,repyear=d.year)
        except:
            r=Reports.objects.create()
            r.repmonth=d.month
            r.repyear=d.year
        r.monthreads+=1
        r.save()
        return NewRecent(i=bid)
    
class CreateBookclub(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        bcname=graphene.String()
        mems=graphene.List(graphene.Int)
    
    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,bcname,mems):
        b=BookClubs.objects.create()
        b.admin=uid
        b.name=bcname
        b.members=[uid]+list(mems)
        b.save()
        return CreateBookclub(s='done')
    
class JoinClub(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        bcid=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,bcid):
        b=BookClubs.objects.get(id=bcid)
        if b.members is None:
            b.members=[uid]
        else:
            if uid not in b.members:
                b.members.append(uid)
        b.save()
        return JoinClub(s="done")
    
class ExitMember(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        bcid=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,bcid):
        b=BookClubs.objects.get(id=bcid)
        Feed.objects.filter(bcid=bcid,uid=uid).delete()
        b.members.remove(uid)
        if b.admin==uid:
            b.delete()
        else:
            b.save()
        return ExitMember(s="done")

class NewClubPost(graphene.Mutation):
    class Arguments:
        uid=graphene.Int()
        cont=graphene.String()
        bcid=graphene.Int()
        botw=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,uid,cont,bcid,botw):
        b=BookClubs.objects.get(id=bcid)
        if uid in b.members or uid==b.admin:
            f=Feed.objects.create()
            f.uid=uid
            f.bcid=bcid
            f.content=cont
            f.botw=botw
            f.date=datetime.now().time()
            f.save()
            return NewClubPost(s="done")  
        else:
            return NewClubPost(s="Join The Club To Post!")

class AddBOTW(graphene.Mutation):
    class Arguments:
        bid=graphene.Int()
        bcid=graphene.Int()

    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,bid,bcid):
        b=BookClubs.objects.get(id=bcid)
        if b.botws is None:
            b.botws=[bid]
        else:
            if bid not in b.botws:
                b.botws.append(bid)
        b.save()
        return AddBOTW(s="done")

class DeleteReview(graphene.Mutation):
    class Arguments:
        rid=graphene.Int()
    
    s=graphene.String()

    @classmethod
    def mutate(cls,root,info,rid):
        r=Reviews.objects.filter(id=rid).delete()
        return DeleteReview(s="done")
        
class Mutation(graphene.ObjectType):
    register_user=RegUser.Field()
    delete_user=DelUser.Field()
    set_prof=SetProfile.Field()
    prof_questions=ProfQues.Field()
    edit_book=EditBook.Field()
    add_review=AddReview.Field()
    new_recent=NewRecent.Field()
    send_request=SendRequest.Field()
    accept_request=AccRequest.Field()
    delete_request=DeleteRequest.Field()
    delete_friend=DeleteFriend.Field()
    new_post=NewPost.Field()
    create_bookclub=CreateBookclub.Field()
    join_club=JoinClub.Field()
    exit_member=ExitMember.Field()
    new_club_post=NewClubPost.Field()
    add_BOTW=AddBOTW.Field()
    delete_review=DeleteReview.Field()
    review_reply=AddReviewReply.Field()
    reg_author=RegAuth.Field()
    add_chapter=AddChap.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)