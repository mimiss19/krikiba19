from django.contrib import admin
from .models import Machine, PieceRechange, Intervention, Notification, MesureCapteur
from .models import PlanMaintenance

admin.site.register(Machine)
admin.site.register(PieceRechange)
admin.site.register(Intervention)
admin.site.register(Notification)
admin.site.register(MesureCapteur)
class PieceRechangeAdmin(admin.ModelAdmin):
    list_display = ('code', 'designation', 'quantite_stock', 'seuil_alerte', 'en_alerte')
    search_fields = ('code', 'designation')


@admin.register(PlanMaintenance)
class PlanMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'machine', 'date_debut', 'frequence', 'unite')
    search_fields = ('titre', 'machine__nom')