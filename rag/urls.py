from django.contrib import admin
from django.urls import path
from chat_core.views import bot_chat
from authentication.views import signup_view, login_view, home_view, logout_view
from bot_creation.views import create_bot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/<str:textfile>/<str:botname>/<uuid:uuid>', bot_chat, name="chat_view"),
    path('signup/', signup_view, name="signup_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('', home_view, name="home_view"),
    path('create-bot/', create_bot, name="create_bot"),
]
