# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie
from .serializers import MovieSerializer
from django.shortcuts import get_object_or_404

class MovieListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response({"list": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        movie_data = request.data.get('movie')
        if not movie_data:
            return Response({"status": 500, "reason": "Invalid data format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Проверяем, существует ли фильм с таким ID
        if Movie.objects.filter(id=movie_data.get('id')).exists():
            return Response({"status": 500, "reason": "Movie with this ID already exists"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = MovieSerializer(data=movie_data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response({"movie": MovieSerializer(movie).data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": 500, "reason": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        movie = get_object_or_404(Movie, id=id)
        serializer = MovieSerializer(movie)
        return Response({"movie": serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, id, *args, **kwargs):
        movie = get_object_or_404(Movie, id=id)
        movie_data = request.data.get('movie')
        if not movie_data:
            return Response({"status": 500, "reason": "Invalid data format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = MovieSerializer(movie, data=movie_data, partial=True)
        if serializer.is_valid():
            movie = serializer.save()
            return Response({"movie": MovieSerializer(movie).data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": 500, "reason": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            movie = get_object_or_404(Movie, id=id)
            movie.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except Movie.DoesNotExist:
            return Response({"status": 404, "reason": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": 500, "reason": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)