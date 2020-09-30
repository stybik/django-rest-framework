from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins



# Generic Views
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
	serializer_class = ArticleSerializer
	queryset = Article.objects.all()

	lookup_field = 'id'

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)
		else:
			return self.list(request)

	def post(self, request):
		return self.create(request)

	def put(self, request, id=None):
		return self.update(request, id)

	def delete(self, request, id=None):
		return self.destroy(request, id)



# Function based views
@api_view(['GET', 'POST'])
def article_list(request):
	"""Serialize all data from article model,
	create record in article model"""
	if request.method == 'GET':
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data)

	elif request.method == "POST":
		serializer = ArticleSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
	"""get details of single article, 
	update an article,
	delete an article"""
	try:
		article = Article.objects.get(id=pk)
	except Article.DoestNotExist:
		return HttpResponse(status=status.HTTP_201_NOT_FOUND)

	if request.method == "GET":
		serializer = ArticleSerializer(article)
		return Response(serializer.data)

	elif request.method == "PUT":
		serializer = ArticleSerializer(article, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == "DELETE":
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


# Class Based Views
class ArticleAPIView(APIView):

	def get(self, request):
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = ArticleSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 		


class ArticleDetails(APIView):

	def get_object(self, id):
		try:
			return Article.objects.get(id=id)
		except Article.DoestNotExist:
			return HttpResponse(status=status.HTTP_201_NOT_FOUND)

	def get(self, request, id):
		article = self.get_object(id)
		serializer = ArticleSerializer(article)
		return Response(serializer.data)

	def put(self, request, id):
		article = self.get_object(id)
		serializer = ArticleSerializer(article, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id):
		article = self.get_object(id)
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
