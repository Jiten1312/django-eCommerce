from django import forms
from myapp.models import Order, Client, PasswordReset


# The form should have 3 fields: i) interested: Should display RadioSelect buttons (Yes/No). The value returned will
# before Yes and 0 for No. ii) quantity: Will accept an integer value of 1 or higher, indicating how many units of a
# product the user is interested in. Initial value is set to 1. iii) comments: An optional input using Textarea
# widget and label =‘AdditionalComments
class InterestForm(forms.Form):
    CHOICES = [(1, 'Yes'),
               (0, 'No')]

    interested = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput({'class': 'form-control'}))
    comments = forms.CharField(widget=forms.Textarea({'class': 'form-control'}), label="Additional Comments",
                               required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        # Set the widget for client field to RadioSelect.
        widgets = {
            'client': forms.RadioSelect(),
            'product': forms.Select({'class': 'form-control'}),
            'num_units': forms.NumberInput({'class': 'form-control', 'value': 1})
        }
        # Set the label for the num_units field to ‘Quantity’; Set the label for the client field to ‘Client Name’
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }

        initial = {
            'num_units':1
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'company',
                  'city', 'province', 'interested_in', 'image']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
            'interested_in': forms.CheckboxSelectMultiple,
        }


class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = PasswordReset
        fields = ['username']
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
