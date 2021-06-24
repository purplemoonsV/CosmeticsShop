from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="อีเมลล์")
    password = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput(render_value=True)
)


class SearchForm(forms.Form):
    name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ป้อนชื่อ'})
 )


class ProductForm(forms.Form):
    class Meta:
        model='Product'
        fields='__all__'