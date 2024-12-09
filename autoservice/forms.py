from django.contrib.auth.models import User

from .models import UzsakymasReview, Profilis
from django import forms

class UzsakymasReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer',)
        widgets = {'uzsakymas': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this is the magic right here:
        self.fields['email'].label = "El.paštas"
        self.fields['first_name'].label = "Vardas"
        self.fields['last_name'].label = "Pavardė"
        self.fields['username'].help_text = "Pakeitus username, nepamirškite pasikeist ir jungiantis Jūsų username!"
        self.fields['email'].help_text = "Įsitikinkite, kad suvedėte galiojantį el.pašta, kitu atvėju negalėsite susigražinti slaptažodžio!"


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


