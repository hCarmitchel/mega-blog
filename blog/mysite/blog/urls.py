from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView
from blog.models import Post
from django.contrib.syndication.views import Feed

class BlogFeed(Feed):
	title = "MySite"
	description = "Some ramblings of mine"
	link = "/blog/feed/"

	def items(self):
		return Post.objects.all().order_by("-created")
	def item_title(self, item):
		return item.title
	def item_description(self, item):
		return item.body
	def item_link(self, item):
		return u"/blog/%d" % item.id

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('blog.views',
	url(r'^$', ListView.as_view(
							queryset=Post.objects.all().order_by("-created"),
							template_name="blog.html")),
	url(r'^(?P<pk>\d+)$', DetailView.as_view(
							model=Post,
							template_name="post.html")),
	url(r'^archives/$', ListView.as_view(
							queryset=Post.objects.all().order_by("-created"),
							template_name="archives.html")),
	url(r'^tag/(?P<tag>\w+)$', 'tagpage'),
	url(r'^feed/$', BlogFeed()),
	url(r'^tags/$', ListView.as_view(
							queryset=Post.tags.all().order_by("taggit_taggeditem_items"),
							template_name="tags.html")),
	(r'^comments/', include('django.contrib.comments.urls')),
)