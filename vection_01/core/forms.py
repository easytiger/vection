from django import newforms as forms
from models import *
from django.newforms import widgets

class IssueUpdateForm(forms.Form):
	priority = forms.ModelChoiceField(queryset=Priority.objects.all(),empty_label=None)
	status = forms.ModelChoiceField(queryset=Status.objects.all(),empty_label=None)
	resolution = forms.ModelChoiceField(queryset=Resolution.objects.all(), required=False)
	comment = forms.CharField(widget=forms.Textarea(), required=False)
	assignee = forms.ModelChoiceField(queryset=UserProfile.objects.all(), required=False)
	
	def save(self, issue_id, user):
		issue = Issue.objects.get(id=issue_id)
		
		s = ''
		self.is_valid()
		clean = self.clean_data
		
		if clean['status'].id != issue.status_id:
			#status has changed
			s = s +"  **Status**: " + str(issue.status) + " > " +  str(clean['status'])
			# set status 
			issue.status_id = clean['status'].id
		
		if clean['priority'].id != issue.priority_id:
			s = s + "  **Priority**: " + str(issue.priority) + "> " +  str(clean['priority'] )
			issue.priority_id = clean['priority'].id
			
		if clean['resolution'] != None:
			if clean['resolution'].id != issue.resolution_id:
				# resolution has changed. update status to closed.
				issue.status_id = 5
				s = s + "  **Resolution**: " + str(issue.resolution) +  " > " +  str(clean['resolution'])
				issue.resolution_id = clean['resolution'].id
				
		if clean['assignee'] != None:
			if clean['assignee'].id != issue.responsible_user_id:
				s = s + "  **New assignee:** " + str(clean['assignee'])
				
		#now createUpdate Object
		iu = IssueUpdate()
		iu.fields = s
		iu.comment = clean['comment']
		iu.user_id = user.userprofile_set.get().id

		# commit to DB
		
		issue.responsible_user_id = clean['assignee'].id 
		iu.issue_id = issue.id
		iu.save()
		issue.save()

		return str(iu.id)
