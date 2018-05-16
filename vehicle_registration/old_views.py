import json

import requests
from django.shortcuts import render

# Create your views here.
from numpy import unicode
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from general.models import Counties, SubCounty
from vehicle_registration.models import Vehicles, Owner
#from vehicle_registration.models import Details
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

def hash_block(block):
    sha = hasher.sha3_256()
    sha.update(pickle.dumps(block))
    m = sha.hexdigest()

    return m

def registerCar(request):
    cars = dict()

    car_add = Vehicles(reg_no=request.data['reg'], vehicle_type=request.data['type'], make=request.data['make'],
                       vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])

    if car_add:
        response = {'reg_no': car_add.reg_no, 'type': car_add.vehicle_type, 'make': car_add.make,
                    'model': car_add.vehicle_model, 'year': car_add.year_of_manufacture,
                    'block_no': 0, 'parent_hash': '0', 'date_time': date.datetime.now()}
        genesisHash = hash_block(response)
        genesisBlock = {'hash': genesisHash, 'contents': response}
        cars.update(genesisBlock)

        car_add.save()

    else:
        print('Unable to save the data.')
        # return Response(status=status.HTTP_400_BAD_REQUEST)

    return cars

# #Genesis Block - Add Vehicle
# @api_view(http_method_names=['POST'])
# @renderer_classes((JSONRenderer,))
# def carRegistration(request):
#
#     cars = dict()
#
#     car_add = Vehicles(reg_no=request.data['reg'], vehicle_type=request.data['type'], make=request.data['make'],
#                       vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])
#
#     if car_add:
#
#         response = {'reg_no': car_add.reg_no, 'type': car_add.vehicle_type, 'make': car_add.make,
#                     'model': car_add.vehicle_model, 'year': car_add.year_of_manufacture,
#                     'block_no': 0, 'parent_hash': '0', 'date_time':date.datetime.now()}
#         genesisHash = hash_block(response)
#         genesisBlock = {'hash': genesisHash, 'contents': response}
#         cars.update(genesisBlock)
#
#         car_add.save()
#
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     return Response(cars)

#Genesis Block - Add Vehicle
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carRegistration(request):

    cars = registerCar(request)

    if cars:

        return Response(cars)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)





# # Add Vehicle Owner
# @api_view(http_method_names=['POST'])
# @renderer_classes((JSONRenderer,))
# def carRegistrationOwner(request):
#
#     owner = []
#
#     # Create the blockchain and add the genesis block
#     blockchain = requests.post('http://localhost:8000/vehicle_reg/add_vehicle')
#
#     previous_block = blockchain.text
#     chain = json.dumps(previous_block)
#     chain2 = json.loads(chain)
#     print(chain2[0])
#     parent_hash = previous_block[1]
#     # block_no = blockchain.contents.block_no
#     print('Parent Hash$$$$$', blockchain)
#
#     # block_num = json.loads(block_number)
#     # block_num = json.loads(block_number)
#     # block_no = block_num('contents', 'block_no')
#
#     # How many blocks should we add to the chain after the genesis block
#     num_of_blocks_to_add = 100
#     for i in range(0, num_of_blocks_to_add):
#
#         car_owner_add = Owner(fullname=request.data['name'], national_id=request.data['national'], mobile=request.data['mobile'],
#                           dob=request.data['dob'], pin=request.data['pin'],
#                           email=request.data['email'], reg_id=request.data['reg'],
#                           vehicle_type=request.data['type'], make=request.data['make'],
#                           vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])
#
#         if car_owner_add:
#
#             response = {'name': car_owner_add.fullname, 'national': car_owner_add.national_id, 'mobile': car_owner_add.mobile, 'dob': car_owner_add.dob,
#                         'pin': car_owner_add.pin, 'email': car_owner_add.email, 'reg_no': car_owner_add.reg_id, 'type': car_owner_add.vehicle_type,
#                         'make': car_owner_add.make, 'model': car_owner_add.vehicle_model, 'year': car_owner_add.year_of_manufacture,
#                         'block_no': '', 'parent_hash': parent_hash, 'date_time':date.datetime.now()}
#
#             blockHash = hash_block(response)
#             block = {'hash': blockHash, 'contents': response}
#             owner.append(block)
#
#             car_owner_add.save()
#
#             # response2 = {'name': car_add.fullname, 'national': car_add.national_id, 'mobile': car_add.mobile, 'dob': car_add.dob,
#             #             'pin': car_add.pin, 'email': car_add.email, 'reg_no': car_add.reg_no, 'type': car_add.vehicle_type,
#             #             'make': car_add.make, 'model': car_add.vehicle_model, 'last_block': m.hexdigest(), 'nonce': 0}
#             # #return Response(response2)
#
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(owner)

# Add Vehicle Owner
def registrationCarOwner(request):

    owner = dict()

    # Create the blockchain and add the genesis block
    blockchain = registerCar(request)

    # previous_block = blockchain.text
    # chain = json.dumps(previous_block)
    # chain2 = json.loads(chain)
    # print(chain2[0])
    parent_hash = blockchain['hash']
    block_no = blockchain['contents']['block_no'] + 1
    print('Parent Hash$$$$$', blockchain)

    # block_num = json.loads(block_number)
    # block_num = json.loads(block_number)
    # block_no = block_num('contents', 'block_no')

    # How many blocks should we add to the chain after the genesis block
    num_of_blocks_to_add = 100
    for i in range(0, num_of_blocks_to_add):

        car_owner_add = Owner(fullname=request.data['name'], national_id=request.data['national'], mobile=request.data['mobile'],
                          dob=request.data['dob'], pin=request.data['pin'],
                          email=request.data['email'], reg_id=request.data['reg'],
                          vehicle_type=request.data['type'], make=request.data['make'],
                          vehicle_model=request.data['model'], year_of_manufacture=request.data['year'])

        if car_owner_add:

            response = {'name': car_owner_add.fullname, 'national': car_owner_add.national_id, 'mobile': car_owner_add.mobile, 'dob': car_owner_add.dob,
                        'pin': car_owner_add.pin, 'email': car_owner_add.email, 'reg_no': car_owner_add.reg_id, 'type': car_owner_add.vehicle_type,
                        'make': car_owner_add.make, 'model': car_owner_add.vehicle_model, 'year': car_owner_add.year_of_manufacture,
                        'block_no': block_no, 'parent_hash': parent_hash, 'date_time':date.datetime.now()}

            blockHash = hash_block(response)
            block = {'hash': blockHash, 'contents': response}
            owner.update(block)

            car_owner_add.save()

            # response2 = {'name': car_add.fullname, 'national': car_add.national_id, 'mobile': car_add.mobile, 'dob': car_add.dob,
            #             'pin': car_add.pin, 'email': car_add.email, 'reg_no': car_add.reg_no, 'type': car_add.vehicle_type,
            #             'make': car_add.make, 'model': car_add.vehicle_model, 'last_block': m.hexdigest(), 'nonce': 0}
            # #return Response(response2)

        else:
            print('Unable to save data')

        return owner

# Add Vehicle Owner
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carRegistrationOwner(request):

    owner = registrationCarOwner(request)

    if owner:
        return Response(owner)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



# Transfer Vehicle
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carTransfer(request):

    transfer = []

    # Create the blockchain and add the previous car registration block
    blockchain = [carRegistrationOwner()]
    previous_block = blockchain[0]
    parent_hash = previous_block['hash']
    block_number = previous_block['contents']['block_no'] + 1

    car_transfer = Details(fullname=request.data['name'], national_id=request.data['national'], mobile=request.data['mobile'],
                      dob=request.data['dob'], pin=request.data['pin'],
                      email=request.data['email'], reg_id=request.data['reg'],
                      vehicle_type=request.data['type'], make=request.data['make'],
                      vehicle_model=request.data['model'], year_of_manufacture=request.data['year'], previous_owner_name=request.data['p_name'],
                      previous_owner_mobile=request.data['p_mobile'], previous_owner_email=request.data['p_email'],
                      vehicle_status=0)

    if car_transfer:

        response = {'name': car_transfer.fullname, 'national': car_transfer.national_id, 'mobile': car_transfer.mobile, 'dob': car_transfer.dob,
                    'pin': car_transfer.pin, 'email': car_transfer.email, 'reg_no': car_transfer.reg_id, 'type': car_transfer.vehicle_type,
                    'make': car_transfer.make, 'model': car_transfer.vehicle_model, 'year': car_transfer.year_of_manufacture,
                    'previous_owner_name': car_transfer.previous_owner_name, 'previous_owner_mobile': car_transfer.previous_owner_email,
                    'previous_owner_email': car_transfer.previous_owner_email, 'vehicle_status': car_transfer.vehicle_status,
                    'block_no': block_number, 'parent_hash': parent_hash, 'date_time': date.datetime.now()}

        blockHash = hash_block(response)
        block = {'hash': blockHash, 'contents': response}
        car_transfer.save()
        transfer.append(block)

        # response2 = {'name': car_transfer.fullname, 'national': car_transfer.national_id, 'mobile': car_transfer.mobile, 'dob': car_transfer.dob,
        #             'pin': car_transfer.pin, 'email': car_transfer.email, 'reg_no': car_transfer.reg_id, 'type': car_transfer.vehicle_type,
        #             'make': car_transfer.make, 'model': car_transfer.vehicle_model, 'previous_owner_name': car_transfer.previous_owner_name,
        #             'previous_owner_mobile': car_transfer.previous_owner_mobile, 'previous_owner_email': car_transfer.previous_owner_email,
        #             'vehicle_status': car_transfer.vehicle_status, 'last_block': n.hexdigest(), 'nonce': 0}
        return Response(transfer)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Confirm Vehicle Transfer
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carTransferConfirmation(request):
    car_transfer_edit = Owner.objects.get(transfer_id=request.data['transfer'])

    confirm = []

    # Create the blockchain and add the previous car registration block
    blockchain = [carRegistrationOwner()]
    previous_block = blockchain[0]
    parent_hash = previous_block['hash']
    block_number = previous_block['contents']['block_no'] + 1

    transfer_confirm = Details(transfer_id=car_transfer_edit.transfer_id, fullname=request.data['name'], national_id=request.data['national'],
                              mobile=request.data['mobile'],dob=request.data['dob'], pin=request.data['pin'],
                              email=request.data['email'], reg_id=request.data['reg'],
                              vehicle_type=request.data['type'], make=request.data['make'],
                              vehicle_model=request.data['model'], year_of_manufacture=request.data['year'], previous_owner_name=request.data['p_name'],
                              previous_owner_mobile=request.data['p_mobile'], previous_owner_email=request.data['p_email'])

    if car_transfer_edit:
        car_transfer_edit.vehicle_status = 1
    #car_transfer_edit.save()

    if transfer_confirm and car_transfer_edit:

        response = {'transfer_id': transfer_confirm.transfer_id,  'name': transfer_confirm.fullname, 'national': transfer_confirm.national_id, 'mobile': transfer_confirm.mobile, 'dob': transfer_confirm.dob,
                    'pin': transfer_confirm.pin, 'email': transfer_confirm.email, 'reg_no': transfer_confirm.reg_id, 'type': transfer_confirm.vehicle_type,
                    'make': transfer_confirm.make, 'model': transfer_confirm.vehicle_model, 'year': transfer_confirm.year_of_manufacture,
                    'previous_owner_name': transfer_confirm.previous_owner_name, 'previous_owner_mobile': transfer_confirm.previous_owner_email,
                    'previous_owner_email': transfer_confirm.previous_owner_email, 'vehicle_status': transfer_confirm.vehicle_status,
                    'block_no': block_number, 'parent_hash': parent_hash, 'date_time': date.datetime.now()}

        blockHash = hash_block(response)
        block = {'hash': blockHash, 'contents': response}
        transfer_confirm.save()
        car_transfer_edit.save()
        confirm.append(block)

        # response2 = {'name': transfer_confirm.fullname, 'national': transfer_confirm.national_id, 'mobile': transfer_confirm.mobile, 'dob': transfer_confirm.dob,
        #             'pin': transfer_confirm.pin, 'email': transfer_confirm.email, 'reg_no': transfer_confirm.reg_id, 'type': transfer_confirm.vehicle_type,
        #             'make': transfer_confirm.make, 'model': transfer_confirm.vehicle_model, 'previous_owner_name': transfer_confirm.previous_owner_name,
        #             'previous_owner_mobile': transfer_confirm.previous_owner_mobile, 'previous_owner_email': transfer_confirm.previous_owner_email,
        #             'last_block': m.hexdigest(), 'nonce': 0}

        return Response(confirm)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, template_name='car_reg/index.html')

# Add View
def addCarRegistrationView(request):
    return render(request, 'car_reg/vehicle_registration_details.html')

