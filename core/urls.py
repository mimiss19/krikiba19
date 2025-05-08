from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from core.views import custom_login

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('machines/', views.machines, name='machines'),
    path('pieces/', views.pieces, name='pieces'),
    path('capteurs/', views.capteurs, name='capteurs'),
    path('interventions/', views.interventions, name='interventions'),
    path('notifications/', views.notifications, name='notifications'),
    path('import-excel/', views.import_excel, name='import_excel'),
    path('delete-all-pieces/', views.delete_all_pieces, name='delete_all_pieces'),
    path('delete-piece/<int:piece_id>/', views.delete_piece, name='delete_piece'),
    path('modifier-piece/', views.modifier_piece, name='modifier_piece'),
    path('ajouter-machine/', views.ajouter_machine, name='ajouter_machine'),
    path('dashboard/', views.dashboard_maintenance, name='dashboard'),
    path('machine/<int:machine_id>/maintenances/', views.voir_maintenance_machine, name='voir_maintenance_machine'),
    path('modifier-machine/<int:id>/', views.modifier_machine, name='modifier_machine'),
    path('supprimer-machine/<int:id>/', views.supprimer_machine, name='supprimer_machine'),
    path('machine/<int:machine_id>/details/', views.details_machine, name='details_machine'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accueil/', views.accueil, name='accueil'),
    path('intervention/<int:intervention_id>/cloturer/', views.cloturer_intervention, name='cloturer_intervention'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('intervention/<int:intervention_id>/modifier/', views.modifier_intervention, name='modifier_intervention'),
    path('intervention/<int:intervention_id>/supprimer/', views.supprimer_intervention, name='supprimer_intervention'),
    path('api/alertes-jour/', views.alertes_du_jour, name='alertes_jour'),
    path('api/interventions/', views.api_interventions, name='api_interventions'),
    path('plans/creer/', views.creer_plan_maintenance,name='creer_plan'),
    path('plans/', views.liste_plans_maintenance, name='liste_plans_maintenance'),
    path('plans/success/', views.success_plan, name='success_plan'),
    path('plans/<int:id>/', views.voir_plan, name='voir_plan'),
    path('plan/<int:id>/modifier/', views.modifier_plan, name='modifier_plan'),
    path('plan/<int:id>/supprimer/', views.supprimer_plan, name='supprimer_plan'),



]
