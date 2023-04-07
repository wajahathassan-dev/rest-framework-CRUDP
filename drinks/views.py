from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# GET '/drinks'  -> Get all drinks
# POST '/drinks' -> Add new drink

@api_view(['GET', 'POST'])
def drink_list(request):
    if request.method == 'GET':
        # get all the drinks
        drinks = Drink.objects.all()
        # serialize them
        serializer = DrinkSerializer(drinks, many=True)
        # return json
        return JsonResponse({"drinks": serializer.data})
    else:
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# GET '/drinks/<int:id>'       -> Send a specific drink based on id
# PUT '/drinks/<int:id>'       -> Update a specific drink based on id
# PATCH '/drinks/<int:id>'     -> Update name of a specific drink based on id
# DELETE '/drinks/<int:id>'    -> Delete a specific drink based on id

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def drink_detail(request, id):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response({
            "success": False
        }, status=status.HTTP_200_OK)
    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response({"success": True, "drink": serializer.data})
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": "Please provide all fields"}, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        if "name" not in request.data and "description" not in request.data:
            return Response({"success": False, "message": "Please provide either name or description field"})
        serializer = DrinkSerializer(drink, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response({"success": False})
    else:
        drink.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
