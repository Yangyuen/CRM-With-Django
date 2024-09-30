from django.urls import path
from . import views

urlpatterns = [
        path('',views.home,name=''),
        path('register',views.register,name="register"),
        path('my-login',views.my_login,name="my-login"),
        path('user-logout',views.user_logout,name="user-logout"),
        
        # CRUD
        path('dashboard',views.dashboard,name="dashboard"),
        path('create-assets',views.create_assets,name="create-assets"),
        path('update-assets/<int:pk>/',views.update_assets,name="update-assets"),
        path('view-assets/<int:pk>/',views.read_assets,name="view-assets"),
        path('delete-assets/<int:pk>/',views.delete_assets,name="delete-assets"),
        path('import-assets/', views.import_assets, name='import-assets'),
]