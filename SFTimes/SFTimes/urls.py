from django.contrib import admin
from django.urls import include, path
#from root import views

urlpatterns = [
    path("", include("root.urls")),
    path("games/", include("games.urls")),
    path("games/SFSpellingBee/", include("games.SFSpellingBee.urls")),
    path("games/SFConnections/", include("games.SFConnections.urls")),
    path("games/SFGalaga/", include("games.SFGalaga.urls")),
    path("games/SFWordle/", include("games.SFWordle.urls")),
    path('admin/', admin.site.urls),
]
