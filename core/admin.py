from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(World)
admin.site.register(Land)

admin.site.register(User, UserAdmin)
admin.site.register(Faction)
admin.site.register(Letter)
admin.site.register(FactionKnowledge)
admin.site.register(Caravan)

#Replace admin form with Caravan form
admin.site.unregister(Caravan)
@admin.register(Caravan)
class caravanAdmin(admin.ModelAdmin):
    form = caravanModelForm
