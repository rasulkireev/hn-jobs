from django.db.models import Q, Count
from django_filters import FilterSet, AllValuesMultipleFilter, ModelMultipleChoiceFilter, CharFilter, NumberFilter, MultipleChoiceFilter
from django import forms

from .models import Post, Technology

class FrequencyOrderedAllValuesMultipleFilter(AllValuesMultipleFilter):
    def field_choices(self, *args, **kwargs):
        queryset = self.model._default_manager.distinct().order_by(self.field_name).values_list(self.field_name, flat=True)
        lst = list(queryset)
        # Count the frequency of each value and sort the choices by frequency in descending order
        choices = sorted(
            self.extra['choices_form_class'](list(enumerate(lst))),
            key=lambda x: -lst.count(x[0])
        )
        return choices

class PostFilter(FilterSet):
    # title = CharFilter(lookup_expr='icontains')
    description = CharFilter(lookup_expr='icontains')

    # # location = CharFilter(lookup_expr='icontains')
    # city = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    # state = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    # country = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)

    # level = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    # technologies_used = ModelMultipleChoiceFilter(
    #     queryset=Technology.objects.annotate(job_count=Count('job')).filter(job_count__gt=10).order_by('-job_count'),
    #     widget=forms.CheckboxSelectMultiple(),
    #     conjoined=True
    # )
    # who_is_hiring_title = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)

    # years_of_experience = NumberFilter()
    # years_of_experience__gt = NumberFilter(field_name='years_of_experience', lookup_expr='gt')
    # years_of_experience__lt = NumberFilter(field_name='years_of_experience', lookup_expr='lt')

    # city = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    # country = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)
    # willing_to_relocate = AllValuesMultipleFilter(widget=forms.CheckboxSelectMultiple)

    # CAPACITY_CHOICES = [
    #     ("Part-time Contractor", "Part-time Contractor"),
    #     ("Full-time Contractor", "Full-time Contractor"),
    #     ("Part-time Employee", "Part-time Employee"),
    #     ("Full-time Employee", "Full-time Employee"),
    # ]
    # capacity = MultipleChoiceFilter(choices=CAPACITY_CHOICES, widget=forms.CheckboxSelectMultiple, lookup_expr="icontains")

    class Meta:
        model = Post
        fields = [
          # "title",
          "description",
          # "level",
          # "is_remote",
          # "willing_to_relocate",
          # "years_of_experience",
          # "technologies_used",
          # "who_is_hiring_title",
          # "location",
          # "city",
          # "state",
          # "country",
          # "capacity"
        ]