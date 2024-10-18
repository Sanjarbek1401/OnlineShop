from django import forms
from shop.models import Comment

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Ismingizni kiriting', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Emailingizni kiriting', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Izohingizni yozing', 'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'full_name': 'Ism',
            'email': 'Email',
            'message': 'Izoh',
        }
        help_texts = {
            'email': 'Iltimos, haqiqiy email manzilingizni kiriting.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email maydoni bo'sh bo'lmasligi kerak.")
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Izoh maydoni bo'sh bo'lmasligi kerak.")
        return message
