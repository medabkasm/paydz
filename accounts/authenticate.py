from .models import	User


class	emailAuthBackend(object):
    """
    Authenticate	using	an	e-mail	address.
    """
    def	authenticate(self,	request,	username=None,	password=None):
        try:
            user = customUser.objects.get(email = username )
            if	user.check_password(password):
                return	user
            return	None
        except	customUser.DoesNotExist:
            return	None

    def	get_user(self,	user_id):
        try:
            return	customUser.objects.get(pk=user_id)
        except	customUser.DoesNotExist:
            return	None


class phoneAuthBackend(object):
    """
    Authenticate	using	a phone number.
    """
    def	authenticate(self,	request,	username=None,	password=None):
        try:
            user = customUser.objects.get(phone = username )
            if	user.check_password(password):
                return	user
            return	None
        except	customUser.DoesNotExist:
            return	None

    def	get_user(self,	user_id):
        try:
            return	customUser.objects.get(pk=user_id)
        except	customUser.DoesNotExist:
            return	None
