from django import forms
from .models import PieceRechange
from .models import Machine
from .models import Intervention
from .models import PlanMaintenance
from django_select2.forms import Select2MultipleWidget

from django.contrib.auth.models import User



class PieceRechangeForm(forms.ModelForm):
    class Meta:
        model = PieceRechange
        fields = ['code', 'designation', 'quantite_stock', 'seuil_alerte', 'prix_unitaire', 'machines_compatibles'] # ➕ ajouter machines
        widgets = {
            'machines': forms.CheckboxSelectMultiple(),  # pour sélectionner plusieurs machines
        }
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['machine', 'description', 'date_planifiee']
        widgets = {
            'date_planifiee': forms.DateInput(attrs={'type': 'date'}),
        }
       
LABEL_CHOICES = [
    ('Préventif', 'Préventif'),
    ('Réglementaire', 'Réglementaire'),
    ('Correctif', 'Correctif'),
    ('Critique', 'Critique'),
]

class PlanMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PlanMaintenance
        fields = '__all__'
        widgets = {
            'machine': forms.SelectMultiple(attrs={'id': 'id_machine'}),
            'assignes': forms.SelectMultiple(attrs={'id': 'id_assignes'}),
            'labels': forms.SelectMultiple(attrs={'id': 'id_labels'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }