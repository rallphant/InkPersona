from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

# Get the currently active user model
UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that requires email and includes it in the fields.
    """
    # Add email field and make it required for signup
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        # Specify the fields to display on the signup form
        fields = ("username", "email")

    def save(self, commit=True):
        """
        Save the user, ensuring the email from the form is correctly assigned.
        """
        user = super().save(commit=False)
        # Assign the cleaned email data to the user's email field
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EmailLoginForm(AuthenticationForm):
    """
    A custom authentication form that uses email instead of username for login.
    """
    # Override the default 'username' field to accept an email address
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'})
    )
