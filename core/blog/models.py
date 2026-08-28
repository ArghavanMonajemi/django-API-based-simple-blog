from django.db import models


class Post(models.Model):
    author = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey("blog.Category", on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="posts/%Y/%m/%d", blank=True, null=True)
    status = models.BooleanField(default=False)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def snippet(self):
        return self.content[:50]


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
