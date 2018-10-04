from django.shortcuts import render
from rest_framework import generics, status
from django.contrib.auth.decorators import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import *
from .serializers import *

'''def main(request):
	if request.user.is_authenticated and request.user.employee:
		employee = request.user.employee
	else:
		employee = None
	orgs = Organisation.objects.all()
	todo_list = employee.org.todoList.all()
	print(ToDoSerializer(todo_list, many=True).data)
	return render(request, 'rest_api/index.html',{'employee': EmployeeSerializer(employee).data, 
		'orgs': OrganisationSerializer(orgs, many=True).data,
		'todolist': ToDoSerializer(todo_list, many=True).data})'''

'''
{
	"org": 1,
	"email": "chingis@ch.bur",
	"password": "1211"
}
'''
def rest_login(request):
	email = request.POST['email']
	password = request.POST['password']
	org = request.POST['org']
	employee = Employee.objects.get(org=org,user__email=email)
	user = authenticate(username=employee.user.username, password=password)
	if user:
		login(request, user)
		return redirect("rest_api:main")
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

def rest_logout(request):
	logout(request)
	return redirect("rest_api:main")


@api_view(['PUT','GET'])
def employee_list(request):
	if request.method == 'GET':
		print(request.user)
		if request.user.is_authenticated:
			employee_list = Employee.objects.filter(user__email=request.user.email)
			return Response(EmployeeSerializer(employee_list, many=True).data)
		else:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
	if request.method == 'PUT':
		try:
			org_id = request.data.get('org')
			org = Organisation.objects.get(pk=org_id)
		except Exception as exc:
			print(str(exc))
			return Response(status=status.HTTP_404_NOT_FOUND)
		request.data['username'] = "{}_{}".format(request.data['email'],org.name)
		userSr = UserSerializer(data=request.data)
		if userSr.is_valid():
			user = userSr.save()
			empl = Employee.objects.create(org=org, user=user)
			return Response(EmployeeSerializer(empl).data, status=status.HTTP_201_CREATED)
		else:
			return Response(userSr.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def todo_list(request):
	print(request.data)
	try:
		employee = request.user.employee
		org = employee.org
	except Exception as exc:
		print(str(exc))
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		print('get')
		todoList = org.todoList.all()
		return Response(ToDoSerializer(todoList,many=True).data)
	elif request.method == 'PUT':
		data = {key: item[0] for (key,item) in request.data if type(item) == 'list'}
		data.update({'createdBy':employee.pk, 'org': org.pk})
		print(data)
		print(type(data['title']))
		todo = ToDoSerializer(data=data)
		if todo.is_valid():
			todo.save()
			return Response(todo.data, status=status.HTTP_201_CREATED)
		else:
			print(todo.errors)
			return Response(todo.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH','DELETE'])
def todo_detail(request,pk):
	try:
		todo = ToDo.objects.get(pk=pk)
	except Exception as exc:
		print(str(exc))
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		return Response(ToDoSerializer(todo).data)
	elif request.method == 'PATCH':
		serializer = ToDoSerializer(instance=todo,data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		todo.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class OrgList(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

class OrgDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer