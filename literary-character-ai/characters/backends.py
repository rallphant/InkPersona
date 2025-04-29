from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

UserModel = get_user_model()

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    """
    Custom authentication backend.

    Allows users to authenticate using their email address instead of username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Overrides the default authenticate method to use email.

        Args:
            request: The HttpRequest object.
            username: The email address entered by the user (passed as username).
            password: The password entered by the user.
            **kwargs: Additional keyword arguments (may include 'email').

        Returns:
            The authenticated user object or None.
        """
        # Django's AuthenticationForm passes the primary identifier as 'username'.
        # We treat this 'username' parameter as the email address here.
        # We also check kwargs for 'email' for flexibility.
        email = username or kwargs.get('email')

        if not email:
            return None # Cannot authenticate without an email

        try:
            # Case-insensitive lookup for the user by email
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce timing attacks
            UserModel().set_password(password)
            return None
        except UserModel.MultipleObjectsReturned:
            # If multiple users have the same email (shouldn't happen with unique=True),
            # return the first one based on ID. Log this occurrence if necessary.
            logger.warning(f"Multiple users found with email: {email}")
            user = UserModel.objects.filter(email__iexact=email).order_by('id').first()

        # Check password and if the user is allowed to authenticate
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to retrieve a user by their primary key.
        Required by the authentication framework.
        """
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
