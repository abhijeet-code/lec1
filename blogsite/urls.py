from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("submit",views.submit,name="submit"),
    path("listings/<int:id>",views.listingpage,name="listingpage"),
    path("cmntsubmit/<int:listingid>",views.cmntsubmit,name="cmntsubmit"),
    path("addachived/<int:listingid>",views.addachived,name="addwatchlist"),
    path("removeachived/<int:listingid>",views.removeachived,name="removewatchlist"),
    path("watchlist/<str:username>",views.watchlistpage,name="watchlistpage"),
    
]
