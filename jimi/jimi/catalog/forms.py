from django import forms
from django.utils.translation import ugettext as _


class ProductAddToCartForm(forms.Form):
    """Add a product to a cart"""
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size': '2',
                                                                'value': '1',
                                                                'class': 'quantity',
                                                                'maxlength': '5'}),
                                  error_messages={'invalid': _('Please enter a valid quantity.')},
                                  min_value=1)
    product = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, request=None, *args, **kwargs):
        """Override to set request"""
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Cookies must be enabled for shopping cart."))
        return self.cleaned_data
