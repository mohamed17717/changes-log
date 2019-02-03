from django import forms
from .models import Comment, Project, Version, Change

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )

class ReplayCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'replay',
        )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'project_name',
            'breif',
            'coders',
            'technologies',
            'under_work',
            'can_try',
            'finished',
        )

class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = (
            'version_number',
            'critical_version',
            'combitable_with_old_dependencies',
            'github_url',
        )

class ChangeForm(forms.ModelForm):
    class Meta:
        model = Change
        fields = (
            'name', 
            'explain',
        )
