from django.urls import path
from .views import create_grade,topic_update_view, grade_list_view,lesson_list_view,topic_detail_view,topic_delete_view,topic_list_view,create_topic_view
app_name = 'curriculum'
urlpatterns = [
    path('',grade_list_view.as_view(),name='grade_list_view'),
    path('make/',create_grade),
    path('<slug:slug>/',lesson_list_view.as_view(),name='lesson_list_view'),
    path('<str:standard>/<slug:slug>/',topic_list_view.as_view(),name='topic_list_view'),
    path('<str:standard>/<str:slug>/create/', create_topic_view.as_view(), name="creat_topic_view"),
    path('<str:standard>/<str:object>/<slug:slug>/', topic_detail_view.as_view(), name='topic_detail_view'),
    path('<str:standard>/<str:object>/<slug:slug>/update', topic_update_view.as_view(), name='topic_update_view'),
    path('<str:standard>/<str:object>/<slug:slug>/delete', topic_delete_view.as_view(), name='topic_delete_view'),
]