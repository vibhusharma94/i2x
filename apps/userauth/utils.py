from apps.userauth import models as userauth_models


def validate_user_auth_token(authenticated_user):
    """
    Util to Get Token and profile detail data for an authenticated User
    """
    # Get or Create token
    token, created = userauth_models.CustomToken.objects.get_or_create(user=authenticated_user)
    return token

def get_token_dict(token):
    token_dict = {
        'token': token.key,
        'refresh_token': token.refresh_token,
        'expiry_time': token.get_epoch_expiry_time()
    }
    return token_dict