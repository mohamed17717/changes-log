from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    ## fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    user_projects = models.ManyToManyField("ProjectsLogs.Project", blank=True)
    p = models.CharField(max_length=100, blank=True, null= True)

    def save(self, *args, **kwargs):
        self.slug = slugify('%s' % self.user)
        return super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.user

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user= instance)

post_save.connect(create_profile, sender=User)