from django.urls import path
from . import views
urlpatterns=[
    path("generate/",views.reportgenerate),
]
'''urlpatterns=[
    path("getfile/<str:fname>",views.fileget),
    path("getsum/<int:n1>/<int:n2>",views.retsum),
    path("adduser",views.adduser),
    path("getusers",views.getusers),
    path("deluser/<int:id>",views.deluser),
    path("upduser/<int:id>",views.upduser)
]'''