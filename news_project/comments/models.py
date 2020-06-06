from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):

    body = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return f'Comment by {self.author.username} in post {self.post.title}, {self.date}'