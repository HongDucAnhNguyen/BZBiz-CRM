from django.urls import path
from .views import AllAgentsView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'agents'

urlpatterns = [
    path('', AllAgentsView.as_view(), name="all_agents"),
    path('create/', AgentCreateView.as_view(), name="agents_create"),
    path('<int:pk>/', AgentDetailView.as_view(), name="agent_detail"),
    path('<int:pk>/update', AgentUpdateView.as_view(), name="agent_update"),
    path('<int:pk>/delete', AgentDeleteView.as_view(), name="agent_delete"),
]
