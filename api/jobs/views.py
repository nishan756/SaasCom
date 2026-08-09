from rest_framework.views import APIView
from .serializers import JobCategorySerializer , SkillSerializer , CurrencySerializer , Skill , JobCategory , Currency
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics , authentication , permissions

class JobCategoryListCreateView(APIView):

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
    
    def get_permissions(self):
        if self.request.method  == "POST":
            return [permissions.IsAdminUser()]
        return []

    def get_authenticators(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return []


class JobCategoryDetailUpdateDeleteView(APIView):

    def get_object(self , id):
        try: 
            JobCategory.objects.get(id = id)
        except JobCategory.DoesNotExist:
            return None


    def get(self , request , id , format = None):
        category = self.get_object(id)

        if not category:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = JobCategorySerializer(instance = category)

        return Response(data = serializer.data , status = status.HTTP_200_OK)

    def put(self, request, id, format=None):
        category = self.get_object(id)
        
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
        
    def get_permissions(self):
        if self.request.method in ["PUT" , "DELETE"]:
            return [permissions.IsAdminUser()]
        return []

    def get_authenticators(self):
        if self.request.method in ["PUT" , "DELETE"]:
            return [permissions.IsAdminUser()]
        return []
    

class SkillListCreateView(APIView):

    def get(self , request , format = None):
        skills = Skill.objects.all()
        serializer = SkillSerializer(instance = skills , many = True)
        return Response(data = serializer.data , status = status.HTTP_200_OK)

    def post(self , request , format = None):
        skill = request.data
        serializer = SkillSerializer(data = skill)

        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data , status = status.HTTP_201_CREATED)
        return Response(data = serializer.errors , status = status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return []
    
    def get_authenticators(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return []

class SkillDetailUpdateDeleteView(APIView):


    def get_object(self , id):
        try:
            return Skill.objects.get(id = id)
        except Skill.DoesNotExist:
            return None

    def get(self , request , id , format = None):
        skill = self.get_object(id)

        serializer = SkillSerializer(instance = skill)
        return Response(data = serializer.data , status = status.HTTP_200_OK)

    def put(self , request , id , format = None):

        skill = self.get_object(id)

        if not skill:
            return Response(status = status.HTTP_404_NOT_FOUND)

        updated_skill = request.data 

        serializer = SkillSerializer(instance = skill , data = updated_skill)

        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data , status = status.HTTP_200_OK)
        return Response(data = serializer.errors , status = status.HTTP_200_OK)
        

    def delete(self , request , id , format = None):
        skill = self.get_object(id)
        if not skill:
            return Response(status = status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ["PUT" , "DELETE"]:
            return [permissions.IsAdminUser()]
        return []

    def get_authenticators(self):
        if self.request.method in ["PUT" , "DELETE"]:
            return [permissions.IsAdminUser()]
        return []

class CurrencyListCreateView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_authenticators(self):
        if self.request.method == "POST":
            return [authentication.BasicAuthentication()]
        return []

class CurrencyDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [permissions.IsAdminUser()]

    def get_authenticators(self):
        if self.request.method == "GET":
            return []
        return [authentication.BasicAuthentication()]