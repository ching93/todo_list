from django.db import models
from django.contrib.auth.models import User

class Organisation(models.Model):
	name = models.TextField(max_length=50,null=False, unique=True)

	def __str__(self):
		return self.name


class Employee(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='employee')
	org = models.ForeignKey(Organisation, related_name='employees',on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'org')

	def __str__(self):
		return self.user.username


class ToDo(models.Model):
	title = models.TextField(max_length=100)
	text = models.TextField(max_length=2048, blank=True)
	org = models.ForeignKey(Organisation, related_name='todoList',on_delete=models.CASCADE)
	createdBy = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='todoList')

	def __str__(self):
		return self.title