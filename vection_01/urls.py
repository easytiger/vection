from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

from core.feeds import *

from core.views import *

feeds = {
	'all_projects': AllProjects,
	'all_issues': AllIssues,
}

urlpatterns = patterns('',

     # rss feed url prefix
     (r'^vection/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
     
    
     # django admin panel
     (r'^vection/admin/', include('django.contrib.admin.urls')),
     
     # login view
     (r'^vection/login/$', login),
     (r'^vection/logout/$', logout_user),
          
     # user home page
     (r'^vection/home/$', home),
     
     # project urls
     (r'^vection/projects/$', projects),
     (r'^vection/projects/new/$', new_project),
     (r'^vection/projects/edit/(?P<project_name>\S+)/$', edit_project),
     (r'^vection/projects/(?P<project_name>\S+)/$', project_detail),
     
     # sub component urls
     (r'^vection/new_sub/(?P<project_name>\S+)/$', new_component),
     (r'^vection/edit_comp/(?P<project_name>\S+)/(?P<comp_name>\S+)/$', edit_component),
     
     # version url
     (r'^vection/new_ver/(?P<project_name>\S+)/$', new_version),
     
     # issue urls
     
     # view specific issue
     (r'^vection/issues/(?P<issue_id>\d+)/$', view_issue),
     #view issues for project:
     (r'^vection/issues/(?P<project_name>\S+)/$', project_issues),
     (r'^vection/closed-issues/(?P<project_name>\S+)/$', closed_project_issues),
     #view issues for subcomponent:
     (r'^vection/comp-issues/(?P<comp_id>\d+)/$', component_issues),
     # create an issue
     (r'^vection/new-issue/$', new_issue_np),
     (r'^vection/new-issue/(?P<project_name>\S+)/$', new_issue),
     
     
     #documentation
     (r'^vection/doc/', doc),
     
     
     
)
