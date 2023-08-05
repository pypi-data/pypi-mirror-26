"""PytSite Auth HTTP API
"""
from pytsite import events as _events, util as _util, logger as _logger, routing as _routing, http_api as _http_api, \
    formatters as _formatters, validation as _validation, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _get_access_token_info(token: str) -> dict:
    r = _auth.get_access_token_info(token)
    r.update({
        'token': token,
        'created': _util.w3c_datetime_str(r['created']),
        'expires': _util.w3c_datetime_str(r['expires']),
    })

    return r


class PostAccessToken(_routing.Controller):
    """Issue new access token
    """

    def exec(self) -> dict:
        try:
            # Try to sign in user via driver
            user = _auth.sign_in(self.arg('driver'), dict(self.args))

            return _get_access_token_info(_auth.generate_access_token(user))

        except (_auth.error.AuthenticationError, _auth.error.UserNotExist) as e:
            _logger.warn(e)
            raise self.forbidden()


class GetAccessToken(_routing.Controller):
    """Get information about an access token
    """

    def exec(self) -> dict:
        try:
            return _get_access_token_info(self.arg('token'))

        except _auth.error.InvalidAccessToken as e:
            raise self.forbidden(str(e))


class DeleteAccessToken(_routing.Controller):
    """Delete an access token
    """

    def exec(self) -> dict:
        try:
            _auth.sign_out(_auth.get_current_user())
            _auth.revoke_access_token(self.arg('token'))

            return {'status': True}

        except (_auth.error.UserNotExist, _auth.error.InvalidAccessToken) as e:
            raise self.forbidden(str(e))


class IsAnonymous(_routing.Controller):
    """Check if the current user is anonymous
    """

    def exec(self):
        return _auth.get_current_user().is_anonymous


class GetUser(_routing.Controller):
    """Get information about user
    """

    def exec(self) -> dict:
        try:
            user = _auth.get_user(uid=self.arg('uid'))
            r = user.as_jsonable()
            _events.fire('pytsite.auth.http_api.get_user', user=user, response=r)

            return r

        except _auth.error.UserNotExist:
            raise self.forbidden()


class PatchUser(_routing.Controller):
    """Update user
    """

    def __init__(self):
        super().__init__()
        self.args.add_formatter('birth_date', _formatters.DateTime())
        self.args.add_formatter('urls', _formatters.JSONArrayToList())
        self.args.add_formatter('profile_is_public', _formatters.Bool())

        self.args.add_validation('email', _validation.rule.DateTime())
        self.args.add_validation('gender', _validation.rule.Choice(options=('m', 'f')))

    def exec(self) -> dict:
        user = _auth.get_current_user()

        # Check permissions
        if user.is_anonymous or (user.uid != self.arg('uid') and not user.is_admin):
            raise self.forbidden()

        allowed_fields = ('email', 'nickname', 'first_name', 'last_name', 'description', 'birth_date',
                          'gender', 'phone', 'urls', 'profile_is_public', 'country', 'city', 'picture')

        for k, v in self.args.items():
            if k in allowed_fields:
                user.set_field(k, v)

        if user.is_modified:
            user.save()

        return _http_api.call('pytsite.auth@get_user', {'uid': user.uid})


class PostFollow(_routing.Controller):
    """Follow a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to follow
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        user.add_follower(current_user).save()
        current_user.add_follows(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.follow', user=user, follower=current_user)

        return {'follows': current_user.as_jsonable()['follows']}


class DeleteFollow(_routing.Controller):
    """Unfollow a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unfollow
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        user.remove_follower(current_user).save()
        current_user.remove_follows(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.unfollow', user=user, follower=current_user)

        return {'follows': current_user.as_jsonable()['follows']}


class PostBlockUser(_routing.Controller):
    """Block a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to block
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        current_user.add_blocked_user(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.block_user', user=user, blocker=current_user)

        return {'blocked_users': current_user.as_jsonable()['blocked_users']}


class DeleteBlockUser(_routing.Controller):
    """Unblock a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unblock
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        current_user.remove_blocked_user(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.unblock_user', user=user, blocker=current_user)

        return {'blocked_users': current_user.as_jsonable()['blocked_users']}
