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
	#user who initially created issue
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
