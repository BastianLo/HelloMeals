from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

# How long a share link stays valid. Generous enough to complete a Mealie import, short enough
# that a link pasted somewhere and forgotten doesn't stay a standing public read access forever.
SHARE_LINK_MAX_AGE = 3600

_signer = TimestampSigner(salt="recipe-share")


def make_share_token(hello_fresh_id):
    return _signer.sign_object(hello_fresh_id)


def resolve_share_token(token):
    try:
        return _signer.unsign_object(token, max_age=SHARE_LINK_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
