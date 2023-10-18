from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, StudentViewSet, EnrolmentCreateView, InstructorsListView, InstructorsDetailView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('instructor/', InstructorsListView.as_view()),
    path('instructor/<pk>', InstructorsDetailView.as_view()),
    path('', include(router.urls)),
    path('Enroll/', EnrolmentCreateView.as_view()),
]
