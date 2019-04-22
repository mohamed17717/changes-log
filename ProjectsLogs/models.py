from django.db import models
from django.utils.text import slugify
import datetime
# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    replay  = models.TextField(blank=True, null=True)
    seen    = models.BooleanField(default=False)

    comment_created = models.DateTimeField(editable=False, default=datetime.datetime.now)
    replay_created  = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.replay:
            if not self.seen:
                self.replay_created = datetime.datetime.now()
            self.seen = True

        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.content[:15]+'...'

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Change(models.Model):
    ## change main data
    name    = models.CharField(max_length=70)
    explain = models.TextField()
    kind = models.CharField(editable=False, max_length=10, blank=True, null=True)


    ## data accroding to user
    accepted = models.BooleanField(default=True)
    user_notes  = models.ManyToManyField(Comment, blank=True)
    
    def __str__(self):
        return self.explain

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Change'
        verbose_name_plural = 'Changes'

class Added(Change):
    def save(self, *args, **kwargs):
        self.kind = 'added'
        return super(Added, self).save(*args, **kwargs)

class Removed(Change):
    def save(self, *args, **kwargs):
        self.kind = 'removed'
        return super(Removed, self).save(*args, **kwargs)

class Changed(Change):
    def save(self, *args, **kwargs):
        self.kind = 'changed'
        return super(Changed, self).save(*args, **kwargs)

class Deprecated(Change):
    def save(self, *args, **kwargs):
        self.kind = 'deprecated'
        return super(Deprecated, self).save(*args, **kwargs)

class Fixed(Change):
    def save(self, *args, **kwargs):
        self.kind = 'fixed'
        return super(Fixed, self).save(*args, **kwargs)

class Security(Change):
    def save(self, *args, **kwargs):
        self.kind = 'security'
        return super(Security, self).save(*args, **kwargs)

class Version(models.Model):
    ## version data
    version_number = models.CharField(max_length=15)
    critical_version = models.BooleanField()
    combitable_with_old_dependencies = models.BooleanField()

    created = models.DateTimeField(editable=False, default=datetime.datetime.now)

    ## version cide on github
    github_url      = models.URLField(null=True, blank=True, max_length=200)

    ## changes logs
    #project_changes = models.ManyToManyField(Change)
    added = models.ManyToManyField(Added, blank=True)
    removed = models.ManyToManyField(Removed, blank=True)
    changed = models.ManyToManyField(Changed, blank=True)
    deprecated = models.ManyToManyField(Deprecated, blank=True)
    fixed = models.ManyToManyField(Fixed, blank=True)
    security = models.ManyToManyField(Security, blank=True)

    def __str__(self):
        return self.version_number

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'

class WebTechnology(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Coder(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    project_name = models.CharField(max_length=70)
    slug         = models.SlugField(blank=True)
    project_versions = models.ManyToManyField(Version, blank=True)
    created      = models.DateTimeField(editable=False, default=datetime.datetime.now)

    ## data appear in profile table
    breif        = models.TextField(null=True, blank=True)
    coders       = models.ManyToManyField(Coder, blank=True)
    technologies = models.ManyToManyField(WebTechnology, blank=True)
    ## i work on it or update it
    under_work   = models.BooleanField(default=True)
    ## i work on it but you can try this beta version while am working
    can_try      = models.BooleanField(default=False)
    ## this project finished
    finished     = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify('%s' % self.project_name)
        return super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'