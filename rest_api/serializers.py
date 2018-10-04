from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from .models import *


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ("username", "email", "password")

class ToDoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ToDo
		fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = Employee
		fields = "__all__"

class OrganisationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Organisation
		fields = "__all__"