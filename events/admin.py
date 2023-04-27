from django.contrib import admin
from .models import Events

class EventsAdmin(admin.ModelAdmin):
    list_display = ('event_name','event_description','max_tickets','start_date','end_date','event_created','account_id')

# Register your models here.
admin.site.register(Events,EventsAdmin)

