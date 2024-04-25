from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [

    path('', views.AllLeadsView.as_view(), name="all_leads"),
    path('create/', views.LeadCreateView.as_view(), name='lead_create'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead_update'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead_delete'),
    path('<int:pk>/assign-agent/', views.AssignAgentView.as_view(), name='assign_agent'),
    path('lead-statuses/', views.AllLeadStatusesView.as_view(), name='all_lead_statuses'),
    path('lead-statuses/<int:pk>/', views.LeadsDetailsByLeadStatusView.as_view(), name='lead_status_detail'),
    path('lead-statuses/<int:pk>/update', views.LeadStatusUpdateView.as_view(), name='lead_status_update'),

]
