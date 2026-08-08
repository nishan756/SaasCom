from rest_framework.views import APIView
from .serializers import JobCategorySerializer , SkillSerializer , CurrencySerializer , Skill , JobCategory
from rest_framework.response import Response
from rest_framework import status

class JobCategoryView(APIView):

    def get(self , request , format = None):
        categories = JobCategory.objects.all()
        serializer = JobCategorySerializer(many = True , instance = categories)
        return Response(data = serializer.data , status = status.HTTP_200_OK)

    def post(self , request , format = None):

        category = request.data
        serializer = JobCategorySerializer(data = category)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data , status = status.HTTP_201_CREATED)

        return Response(data = serializer.errors , status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        try:
            category = JobCategory.objects.get(id=id)

        except JobCategory.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobCategorySerializer(
            instance=category,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )

    def delete(self , request , id , format = None):

        try:
            category = JobCategory.objects.get(id = id)
            category.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except JobCategory.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    
