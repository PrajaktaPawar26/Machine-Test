from django.urls import path
from .views import ClientListCreateView, ClientRetrieveUpdateDeleteView, ProjectListCreateView, ProjectRetrieveUpdateDeleteView

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDeleteView.as_view(), name='client-detail'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDeleteView.as_view(), name='project-detail'),
]
