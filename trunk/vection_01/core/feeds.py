from django.contrib.syndication.feeds import Feed
from models import *

class AllProjects(Feed):
    title = "Vection Projects"
    link = "/all_projects/"
    description = "RSS Feeds for all projects"

    def items(self):
        return Project.objects.order_by('name')
	
class AllIssues(Feed):
	title = "Issues"
	link = "/issues/"
	description = "RSS feed for all issues"
	
	def items(self):
		return Issue.objects.all().order_by('-last_updated')[:25]
