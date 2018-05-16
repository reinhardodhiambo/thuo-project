"""car_reg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from users.views import allUsers, addUsers, editUsers, login, register, administrator, login_user
from vehicle_registration.views import index, addCarRegistrationView, carRegistration, carRegistrationOwner, \
    carTransfer, carTransferConfirmation, addCarDetails
from vehicle_transfer.views import carOwner, carOwnerView
from vehicle_transfer_confirmation.views import carConfirmation, carConfirmationView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/all_users$', allUsers, name='users'),
    url(r'^users/add_users$', addUsers, name='add_users'),
    url(r'^users/edit_users$', editUsers, name='edit_users'),
    url(r'^user/login$', login_user),
    url(r'^vehicle_reg/add_vehicle$', carRegistration, name='add_vehicle'),
    url(r'^vehicle_reg/add_vehicle_owner$', carRegistrationOwner, name='add_vehicle_owner'),
    url(r'^vehicle_reg/transfer_vehicle$', carTransfer, name='transfer_vehicle'),
    url(r'^vehicle_reg/confirm_vehicle_transfer$', carTransferConfirmation, name='confirm_vehicle_transfer'),

    url(r'^signin$', login, name='signin'),
    url(r'^admin$', administrator, name='admin'),
    url(r'^signup$', register, name='signup'),
    url(r'^home$', index, name='home'),
    url(r'^vehicle_registration_details$', addCarDetails, name='vehicle_registration_details'),
    url(r'^vehicle_registration$', addCarRegistrationView, name='vehicle_registration'),
    url(r'^vehicle_owner$', carOwner, name='vehicle_owner'),
    url(r'^vehicle_owner_details$', carOwnerView, name='vehicle_owner_details'),
    url(r'^vehicle_confirmation$', carConfirmation, name='vehicle_confirmation'),
    url(r'^vehicle_confirmation_details$', carConfirmationView, name='vehicle_confirmation_details'),
]
