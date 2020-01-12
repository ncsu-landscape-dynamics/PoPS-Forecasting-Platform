from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key and some user state that's sure to change
        after account activation to produce a token that's invalidated when it's
        used:
        1. The user email_confirmed will be changed to True once the link is used.

        Failing this, settings.PASSWORD_RESET_TIMEOUT eventually
        invalidates the token.
        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        """
        return str(user.pk) + str(timestamp) + str(user.email_confirmed)

account_activation_token = AccountActivationTokenGenerator()


