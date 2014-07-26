OAUTH_LABEL='OAuth '

#Transforms OAuth2 credentials to OAuth2 token.
class OAuthCred2Token(object):

    def __init__(self, token_string):
        self.token_string = token_string

    def modify_request(self, http_request):
        http_request.headers['Authorization'] = '%s%s' % (OAUTH_LABEL,
                                                          self.token_string)