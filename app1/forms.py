from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['mytype', 'amount', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'datepicker'  # You can add custom attributes like CSS classes for datepicker
        self.fields['end_date'].widget.attrs['class'] = 'datepicker'
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        user = cleaned_data.get('user')

        if start_date and end_date and user:
            # Check for overlapping offers for the same user
            overlapping_offers = Offer.objects.filter(
                user=user,
                start_date__lte=end_date,
                end_date__gte=start_date,
            ).exclude(pk=self.instance.pk)  # Exclude the current offer when editing

            if overlapping_offers.exists():
                raise forms.ValidationError("Overlapping offers for the same user are not allowed.")