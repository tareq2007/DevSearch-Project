from django.db import models
from users.models import Profile
from uuid import uuid4

class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    p_image = models.ImageField(blank=True, null=True, default="df.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0,null=True, blank=True)
    vote_ratio = models.IntegerField(default=0,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

    def __str__(self):
        return self.title
    
    @property
    def getVoteCount(self):
         reviews = self.review_set.all()
         upVotes = reviews.filter(value='up').count()
         totalVotes = reviews.count()
         ratio = (upVotes / totalVotes) * 100
         self.vote_total = totalVotes
         self.vote_ratio = ratio
         self.save()

    class Meta:
        ordering = ['-vote_ratio', '-vote_total']
    @property
    def reviewers(self):
        setquery = self.review_set.all().values_list('owner__id', flat=True)
        return setquery

class Review(models.Model):
    VOTE_TYPE = (
        ('up', '👍'),
        ('down', '👎')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

    def __str__(self):
        return self.value
    
    class Meta:
        unique_together = [['owner', 'project']]
    
class Tag(models.Model):
        name = models.CharField(max_length=200)
        created = models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)

        def __str__(self):
            return self.name