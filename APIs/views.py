from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Course, Student, Instructor
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer, InstructorSerializer


# ViewSet _______________________________________________________
class CourseViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="List All Courses with instructors",
        responses={200: CourseSerializer(many=True)}
    )
    def list(self, request):
        try:
            queryset = Course.objects.all()
            serializer = CourseSerializer(queryset, many=True)
            return Response({
                "isError": False,
                "message": "List of All Courses",
                "exception": "",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": str(e),
                "data": ""
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @swagger_auto_schema(
        operation_description="Create a Course",
        request_body=CourseSerializer(),
        responses={201: "Course Created Successfully"}
    )
    def create(self, request):
        try:
            payload = request.data
            serializer = CourseSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "isError": False,
                    "message": "Course is created successfully",
                    "exception": "",
                    "data": ""
                }, status=status.HTTP_201_CREATED
                )
            else:
                return Response({
                    "isError": True,
                    "message": "Something went wrong",
                    "exception": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": str(e),
                "data": ""
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @swagger_auto_schema(
        operation_description="Get Detail",
        responses={200: CourseSerializer()}
    )
    def retrieve(self, request, pk=None):
        try:
            instance = Course.objects.get(pk=pk)
        except Exception as e:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CourseSerializer(instance)
        return Response({
            "isError": False,
            "message": "Course Details",
            "exception": "",
            "data": serializer.data
        }, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Update a course",
        request_body=CourseSerializer(),
        responses={201: CourseSerializer()}
    )
    def update(self, request, pk=None):
        try:
            instance = Course.objects.get(pk=pk)
        except Exception as e:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CourseSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "isError": False,
                "message": "Course is updated successfully",
                "exception": "",
                "data": serializer.data
            }, status=status.HTTP_200_OK
            )
        else:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": serializer.errors,
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Delete a course",
        responses={204: "Success"}
    )
    def destroy(self, request, pk=None):
        try:
            instance = Course.objects.get(pk=pk)
        except Exception as e:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        instance.save()
        return Response({
            "isError": False,
            "message": "Course is Deleted successfully",
            "exception": "",
            "data": ""
        }, status=status.HTTP_204_NO_CONTENT
        )


# ModelViewSet _______________________________________________________
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# APIView _____________________________________________________________
class EnrolmentCreateView(APIView):
    @swagger_auto_schema(
        operation_description="update description override",
        request_body=EnrollmentSerializer(),
        responses={201: EnrollmentSerializer()}
    )
    def post(self, request):
        payload = request.data
        serializer = EnrollmentSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            course = Course.objects.filter(id=payload.get("course")).first()
            student = Student.objects.filter(id=payload.get("student")).first()
            student.courses.add(course)
            return Response({
                "isError": False,
                "message": "Student is Enrolled successfully",
                "exception": "",
                "data": ""
            }, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({
                "isError": True,
                "message": "Something went wrong",
                "exception": serializer.errors,
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST
            )


# generic views ______________________________________
class InstructorsListView(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer


class InstructorsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
