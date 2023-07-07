from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('categorias',views.categorias,name='categorias'),
    path('periodistas',views.periodistas,name='periodistas'),
    path('contacto',views.contacto,name='contacto'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('signout', views.signout, name='signout'),
    path('change_passwd', views.change_passwd, name='change_passwd'),
    path('admin_noticia', views.admin_noticia, name='admin_noticia'),
    path('accion_noticia', views.accion_noticia, name='accion_noticia'),
    path('add_news', views.add_news, name='add_news'),
    path('my_news', views.my_news, name='my_news'),
    path('admin_users', views.admin_users, name='admin_users'),
    path('user_chng', views.user_chng, name='user_chng'),
    path('noticia',views.noticia,name='noticia'),
    path('noticia1',views.noticia1,name='noticia1'),
    path('noticia2',views.noticia2,name='noticia2'),
    path('noticia3',views.noticia3,name='noticia3'),
    path('noticia4',views.noticia4,name='noticia4'),
    path('noticia5',views.noticia5,name='noticia5'),
    path('noticia6',views.noticia6,name='noticia6'),
    path('noticia7',views.noticia7,name='noticia7'),
    path('noticia8',views.noticia8,name='noticia8'),
    path('noticia9',views.noticia9,name='noticia9'),
]