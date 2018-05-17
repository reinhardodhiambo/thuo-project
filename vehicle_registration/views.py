import json

import requests
from django.shortcuts import render

# Create your views here.
from django.template.defaultfilters import register
from numpy import unicode
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from general.models import Counties, SubCounty
from vehicle_registration.models import Vehicles, Owner
# from vehicle_registration.models import Details
import pickle
import hashlib as hasher
import datetime as date

# def __init__(self, index, timestamp, data, previous_hash):
#     self.index = index
#     self.timestamp = timestamp
#     self.data = data
#     self.previous_hash = previous_hash
#     self.hash = self.hash_block()


# Hashing a Block - Hashing Algorithm
from vehicle_transfer.models import Details


# @api_view(http_method_names=['POST'])
# @renderer_classes((JSONRenderer,))
# def hash_block(block):
#     sha = hasher.sha3_256()
#     sha.update(str(block).encode('utf-8'))
#     sha.digest()
#     m = sha.hexdigest()
#
#     return m

@register.filter(name='range')
def filter_year(start, end):
    return range(start, end)


def hash_block(block):
    sha = hasher.sha3_256()
    sha.update(pickle.dumps(block))
    m = sha.hexdigest()

    return m


# Genesis Block - Add Vehicle
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carRegistration(request):
    car_reg = Vehicles.objects.filter(reg_no=request.data['reg'].upper()).values()
    if car_reg:
        return Response({'error': 'Vehicle exist'})
    else:
        cars = dict()
        # cars = []

        car_add = Vehicles(reg_no=request.data['reg'].upper(), vehicle_type=request.data['type'],
                           make=request.data['make'],
                           vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])
        response = {'reg_no': car_add.reg_no.upper(), 'type': car_add.vehicle_type, 'make': car_add.make,
                    'model': car_add.vehicle_model, 'year': car_add.year_of_manufacture,
                    'parent_hash': car_add.previous_hash, 'date_time': date.datetime.now()}
        genesishash = hash_block(response)
        car_add.hash = genesishash
        # genesisBlock = {'hash': car_add.hash, 'contents': response}
        # cars.update(genesisBlock)
        # cars.append(genesisBlock)

        car_add.save()
        res = {'reg_no': car_add.reg_no, 'type': car_add.vehicle_type, 'make': car_add.make,
               'model': car_add.vehicle_model, 'year': car_add.year_of_manufacture,
               'parent_hash': car_add.previous_hash, 'date_time': date.datetime.now(), 'hash': car_add.hash}

        return Response(res)
        # return Response(cars)


# #Genesis Block - Add Vehicle
# @api_view(http_method_names=['POST'])
# @renderer_classes((JSONRenderer,))
# def carRegistration(request):
#
#     cars_reg = _careg(request)
#
#     if cars_reg:
#         return Response(cars_reg)
#
#     return Response(status=status.HTTP_400_BAD_REQUEST)
#


# Add Vehicle Owner
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carRegistrationOwner(request):
    owner = _registrationCarOwner(request)

    if owner:
        return Response(owner)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# Transfer Vehicle
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carTransfer(request):
    transfer = _transferCar(request)

    if transfer:
        return Response(transfer)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# Confirm Vehicle Transfer
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carTransferConfirmation(request):
    confirm = _confirmCar(request)

    if confirm:
        return Response(confirm)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, template_name='car_reg/index.html')


# Add Car Registration
def addCarDetails(request):
    return render(request, 'car_reg/vehicle_registration.html')


# Add View
def addCarRegistrationView(request):
    return render(request, 'car_reg/vehicle_registration_details.html')


def _careg(request):
    car_reg = Vehicles.objects.all()
    if car_reg:

        for car in car_reg:
            exist = car.reg_no
            new = request.data['reg']

            if exist == new:
                print('Vehicle Already Registered')
                # return Response(status=status.HTTP_400_BAD_REQUEST)

    else:

        cars = dict()

        car_add = Vehicles(reg_no=request.data['reg'], vehicle_type=request.data['type'], make=request.data['make'],
                           vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])
        if car_add:
            response = {'reg_no': car_add.reg_no, 'type': car_add.vehicle_type, 'make': car_add.make,
                        'model': car_add.vehicle_model, 'year': car_add.year_of_manufacture,
                        'parent_hash': car_add.previous_hash, 'date_time': date.datetime.now()}
            genesisHash = hash_block(response)
            car_add.hash = genesisHash
            genesisBlock = {'hash': car_add.hash, 'contents': response}
            cars.update(genesisBlock)

            car_add.save()

            return cars
        else:
            return False


def _registrationCarOwner(request):
    # car_owner = Owner.objects.all()
    car_owner = Owner.objects.filter(reg_id=request.data['reg']).values()
    if car_owner:
        return {'error': 'Vehicle exist'}
    else:
        owner = dict()
        # How many blocks should we add to the chain after the genesis block
        car_reg = Vehicles.objects.get(reg_no=request.data['reg'])
        car_owner_add = Owner(fullname=request.data['name'], national_id=request.data['national'],
                              mobile=request.data['mobile'],
                              dob=request.data['dob'], pin=request.data['pin'],
                              email=request.data['email'], reg_id=request.data['reg'],
                              vehicle_type=request.data['type'], make=request.data['make'],
                              vehicle_model=request.data['model'],
                              year_of_manufacture=request.data['year'], previous_hash=car_reg.hash)

        response = {'name': car_owner_add.fullname, 'national': car_owner_add.national_id,
                    'mobile': car_owner_add.mobile, 'dob': car_owner_add.dob,
                    'pin': car_owner_add.pin, 'email': car_owner_add.email,
                    'reg_no': car_owner_add.reg_id, 'type': car_owner_add.vehicle_type,
                    'make': car_owner_add.make, 'model': car_owner_add.vehicle_model,
                    'year': car_owner_add.year_of_manufacture,
                    'parent_hash': car_owner_add.previous_hash,
                    'date_time': date.datetime.now()}

        blockHash = hash_block(response)
        car_owner_add.hash = blockHash
        block = {'hash': car_owner_add.hash, 'contents': response}
        owner.update(block)
        car_owner_add.save()
        return owner


def _transferCar(request):
    transfer = Details.objects.filter(reg_id=request.data['reg'], vehicle_status=0,
                                      national_id=request.data['national']).values()
    if transfer:
        return {'error': 'Vehicle Already Transferred'}
    else:
        transfer = dict()

        # Create the blockchain and add the previous car registration block

        car_trans = Owner.objects.get(owner_id=request.data['owner'])

        car_transfer = Details(owner_id=request.data['owner'], fullname=request.data['name'],
                               national_id=request.data['national'], mobile=request.data['mobile'],
                               dob=request.data['dob'], pin=request.data['pin'],
                               email=request.data['email'], reg_id=request.data['reg'],
                               vehicle_type=request.data['type'], make=request.data['make'],
                               vehicle_model=request.data['model'],
                               year_of_manufacture=request.data['year'],
                               previous_owner_name=request.data['p_name'],
                               previous_owner_mobile=request.data['p_mobile'],
                               previous_owner_email=request.data['p_email'], previous_hash=car_trans.hash)

        response = {'name': car_transfer.fullname, 'national': car_transfer.national_id,
                    'mobile': car_transfer.mobile,
                    'dob': car_transfer.dob,
                    'pin': car_transfer.pin, 'email': car_transfer.email,
                    'reg_no': car_transfer.reg_id,
                    'type': car_transfer.vehicle_type,
                    'make': car_transfer.make, 'model': car_transfer.vehicle_model,
                    'year': car_transfer.year_of_manufacture,
                    'previous_owner_name': car_transfer.previous_owner_name,
                    'previous_owner_mobile': car_transfer.previous_owner_mobile,
                    'previous_owner_email': car_transfer.previous_owner_email,
                    'vehicle_status': car_transfer.vehicle_status,
                    'parent_hash': car_transfer.previous_hash,
                    'date_time': date.datetime.now()}

        blockHash = hash_block(response)
        car_transfer.hash = blockHash
        block = {'hash': car_transfer.hash, 'contents': response}
        transfer.update(block)

        car_transfer.save()
        return transfer


def _confirmCar(request):
    car_registration_edit = Owner.objects.get(owner_id=request.data['owner'])
    car_transfer_edit = Details.objects.get(owner_id=request.data['owner'])

    confirm_car = Details.objects.filter(reg_id=car_transfer_edit.reg_id, vehicle_status=0,
                                         owner_id=request.data['owner']).values()
    if confirm_car:

        confirm = dict()
        # Create the blockchain and add the previous car registration block
        car_registration_edit.vehicle_status = 'transferred'
        car_transfer_edit.vehicle_status = '1'
        # car_transfer_edit.save()
        car_owner_add = Owner(fullname=car_transfer_edit.fullname, national_id=car_transfer_edit.national_id,
                              mobile=car_transfer_edit.mobile,
                              dob=car_transfer_edit.dob, pin=car_transfer_edit.pin,
                              email=car_transfer_edit.email, reg_id=car_transfer_edit.reg_id,
                              vehicle_type=car_transfer_edit.vehicle_type, make=car_transfer_edit.make,
                              vehicle_model=car_transfer_edit.vehicle_model,
                              year_of_manufacture=car_transfer_edit.year_of_manufacture,
                              previous_hash=car_transfer_edit.previous_hash)

        response = {'name': car_owner_add.fullname, 'national': car_owner_add.national_id,
                    'mobile': car_owner_add.mobile, 'dob': car_owner_add.dob,
                    'pin': car_owner_add.pin, 'email': car_owner_add.email,
                    'reg_no': car_owner_add.reg_id, 'type': car_owner_add.vehicle_type,
                    'make': car_owner_add.make, 'model': car_owner_add.vehicle_model,
                    'year': car_owner_add.year_of_manufacture,
                    'parent_hash': car_owner_add.previous_hash,
                    'date_time': date.datetime.now()}

        blockHash = hash_block(response)
        car_owner_add.hash = blockHash
        block = {'hash': car_owner_add.hash, 'contents': response}
        car_registration_edit.save()
        car_transfer_edit.save()
        car_owner_add.save()

        confirm.update(block)
        return confirm

    else:
        return {'error': 'Vehicle Transfer Already Accepted'}

        # def _careg(request):
        #     car_reg = Vehicles.objects.all()
        #     print("Welcome")
        #     if car_reg:
        #
        #         for car in car_reg:
        #             exist = car.reg_no
        #             new = request.data['reg']
        #
        #             if exist == new:
        #                 print('Vehicle Already Registered')
        #                 # return Response(status=status.HTTP_400_BAD_REQUEST)
        #
        #     else:
        #
        #         cars = dict()
        #
        #         car_add = Vehicles(reg_no=request.data['reg'], vehicle_type=request.data['type'], make=request.data['make'],
        #                            vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])
        #         if car_add:
        #             response = {'reg_no': car_add.reg_no, 'type': car_add.vehicle_type, 'make': car_add.make,
        #                         'model': car_add.vehicle_model, 'year': car_add.year_of_manufacture,
        #                         'block_no': 0, 'parent_hash': '0', 'date_time': date.datetime.now()}
        #             genesisHash = hash_block(response)
        #             genesisBlock = {'hash': genesisHash, 'contents': response}
        #             cars.update(genesisBlock)
        #
        #             car_add.save()
        #
        #             return cars
        #         else:
        #             return False

        # def _registrationCarOwner(request):
        #     car_owner = Owner.objects.all()
        #
        #     if car_owner:
        #         for car in car_owner:
        #             exist = car.reg_id
        #             new = request.data['reg']
        #
        #             if exist == new:
        #                 print('Vehicle Already Registered')
        #
        #             else:
        #
        #                 owner = dict()
        #
        #                 # Create the blockchain and add the genesis block
        #                 blockchain = _careg(request)
        #
        #                 # previous_block = blockchain.text
        #                 # chain = json.dumps(previous_block)
        #                 # chain2 = json.loads(chain)
        #                 # print(chain2[0])
        #                 parent_hash = blockchain['hash']
        #                 block_no = blockchain['contents']['block_no'] + 1
        #                 print('Parent Hash$$$$$', blockchain)
        #
        #                 # block_num = json.loads(block_number)
        #                 # block_num = json.loads(block_number)
        #                 # block_no = block_num('contents', 'block_no')
        #
        #                 # How many blocks should we add to the chain after the genesis block
        #                 num_of_blocks_to_add = 100
        #                 for i in range(0, num_of_blocks_to_add):
        #
        #                     car_owner_add = Owner(fullname=request.data['name'], national_id=request.data['national'], mobile=request.data['mobile'],
        #                                       dob=request.data['dob'], pin=request.data['pin'],
        #                                       email=request.data['email'], reg_id=request.data['reg'],
        #                                       vehicle_type=request.data['type'], make=request.data['make'],
        #                                       vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])
        #
        #                     if car_owner_add:
        #
        #                         response = {'name': car_owner_add.fullname, 'national': car_owner_add.national_id, 'mobile': car_owner_add.mobile, 'dob': car_owner_add.dob,
        #                                     'pin': car_owner_add.pin, 'email': car_owner_add.email, 'reg_no': car_owner_add.reg_id, 'type': car_owner_add.vehicle_type,
        #                                     'make': car_owner_add.make, 'model': car_owner_add.vehicle_model, 'year': car_owner_add.year_of_manufacture,
        #                                     'block_no': block_no, 'parent_hash': parent_hash, 'date_time':date.datetime.now()}
        #
        #                         blockHash = hash_block(response)
        #                         block = {'hash': blockHash, 'contents': response}
        #                         owner.update(block)
        #
        #                         car_owner_add.save()
        #
        #                         # response2 = {'name': car_add.fullname, 'national': car_add.national_id, 'mobile': car_add.mobile, 'dob': car_add.dob,
        #                         #             'pin': car_add.pin, 'email': car_add.email, 'reg_no': car_add.reg_no, 'type': car_add.vehicle_type,
        #                         #             'make': car_add.make, 'model': car_add.vehicle_model, 'last_block': m.hexdigest(), 'nonce': 0}
        #                         # #return Response(response2)
        #                         return owner
        #
        #                     else:
        #                         return False

        # def _transferCar(request):
        #     transfer = Details.objects.all()
        #
        #     if transfer:
        #         for trans in transfer:
        #             exist_reg = trans.reg_id
        #             new_reg = request.data['reg']
        #
        #             exist_status = trans.vehicle_status
        #
        #             if exist_reg == new_reg and exist_status == '0':
        #                 print('Vehicle Already Transferred')
        #
        #             else:
        #
        #                 transfer = dict()
        #
        #                 # Create the blockchain and add the previous car registration block
        #                 blockchain = _registrationCarOwner(request)
        #                 parent_hash = blockchain['hash']
        #                 block_number = blockchain['contents']['block_no'] + 1
        #
        #                 car_transfer = Details(owner_id=request.data['owner'], fullname=request.data['name'],
        #                                        national_id=request.data['national'], mobile=request.data['mobile'],
        #                                        dob=request.data['dob'], pin=request.data['pin'],
        #                                        email=request.data['email'], reg_id=request.data['reg'],
        #                                        vehicle_type=request.data['type'], make=request.data['make'],
        #                                        vehicle_model=request.data['model'], year_of_manufacture=request.data['year'],
        #                                        previous_owner_name=request.data['p_name'],
        #                                        previous_owner_mobile=request.data['p_mobile'], previous_owner_email=request.data['p_email'])
        #
        #                 if car_transfer:
        #                     response = {'name': car_transfer.fullname, 'national': car_transfer.national_id, 'mobile': car_transfer.mobile,
        #                                 'dob': car_transfer.dob,
        #                                 'pin': car_transfer.pin, 'email': car_transfer.email, 'reg_no': car_transfer.reg_id,
        #                                 'type': car_transfer.vehicle_type,
        #                                 'make': car_transfer.make, 'model': car_transfer.vehicle_model,
        #                                 'year': car_transfer.year_of_manufacture,
        #                                 'previous_owner_name': car_transfer.previous_owner_name,
        #                                 'previous_owner_mobile': car_transfer.previous_owner_mobile,
        #                                 'previous_owner_email': car_transfer.previous_owner_email,
        #                                 'vehicle_status': car_transfer.vehicle_status,
        #                                 'block_no': block_number, 'parent_hash': parent_hash, 'date_time': date.datetime.now()}
        #
        #                     blockHash = hash_block(response)
        #                     block = {'hash': blockHash, 'contents': response}
        #                     transfer.update(block)
        #                     car_transfer.save()
        #
        #                     # response2 = {'name': car_transfer.fullname, 'national': car_transfer.national_id, 'mobile': car_transfer.mobile, 'dob': car_transfer.dob,
        #                     #             'pin': car_transfer.pin, 'email': car_transfer.email, 'reg_no': car_transfer.reg_id, 'type': car_transfer.vehicle_type,
        #                     #             'make': car_transfer.make, 'model': car_transfer.vehicle_model, 'previous_owner_name': car_transfer.previous_owner_name,
        #                     #             'previous_owner_mobile': car_transfer.previous_owner_mobile, 'previous_owner_email': car_transfer.previous_owner_email,
        #                     #             'vehicle_status': car_transfer.vehicle_status, 'last_block': n.hexdigest(), 'nonce': 0}
        #                     return transfer
        #
        #                 else:
        #                     return False

        # def _confirmCar(request):
        #     car_registration_edit = Owner.objects.get(owner_id=request.data['owner'])
        #     car_transfer_edit = Details.objects.get(transfer_id=request.data['transfer'])
        #
        #     confirm = dict()
        #
        #     # Create the blockchain and add the previous car registration block
        #     blockchain = _registrationCarOwner(request)
        #     parent_hash = blockchain['hash']
        #     block_number = blockchain['contents']['block_no'] + 1
        #
        #     transfer_confirm = Details(owner_id=request.data['p_owner_id'], fullname=request.data['name'],
        #                                national_id=request.data['national'],
        #                                mobile=request.data['mobile'], dob=request.data['dob'], pin=request.data['pin'],
        #                                email=request.data['email'], reg_id=request.data['reg'],
        #                                vehicle_type=request.data['type'], make=request.data['make'],
        #                                vehicle_model=request.data['model'], year_of_manufacture=request.data['year'],
        #                                previous_owner_name=request.data['p_name'],
        #                                previous_owner_mobile=request.data['p_mobile'],
        #                                previous_owner_email=request.data['p_email'])
        #
        #     if car_registration_edit and car_transfer_edit:
        #         car_registration_edit.vehicle_status = 'transferred'
        #         car_transfer_edit.vehicle_status = '1'
        #     # car_transfer_edit.save()
        #
        #     if transfer_confirm and car_registration_edit and car_transfer_edit:
        #         response = {'transfer_id': transfer_confirm.transfer_id, 'name': transfer_confirm.fullname,
        #                     'national': transfer_confirm.national_id, 'mobile': transfer_confirm.mobile,
        #                     'dob': transfer_confirm.dob,
        #                     'pin': transfer_confirm.pin, 'email': transfer_confirm.email, 'reg_no': transfer_confirm.reg_id,
        #                     'type': transfer_confirm.vehicle_type,
        #                     'make': transfer_confirm.make, 'model': transfer_confirm.vehicle_model,
        #                     'year': transfer_confirm.year_of_manufacture,
        #                     'previous_owner_name': transfer_confirm.previous_owner_name,
        #                     'previous_owner_mobile': transfer_confirm.previous_owner_email,
        #                     'previous_owner_email': transfer_confirm.previous_owner_email,
        #                     'vehicle_status': car_transfer_edit.vehicle_status,
        #                     'block_no': block_number, 'parent_hash': parent_hash, 'date_time': date.datetime.now()}
        #
        #         blockHash = hash_block(response)
        #         block = {'hash': blockHash, 'contents': response}
        #         transfer_confirm.save()
        #         car_registration_edit.save()
        #         car_transfer_edit.save()
        #         confirm.update(block)
        #
        #         # response2 = {'name': transfer_confirm.fullname, 'national': transfer_confirm.national_id, 'mobile': transfer_confirm.mobile, 'dob': transfer_confirm.dob,
        #         #             'pin': transfer_confirm.pin, 'email': transfer_confirm.email, 'reg_no': transfer_confirm.reg_id, 'type': transfer_confirm.vehicle_type,
        #         #             'make': transfer_confirm.make, 'model': transfer_confirm.vehicle_model, 'previous_owner_name': transfer_confirm.previous_owner_name,
        #         #             'previous_owner_mobile': transfer_confirm.previous_owner_mobile, 'previous_owner_email': transfer_confirm.previous_owner_email,
        #         #             'last_block': m.hexdigest(), 'nonce': 0}
        #
        #         return confirm
        #
        #     else:
        #         return False
