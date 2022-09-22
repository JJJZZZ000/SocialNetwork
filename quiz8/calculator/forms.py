from django import forms

class CalcForm(forms.Form):
    x = forms.IntegerField()
    y = forms.IntegerField()
    # def clean(self):
    #     cleaned_data = super().clean()
    #     x = cleaned_data.get('x')
    #     y = cleaned_data.get('y')
    #     if y == "0":
    #         raise forms.ValidationError("Y should not be zero")
    #     return cleaned data
    def clean_y(self):
        y = self.cleaned_data.get('y')
        if y == 0:
            raise forms.ValidationError("Y should not be zero")
        return y