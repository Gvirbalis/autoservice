from .models import UzsakymasReview
from django import forms

class UzsakymasReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer',)
        widgets = {'uzsakymas': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}