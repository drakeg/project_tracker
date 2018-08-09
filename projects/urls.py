from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:tracker_id>/', views.detail, name='detail'),
	path('<int:tracker_id>/comments', views.comments, name='comments'),
	path('<int:tracker_id>/updates', views.updates, name='updates'),
]
