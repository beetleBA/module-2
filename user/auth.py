from rest_framework.authentication import TokenAuthentication


class BearerToken(TokenAuthentication):
    keyword = 'bearer'
