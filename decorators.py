from functools import wraps
# WARNING: Method decorator
def is_authenticated(method):

    @wraps(method)
    def inner(session, *args, **kwargs):

        assert session.authenticated, ('The session object must be ' \
            f'authenticated prior calling session.{method.__name__}')

        return method(session, *args, **kwargs)

    return inner
# WARNING: Method decorator
def versionize(method):

    @wraps(method)
    def inner(session,*args,**kwargs):

        session.headers.update(
                {'x-li-page-instance':'urn:li:page:d_fl' \
                'agship3_profile_self_edit_top_card;' + \
                session.getTrackingId()}
            )

        if 'params' in kwargs:
            kwargs['params']['versionTag'] = self.getVersionTag()
        else:
            kwargs['params'] = {'versionTag':session.getVersionTag()}

        ret = method(session, *args, **kwargs)

        del(session.headers['x-li-page-instance'])

        return ret

    return inner
