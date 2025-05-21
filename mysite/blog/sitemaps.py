from django.contrib.sitemaps import Sitemap
from django.db.models import Model
from blog.models import Post, Comment

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated

class CommentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Comment.objects.all()
    
    def lastmod(self, obj):
        return obj.created
    
    def location(self, item: Model) -> str:
        return f"{item.id}/comments/"
