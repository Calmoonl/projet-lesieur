from django.contrib import admin
from .models import Standard, Format, Ligne, Machine, Audit, StandardAudit, Photo

admin.site.register(Standard)
admin.site.register(Format)
admin.site.register(Photo)
admin.site.register(Ligne)
admin.site.register(Machine)
admin.site.register(Audit)
admin.site.register(StandardAudit)
