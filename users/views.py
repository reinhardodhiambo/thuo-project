from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from general.models import Counties, SubCounty
from users.models import Users
from django.shortcuts import redirect


def login(request):
    return render(request, template_name='car_reg/sign_in.html')


def administrator(request):
    users = Users.objects.all()
    return render(request, 'car_reg/admin.html', {'users': users})


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
            c = {'name': user.fullname, 'dob': user.dob,
                 'mobile': user.mobile,
                 'email': user.email,
                 'pin': user.pin,
                 'national_id': user.national_id}
            users.append(c)
    else:
        pass
    return Response(users)


# Add Users
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def addUsers(request):
    users_add = None

    if request.data['user_type'] == 3:
        users_add = Users(fullname=request.data['name'], dob=request.data['dob'],
                          mobile=request.data['mobile'], email=request.data['email'], pin=request.data['pin'],
                          national_id=request.data['national'],
                          password=request.data['password'], user_type=request.data['user_type'])
    else:
        users_add = Users(fullname=request.data['name'],  pin=request.data['pin'],
                          national_id=request.data['national'],
                          password=request.data['password'], user_type=request.data['user_type'])

    if users_add:
        users_add.save()
        # return Response(status=status.HTTP_201_CREATED)
        return render(request, template_name='car_reg/sign_in.html')
    return Response(status=status.HTTP_400_BAD_REQUEST)


# Edit Users
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def editUsers(request):
    users_edit = Users.objects.get(national_id=request.data['id'])

    if 'name' in request.data:
        users_edit.fullname = request.data['name']
    if 'dob' in request.data:
        users_edit.dob = request.data['dob']
    if 'mobile' in request.data:
        users_edit.mobile = request.data['mobile']
    if 'email' in request.data:
        users_edit.email = request.data['email']
    if 'pin' in request.data:
        users_edit.pin = request.data['pin']
    if 'password' in request.data:
        users_edit.password = request.data['password']

    users_edit.save()
    # response = {'success'}
    return Response(status=status.HTTP_201_CREATED)


# Edit Users
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def login_user(request):
    user = Users.objects.filter(national_id=request.data['id'], password=request.data['password'],
                                status='active').values()
    if user:
        return Response(user[0])
    else:
        return Response({'error': 'user not found'})


@api_view(http_method_names=['GET'])
@renderer_classes((JSONRenderer,))
def searchuser(request, id):
    user = Users.objects.filter(national_id=id).values()
    if user:
        return Response(user[0])
    else:
        return Response({'error': 'User not found'})


@api_view(http_method_names=['GET'])
@renderer_classes((JSONRenderer,))
def deactivateuser(request, id):
    user = Users.objects.get(national_id=id)
    if user:
        if user.status == 'active':
            user.status = 'inactive'
        else:
            user.status = 'active'
        user.save()
        return redirect('admin')
    else:
        return redirect('admin')
