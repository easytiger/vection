from django.http import *
import csv
from django.shortcuts import *
from django.contrib.auth.decorators import *
from django.contrib import *
from django.template import *
from django.contrib.auth.views import login, logout
from django.utils.html import escape

from django import newforms as forms
from django.newforms import widgets

#vection components
from forms import *
from models import *

def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/vection/login")
	
def doc(request):
	return render_to_response('doc.html', 
		context_instance=RequestContext(request))
		
def new_issue_np(request):

	projects = Project.objects.all()
	
	return render_to_response('base/issues/new_issue_np.html',
		{'projects': projects},
		context_instance=RequestContext(request))
		
def home(request):
	# get all the user's profile
	up = request.user.get_profile()
	issues = Issue.objects.filter(responsible_user=up).exclude(status=5).order_by('priority')
	
	c = Context({
		'issues': issues,
	})
		
	return render_to_response('base/vection_home.html', c,
		context_instance=RequestContext(request))
	
def projects(request):
	projects_list = Project.objects.all()
	return render_to_response('base/vection_projects_all.html', 
		{'projects_list': projects_list}, 
		context_instance=RequestContext(request))
	
def project_detail(request, project_name):
	pro = Project.objects.get(name=project_name)
	return render_to_response('base/vection_project_detail.html', 
		{'pro': pro}, context_instance=RequestContext(request))

def new_project(request):
	ProjectForm = forms.models.form_for_model(Project)
	
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			project = form.save()
			return HttpResponseRedirect("/vection/projects/")
	else:
		form = ProjectForm()
		
	return render_to_response('base/new_project.html', {'form': form},
		context_instance=RequestContext(request))
	
		
def edit_project(request, project_name):
	pro = Project.objects.get(name=project_name)
	ProjectForm = forms.models.form_for_instance(pro)
	form = ProjectForm();
	
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/vection/projects/" + project_name)
			
	return render_to_response('base/edit_project.html', {'form': form},
		context_instance=RequestContext(request))

def new_component(request, project_name):
	PCForm = forms.models.form_for_model(ProjectComponent)
	project = Project.objects.get(name=project_name)
	
	if request.method == 'POST':
		form = PCForm(request.POST)
		if form.is_valid():
			pc = form.save()
			return HttpResponseRedirect("/vection/projects/" + project_name)
	else:
		form = PCForm()
		form.fields['project_for_component'].initial=project.id
		
	return render_to_response('base/new_component.html', {'form': form},
		context_instance=RequestContext(request))
		
def edit_component(request, project_name, comp_name):
	comp = ProjectComponent.objects.get(name=comp_name)
	PCForm = forms.models.form_for_instance(comp)
	form = PCForm()
	
	if request.method == 'POST': 
		form = PCForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/vection/projects/" + project_name)
			
	return render_to_response('base/new_component.html', {'form': form},
		context_instance=RequestContext(request))
		
	
	
def new_version(request, project_name):
	VerForm = forms.models.form_for_model(ProjectVersion)
	project = Project.objects.get(name=project_name)
	
	if request.method == 'POST':
		form = VerForm(request.POST)
		if form.is_valid():
			vf = form.save()
			return HttpResponseRedirect("/vection/projects/" + project_name)
	else:
		form = VerForm()
		form.fields['project_for_version'].initial=project.id
	
	return render_to_response('base/new_version.html', {'form': form},
		context_instance=RequestContext(request))

	
def new_issue(request, project_name=None):
	IssueForm = forms.models.form_for_model(Issue)
	project = get_object_or_404(Project, name=project_name)
	
	# the following limit the FK selection by a query so 
	# there are no incorrect components etc
	
	q = ProjectComponent.objects.filter(project_for_component=project.id)
	IssueForm.base_fields['sub_component'] = forms.ModelChoiceField(queryset=q)
	
	q = ProjectVersion.objects.filter(project_for_version=project.id)
	IssueForm.base_fields['version'] = forms.ModelChoiceField(queryset=q)
	
	if request.method == 'POST':
		form = IssueForm(request.POST)
		form.clean
		if form.is_valid():
			issue = form.save(commit=False)
			# set the project first
			issue.project_id = project.id
			# set the status to open
			issue.status_id = 1
			# commit it to DB
			issue.save()
			return HttpResponseRedirect('/vection/issues/' + str(issue.id))
	else:
		form = IssueForm()

	return render_to_response('base/issues/new_issue.html', 
		{'form': form, 'project': project},context_instance=RequestContext(request))
	
def view_issue(request, issue_id):
	issue = get_object_or_404(Issue, id=issue_id)
	form = IssueUpdateForm()
	
	#set form defaults for this issue:
	form.fields['priority'].initial=issue.priority_id
	form.fields['status'].initial=issue.status_id
	
	if issue.responsible_user_id != None:
		form.fields['assignee'].initial=issue.responsible_user_id
	if issue.resolution_id != None:
		form.fields['resolution'].initial=issue.resolution_id

	if request.method == 'POST':
		form = IssueUpdateForm(request.POST)
		form.save(issue_id, request.user)
		return HttpResponseRedirect("/vection/issues/" + str(issue_id))
	
	c = Context({
		'issue': issue,
		'form' : form,
	})
	
	return render_to_response('base/issues/view_issue.html', 
		c, context_instance=RequestContext(request))

def project_issues(request, project_name):
	project = Project.objects.get(name=project_name)
	
	if request.GET:
		if request.GET['sortby'] == 'updated':
			open_issues = project.issue_set.exclude(status=5).order_by('-last_updated')
		elif request.GET['sortby'] == 'created':
			open_issues = project.issue_set.exclude(status=5).order_by('-created')
		elif request.GET['sortby'] == 'priorityasc':
			open_issues = project.issue_set.exclude(status=5).order_by('priority')
		elif request.GET['sortby'] == 'prioritydes':
			open_issues = project.issue_set.exclude(status=5).order_by('-priority')
		elif request.GET['sortby'] == 'comp':
			open_issues = project.issue_set.exclude(status=5).order_by('sub_component')
		elif request.GET['sortby'] == 'status':
			open_issues = project.issue_set.exclude(status=5).order_by('status')
		else:
			#default sort
			open_issues = project.issue_set.exclude(status=5).order_by('priority')
	else:
		#open issues for this project
		open_issues = project.issue_set.exclude(status=5).order_by('priority')
		count = Issue.objects.filter(project=project.id).count()
		
	
	c = Context({
		'project': project,
		'open_issues': open_issues,
		'count': project,
	})
	
	return render_to_response('base/issues/project_issues.html', 
		c, context_instance=RequestContext(request))
		
def closed_project_issues(request, project_name):
	project = Project.objects.get(name=project_name)
	
	if request.GET:
		if request.GET['sortby'] == 'updated':
			closed_issues = project.issue_set.filter(status=5).order_by('-last_updated')
		elif request.GET['sortby'] == 'created':
			closed_issues = project.issue_set.filter(status=5).order_by('-created')
		elif request.GET['sortby'] == 'priorityasc':
			closed_issues = project.issue_set.filter(status=5).order_by('priority')
		elif request.GET['sortby'] == 'prioritydes':
			closed_issues = project.issue_set.filter(status=5).order_by('-priority')
		elif request.GET['sortby'] == 'comp':
			closed_issues = project.issue_set.filter(status=5).order_by('sub_component')
		elif request.GET['sortby'] == 'status':
			closed_issues = project.issue_set.filter(status=5).order_by('status')
		else:
			#default sort
			closed_issues = project.issue_set.filter(status=5).order_by('priority')
	else:
		#open issues for this project
		closed_issues = project.issue_set.filter(status=5).order_by('priority')
		count = Issue.objects.filter(project=project.id).count()
		
	
	c = Context({
		'project': project,
		'closed_issues': closed_issues,
		'count': project,
	})
	
	return render_to_response('base/issues/closed_project_issues.html', 
		c, context_instance=RequestContext(request))
		
		
		
def component_issues(request, comp_id):
	comp = ProjectComponent.objects.get(id=comp_id).issue_set.all()
	
	component = ProjectComponent.objects.get(id=comp_id)
	if request.GET:
		if request.GET['sortby'] == 'updated':
			issues = comp.order_by('-last_updated')
		elif request.GET['sortby'] == 'created':
			issues = comp.order_by('-created')
		elif request.GET['sortby'] == 'priorityasc':
			issues = comp.order_by('priority')
		elif request.GET['sortby'] == 'prioritydes':
			issues = comp.order_by('-priority')
		elif request.GET['sortby'] == 'comp':
			issues = comp.order_by('sub_component')
		elif request.GET['sortby'] == 'status':
			issues = comp.order_by('status')
		else:
			#default sort
			issues = comp.order_by('priority')
	else:
		#open issues for this project
		issues = comp.order_by('priority')
		
		
	
	c = Context({
		'comp': comp,
		'component': component,
		'issues': issues,
	})
	
	return render_to_response('base/issues/component-issues.html', 
		c, context_instance=RequestContext(request))

    
# enforce logins
projects = login_required(projects)
project_detail = login_required(project_detail)
home = login_required(home)
new_project = login_required(new_project)
edit_project = login_required(edit_project)
view_issue = login_required(view_issue)
project_issues = login_required(project_issues)
component_issues = login_required(component_issues)
closed_project_issues = login_required(closed_project_issues)




