from django.contrib import admin

from .models import User,VerificationToken

admin.site.register(User)
admin.site.register(VerificationToken)