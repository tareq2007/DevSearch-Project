from .models import Project, Review, Tag
from django.forms import ModelForm
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','p_image', 'description', 'demo_link', 'source_link', 'tags']

        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'value']
        
        labels = {
            'value': 'Place a vote',
            'body': 'Add a comment',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})