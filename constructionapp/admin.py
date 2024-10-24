from django.contrib import admin

from constructionapp.models import ArchitectBooking, ContractorBooking, DesignerBooking, Payment

# Register your models here.
admin.site.register(Payment)
admin.site.register(ArchitectBooking)
admin.site.register(DesignerBooking)
admin.site.register(ContractorBooking)