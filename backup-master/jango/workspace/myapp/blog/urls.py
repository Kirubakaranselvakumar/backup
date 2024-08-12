from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('index', views.index, name="index"),
    path('post/<str:slug>', views.detail, name="detail"),    
    path('contact', views.contact_view, name='contact'),
    path('about', views.about_view, name='about'),
    path('add',views.add, name="add"),
    path('edit/<int:post_id>',views.edit, name="edit"),
    path('delete/<int:post_id>',views.delete, name="delete"),
    path('grid', views.grid, name="grid"),
    path('get_grid', views.get_grid, name="get_grid"),
    path('', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('category/', views.category_search, name="category"),
    path('subcategory', views.subcategory, name="subcategory"),
    # path('ajax/posts/', views.post_list, name='post_list'),
    # path('ajax/posts/<slug:slug>/', views.post_detail, name='post_detail'),
    # path('new_something_url', views.new_url_view, name='new_page_url'),
    # path('old_url', views.old_url_redirect, name='old_url'),
]