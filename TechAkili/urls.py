
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('publicpages.urls')),  # Connect the publicpages app
    path('auth/', include('social_django.urls', namespace='social'))

]
