from django_filters import FilterSet, AllValuesMultipleFilter, ModelMultipleChoiceFilter, CharFilter, NumberFilter, MultipleChoiceFilter
from django import forms

from .models import Profile, Technology

class ProfileFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')
    location = CharFilter(lookup_expr='icontains')
    level = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    technologies_used = ModelMultipleChoiceFilter(
        queryset=Technology.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple
    )
    who_wants_to_be_hired_title = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)

    years_of_experience = NumberFilter()
    years_of_experience__gt = NumberFilter(field_name='years_of_experience', lookup_expr='gt')
    years_of_experience__lt = NumberFilter(field_name='years_of_experience', lookup_expr='lt')

    city = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    country = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    willing_to_relocate = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)

    CAPACITY_CHOICES = [
        ("Part-time Contractor", "Part-time Contractor"),
        ("Full-time Contractor", "Full-time Contractor"),
        ("Part-time Employee", "Part-time Employee"),
        ("Full-time Employee", "Full-time Employee"),
    ]
    capacity = MultipleChoiceFilter(choices=CAPACITY_CHOICES, widget=forms.CheckboxSelectMultiple, lookup_expr="icontains")

    class Meta:
        model = Profile
        fields = [
          "title",
          "description",
          "level",
          "is_remote",
          "willing_to_relocate",
          "years_of_experience",
          "technologies_used",
          "who_wants_to_be_hired_title",
          "location",
          "city",
          "state",
          "country",
          "capacity"
        ]