from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.gis.db.models.functions import AsGeoJSON
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Driver, Truck, Company
from .serializers import DriverSerializer, TruckSerializer, CompanySerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import json

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_drivers(request, format=None):
    """
    Returns a JSONResponse of all drivers.
    """
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return JsonResponse({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_companies(request, format=None):
    """
    Returns a JSONResponse of all companies.
    """
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = DriverSerializer(companies, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return JsonResponse({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def list_trucks(request, format=None):
    """
    Returns a JSONResponse of all trucks.
    """
    if request.method == 'GET':
        trucks = Truck.objects.all()
        serializer = TruckSerializer(trucks, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return JsonResponse({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_driver(request, format=None):
    """
    Creates a driver and returns a JSONResponse of the created driver.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DriverSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_company(request, format=None):
    """
    Creates a company and returns a JSONResponse of the created company.
    """
    if request.method == 'POST':
        print(request)
        data = JSONParser().parse(request)
        print(data)
        serializer = CompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_truck(request, format=None):
    """
    Creates a truck and returns a JSONResponse of the created truck.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        #data['current_location'] = 
        serializer = TruckSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes((permissions.AllowAny,))
def driver_detail(request, pk, format=None):
    """
    Retrieve, update or delete a driver by primary key.
    """
    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return JsonResponse({"error": "Driver does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DriverSerializer(driver, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        driver.delete()
        return JsonResponse({"message": "Driver ID {} successfully deleted.".format(driver.id)},status=204)

@api_view(['GET','PUT','DELETE'])
@permission_classes((permissions.AllowAny,))
def company_detail(request, pk, format=None):
    """
    Retrieve, update or delete a company by primary key.
    """
    try:
        company = Company.objects.get(pk=pk)
        print(company)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        print(serializer)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(company, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        company.delete()
        return JsonResponse({"message": "Company ID {} successfully deleted.".format(company.id)},status=204)

@api_view(['GET','PUT','DELETE'])
@permission_classes((permissions.AllowAny,))
def truck_detail(request, pk, format=None):
    """
    Retrieve, update or delete a truck by primary key.
    """
    try:
        truck = Truck.objects.get(pk=pk)
    except Truck.DoesNotExist:
        return JsonResponse({"error": "Truck does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TruckSerializer(truck)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TruckSerializer(truck, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        truck.delete()
        return JsonResponse({"message": "Truck ID {} successfully deleted.".format(truck.id)},status=204)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_closest_truck(request, format=None):
    """
    Returns a JSONResponse of the closest truck to a given lat/lng and the distance from that point.
    """
    if request.method == 'GET':
        model = Truck
        try:
            lat = float(request.GET.get('lat'))
            lng = float(request.GET.get('lng'))
            assert lat >= -180 and lat <= 180
            assert lng >= -180 and lng <= 180
        except:
            return JsonResponse({"error": "Invalid or missing query parameters lat, lng."}, status=status.HTTP_400_BAD_REQUEST)

        location = Point(lat, lng, srid=4326)
        closest = Truck.objects.annotate(distance=Distance('current_location',location)).annotate(current_location_geojson=AsGeoJSON('current_location')).order_by('distance')[0]
        return JsonResponse({"id": closest.id, "current_driver": closest.current_driver_id, "current_location": json.loads(closest.current_location_geojson), "distance": closest.distance.m})

        
        