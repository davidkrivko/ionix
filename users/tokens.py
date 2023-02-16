#Token generator utility for account confirmation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six

class UserTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):

        return f'{user.pk}{timestamp}'

user_tokenizer = UserTokenGenerator()



class PasswordResetTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):

        return f'{user.pk}{timestamp}{user.updated_at}'

password_reset_tokenizer = PasswordResetTokenGenerator()