from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256",],
        default="pbkdf2_sha256",

        all__vary_rounds = 0.1,

        pbkdf2_sha256__default_rounds = 20000,
)

class PasswordAlreadySetException(Exception):
    pass

class PasswordIncorrectException(Exception):
    pass

class PasswordChangeFailureException(Exception):
    pass

class User(object):
    def __init__(self, username):
        self.username = username
        self.energy = 0.00

        self.password = None
        self.auth = False

    def set_password(self, password):
        if self.password is not None:
            raise PasswordAlreadySetException()
        else:
            self.password = pwd_context.encrypt(password)

    def change_password(self, old_password, new_password):
        if self.password is None:
            raise PasswordChangeFailureException("Can not change password when no password is set.")
        elif not pwd_context.verify(old_password, self.password):
            raise PasswordIncorrectException()
        else:
            self.password = pwd_context.encrypt(new_password)

    def verify_password(self, password):
        if pwd_context.verify(password, self.password) is True:
            self.auth = True
        else:
            self.auth = False
            raise PasswordIncorrectException()
