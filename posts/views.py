from operator import ge
from xml.dom import ValidationErr
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.mixins import DestroyModelMixin
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

# Create your views here.
class PostAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
        
class PostRetriveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if request.user == post.poster:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('This is not your post!')
        
        # post = Post.objects.filter(pk=kwargs['pk'],poster=self.request.user)
        # if post.exists():
        #     self.destroy(request, *args, **kwargs)
        # else:
        #     raise ValidationError('This is not your!')
            
            

    
class VoteAPIView(generics.CreateAPIView, DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user,post=post)
    
    def perform_create(self, serializer):
        
        if self.get_queryset().exists():
            raise ValidationError('You vonted already for this post :)!')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
        
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Vont is not already!')


