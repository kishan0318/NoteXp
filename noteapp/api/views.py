from tkinter.tix import Tree
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import generics
from ..models import *


class SignupAPIView(APIView):
    permission_classes =[AllowAny,]

    def post(self,request):
        serializer=SignupSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            return Response({'Success':'user created successfully','data':data},status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

# class RegisterView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSer
#     permission_classes = [AllowAny, ]

class CRDNoteApiView(APIView):
    permission_classes =[IsAuthenticated,]

    def get(self, request,*args,**kwargs):
        if request.user.is_staff==True:
            queryset = Note.objects.all()
            serializer = NoteSer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            user = request.user
            queryset = Note.objects.filter(u_id=user,id=self.kwargs.get('pk'))
            serializer = NoteSer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
 
    def post(self, request):
        # print(request.user.id)
        serializer = NoteSer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "Note added successfully", 'data': serializer.data}, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self,request,*args,**kwargs):
        if request.user.is_staff==True:
            try:
                Note.objects.get(id=self.kwargs.get('pk')).delete()
                return Response({'Success':'Note deleted successfully'},status=HTTP_200_OK)
            except Exception as e:
                return Response({'Error':str(e)},status=HTTP_400_BAD_REQUEST)
        else:
            try:
                Note.objects.get(id=self.kwargs.get('pk'),u_id=request.user).delete()
                return Response({'Success':'Note deleted successfully'},status=HTTP_200_OK)
            except Exception as e:
                return Response({'Error':str(e)},status=HTTP_400_BAD_REQUEST)
 
TITLE_CHOICES = [
    ('1', 'Normal_user'),
    ('2', 'Employee'),
]

class AsdfView(APIView):
    permission_classes =[IsAuthenticated,]
    def post(self,request):
        user = request.user
        if user.is_staff==True:
                x='2'
        else:
                x='1'
        try:
            Profile.objects.get(user=user)
            return Response({'error':'User already exists'},status=HTTP_400_BAD_REQUEST)
        except:
            Profile.objects.create(user=user,address=request.data.get('address'),intrest=request.data.get('intrest'),dob=request.data.get('dob'),user_type=x)
            return Response({'Done':'profile added succesfully','data':True},status=HTTP_200_OK)
    
class LoginAPIView(APIView): 
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSer(data=request.data)
        if serializer.is_valid():
            return Response({'Success': 'login successfully', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'Error': 'login unsuccesfull', 'data': serializer.data},status=HTTP_400_BAD_REQUEST)

class UpdateNoteApi(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,*args,**kwargs):
        try:
            stu=Note.objects.get(id=self.kwargs.get('pk'))
        except:
            return Response({'Error':'Not found'},status=HTTP_404_NOT_FOUND)
        serializer=NoteSer1(instance=stu,data=request.data,context={'user':request.user})
        if serializer.is_valid():
           serializer.save()
           return Response({'success':'Successfull','data':serializer.data},status=HTTP_200_OK) 
        return Response(Serializer.errors,status=HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes =[IsAuthenticated,]
    def get(self, request):
        if request.user.is_staff==True:
            queryset = Profile.objects.all()
            serializer = ProfileSer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            queryset = Profile.objects.filter(user=request.user)
            serializer = ProfileSer(queryset, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
    
    def delete(self, request,*args,**kwargs):
        if request.user.is_staff==True:
            try:
                Profile.objects.get(user=self.kwargs.get('pk')).delete()
                # User.objects.get(id=self.kwargs.get('pk')).delete()
                return Response({'Success':'user deleted successfully'},status=HTTP_200_OK)
            except Exception as e:
                return Response({'Error':str(e)},status=HTTP_400_BAD_REQUEST)
        else:
            try:
                Profile.objects.get(user=request.user).delete()
                request.user.delete()
                return Response({'Success':'user deleted successfully'},status=HTTP_200_OK)
            except Exception as e:
                return Response({'Error':str(e)},status=HTTP_400_BAD_REQUEST)

    def put(self,request,*args,**kwargs):
        if request.user.is_staff==True:
            queryset=Profile.objects.get(id=self.kwargs.get('pk'))
            serializer=ProfileSer(instance=queryset,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'account': 'Updated successfully',"data":serializer.data},status=HTTP_201_CREATED)
            return Response(serializer.errors)
        else:
            queryset=Profile.objects.get(user=request.user)
            serializer=ProfileSer(instance=queryset,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'account': 'create successfully',"data":serializer.data},status=HTTP_201_CREATED)
            return Response(serializer.errors)
                    
    

   

        
    
