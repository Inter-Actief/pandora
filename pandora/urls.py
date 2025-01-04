from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path

# Use django-allauth for admin login
admin.site.login = staff_member_required(admin.site.login, login_url=settings.LOGIN_URL)

urlpatterns = [
    path('', include('pandora.core.urls')),
    path('', include('pandora.editions.urls')),
    path('', include('pandora.pregames.urls')),
    path('', include('pandora.puzzles.urls')),
    path('', include('pandora.teams.urls')),

    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('qr-code/', include('qr_code.urls', namespace='qr_code')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
