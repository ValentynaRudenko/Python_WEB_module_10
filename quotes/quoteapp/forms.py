from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, \
                            DateField, Textarea

from .models import Tag, Quote, Author


class TagForm(ModelForm):

    name = CharField(min_length=3,
                     max_length=25,
                     required=True,
                     widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(
                      max_length=500,
                      required=True,
                      widget=Textarea())
    author = ModelChoiceField(queryset=Author.objects.all(), required=True)

    class Meta:
        model = Quote
        fields = ['author', 'quote']
        exclude = ['tags']


class AuthorForm(ModelForm):
    fullname = CharField(
                      max_length=70,
                      required=True,
                      widget=TextInput())
    born_date = DateField(required=True,
                          widget=TextInput(attrs={'type': 'date'}))
    born_location = CharField(max_length=100,
                              required=True, widget=TextInput())
    description = CharField(max_length=300,
                            required=True, widget=Textarea())

    class Meta:
        model = Author
        fields = ['fullname',
                  'born_date',
                  'born_location',
                  'description']
