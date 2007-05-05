from django.db import models
from django.contrib.auth.models import User 

DOMAIN_PREFIX = "http://belfast.no-ip.org/"

class UserProfile(models.Model):
	"""
	An extension of the user model 
	
	"""
	url = models.URLField(blank = True)
	user = models.ForeignKey(User, unique=True)
	avatar_url = models.URLField( null=True, blank=True)
	tagline = models.CharField(maxlength=50)


	def __str__(self):
		return self.user.username
		
	def fullname(self):
		return self.user.first_name + " " + self.user.last_name 
	
	def open_issue_count(self):
		return Issue.objects.filter(responsible_user=self.user).exclude(status=5).count()
		
	class Admin:
		pass	
	
class IssueType(models.Model):
	type  = models.CharField(maxlength=20)
	description = models.CharField(maxlength=100)
	icon = models.CharField(maxlength=120,blank=True, null=True)
	position = models.PositiveIntegerField()
	
	def __str__(self):
		return self.type
		
	class Meta:
		ordering = ['position']

	class Admin:
		pass
	

class ProjectComponent(models.Model):
	name = models.CharField(maxlength=50)
	desc = models.CharField(maxlength=100)
	# default assignee
	default_engineer = models.ForeignKey(UserProfile)
	project_for_component = models.ForeignKey("Project")
	
	def __str__(self):
		return self.name
		
	class Admin:
		pass

class ProjectVersion(models.Model):
	name = models.CharField(maxlength=30)
	released = models.NullBooleanField()
	#desc = models.CharField(maxlength=40, blank=True, null=True)
	release_date = models.DateField(blank = True, null=True)
	unnasigned = models.BooleanField()
	project_for_version = models.ForeignKey("Project")
	
	def __str__(self):
		return self.name
		
	class Admin:
		pass	
	
class Project(models.Model):
	name = models.CharField(maxlength=30)
	tag = models.CharField(maxlength=5, unique=True)
	desc = models.TextField()
	project_lead = models.ForeignKey(UserProfile)
	
	def get_absolute_url(self):
		return DOMAIN_PREFIX + "vection/projects/" + self.name
		
	def __str__(self):      
		return self.name
	
	class Admin:
		pass
	
	class Meta:
		ordering = ['name']
	

		
class Priority(models.Model):
	name = models.CharField(maxlength=10)
	description = models.CharField(maxlength=60)
	icon = models.CharField(maxlength=250)
	position = models.PositiveIntegerField()
	colour = models.CharField(maxlength=10)
	def __str__(self):
		return self.name
		
	class Admin:
		pass
	
	class Meta:
		# 1 is high priority
		ordering = ['position']
		verbose_name_plural = "Priorities"

class Status(models.Model):
	status  = models.CharField(maxlength=20)
	description = models.CharField(maxlength=100)
	position = models.PositiveIntegerField()
	icon = models.CharField(maxlength=250, blank=True, null=True)
	
	def is_closed(self):
		if self.id == 5:
			return True
		else:
			return False
		
	def __str__(self):
		return self.status
	
	class Meta:
		verbose_name = "Status"
		verbose_name_plural = "Statuses"
		ordering = ['position']
		
	class Admin:
		pass

class Resolution(models.Model):
	type  = models.CharField(maxlength=20)
	description = models.CharField(maxlength=100)

	def __str__(self):
		return self.type
	
	class Meta:
		ordering = ['type']
		verbose_name = "Resolution"
		verbose_name_plural = "Resolutions"
		
	class Admin:
		pass
	
class IssueUpdate(models.Model):
	fields = models.TextField(blank=True, null=True, editable=False)
	comment = models.TextField()
	made = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(UserProfile)
	issue = models.ForeignKey("Issue", blank=True, null=True, editable=False)
	
	def __str__(self):
		return self.fields + self.comment
		
	class Admin:
		pass
	
class Issue(models.Model):
	
	title = models.CharField(maxlength=100)
	
	issue_type = models.ForeignKey(	IssueType)
	
	project = models.ForeignKey(Project, editable = False)
	
	sub_component = models.ForeignKey(ProjectComponent)
	
	priority = models.ForeignKey(Priority)
	
	status = models.ForeignKey(Status, blank=True, null=True, editable=False)
	
	resolution = models.ForeignKey(Resolution, blank=True, null=True, editable=False)
	
	description = models.TextField()
	
	version = models.ForeignKey(ProjectVersion, blank=True, null=True)
	
	environment = models.TextField(blank = True, null=True)
	
	#update = models.ForeignKey(IssueUpdate, blank=True, null=True, editable=False)

	#user who initially created issue
	# use a hidden field
	created_by = models.ForeignKey(UserProfile, related_name='creator')
	
	# engineer looking at issue
	responsible_user = models.ForeignKey(UserProfile, related_name='responsible')

	due_date = models.DateField(blank = True, null=True)
	
	# automatic dates
	created = models.DateTimeField(auto_now_add = True)
	last_updated = models.DateTimeField(auto_now = True)
	
	
	def __str__(self):
		return "[" + self.project.name +":"+ self.sub_component.name + "] " + self.title
		
	def tag(self):
		return   self.project.tag + '-' + str(self.id)
	
	def get_absolute_url(self): 
		return DOMAIN_PREFIX + "vection/issues/" + str(self.id)
	class Admin:
		pass
