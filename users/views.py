from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from general.models import Counties, SubCounty
from users.models import Users


def login(request):
    return render(request, template_name='car_reg/sign_in.html')


def administrator(request):
    return render(request, template_name='car_reg/admin.html')


def register(request):
    return render(request, template_name='car_reg/sign_up.html')


# All Users
@api_view(http_method_names=['GET'])
@renderer_classes((JSONRenderer,))
def allUsers(request):
    all_users = Users.objects.all()

    users = []

    if all_users:
        for user in all_users:
            counties = Counties.objects.get(county_id=user.county)
            subcounty = SubCounty.objects.get(subcounty_id=user.subcounty)
            c = {'name': user.fullname, 'gender': user.gender, 'dob': user.dob, 'occupation': user.occupation,
                 'mobile': user.mobile,
                 'email': user.email, 'county': counties.county_name, 'subcounty': subcounty.subcounty_name,
                 'pin': user.pin,
                 'national_id': user.national_id, 'nationality': user.nationality,
                 'physical_address': user.physical_address, 'box': user.box,
                 'code': user.code, 'town': user.town}
            users.append(c)
    else:
        pass
    return Response(users)


# Add Users
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def addUsers(request):
    users_add = Users(fullname=request.data['name'], gender=request.data['gender'], dob=request.data['dob'],
                      occupation=request.data['occupation'],
                      mobile=request.data['mobile'], email=request.data['email'], pin=request.data['pin'],
                      national_id=request.data['national'], nationality=request.data['nationality'],
                      physical_address=request.data['address'],
                      box=request.data['box'], code=request.data['code'], town=request.data['town'],
                      password=request.data['password'])

    if users_add:
        users_add.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# Edit Users
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def editUsers(request):
    users_edit = Users.objects.get(national_id=request.data['id'])

    if 'name' in request.data:
        users_edit.fullname = request.data['name']
    if 'gender' in request.data:
        users_edit.gender = request.data['gender']
    if 'dob' in request.data:
        users_edit.dob = request.data['dob']
    if 'occupation' in request.data:
        users_edit.occupation = request.data['occupation']
    if 'mobile' in request.data:
        users_edit.mobile = request.data['mobile']
    if 'email' in request.data:
        users_edit.email = request.data['email']
    if 'pin' in request.data:
        users_edit.pin = request.data['pin']
    if 'nationality' in request.data:
        users_edit.nationality = request.data['nationality']
    if 'address' in request.data:
        users_edit.physical_address = request.data['address']
    if 'box' in request.data:
        users_edit.box = request.data['box']
    if 'code' in request.data:
        users_edit.code = request.data['code']
    if 'town' in request.data:
        users_edit.town = request.data['town']
    if 'password' in request.data:
        users_edit.password = request.data['password']

    users_edit.save()
    # response = {'success'}
    return Response(status=status.HTTP_201_CREATED)


# Edit Users
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def login_user(request):
    user = Users.objects.filter(national_id=request.data['id'], password=request.data['password']).values()
    if user:
        return Response(user[0])
    else:
        return Response({'error': 'user not found'})
