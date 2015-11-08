# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# repoze.who.plugins.saml2: A SAML2 plugin for repoze.who
# Copyright (C) 2015 Andrew Colin Kissa <andrew@topdog.za.net>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""
repoze.who.plugins.saml2: A SAML2 plugin for repoze.who
Copyright (C) 2015 Andrew Colin Kissa <andrew@topdog.za.net>
"""
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import logging


from webob import Request
from webob.exc import HTTPFound
from repoze.who.interfaces import (
    IChallenger,
    IIdentifier,
    IAuthenticator,
    IMetadataProvider
)
from zope.interface import implements
from lasso import (
    Server,
    Login,
    Error,
    PROVIDER_ROLE_IDP,
    SAML2_FIELD_RESPONSE
)

# from .utils import get_attributes_from_assertion

logger = logging.getLogger(__name__)


def get_came_from(environ):
    """get the url the user came from"""
    came_from = environ.get("PATH_INFO")
    qstr = environ.get("QUERY_STRING", "")
    if qstr:
        came_from += '?' + qstr
    return came_from


class SAML2Plugin(object):
    """docstring for SAML2Plugin"""

    implements(
        IChallenger,
        IIdentifier,
        IAuthenticator,
        IMetadataProvider
    )

    def __init__(
            self,
            rememberer_name,
            sp_metadata,
            sp_priv_key,
            sp_cert,
            idp_metadata,
            idp_cert=None,
            idp_ca_cert=None,
            logout_handler_path=None,
            post_logout_url=None):
        self.sp_metadata = sp_metadata
        self.sp_priv_key = sp_priv_key
        self.sp_cert = sp_cert
        self.idp_metadata = idp_metadata
        self.idp_cert = idp_cert
        self.idp_ca_cert = idp_ca_cert
        self.rememberer_name = rememberer_name
        self.logout_handler_path = logout_handler_path
        self.post_logout_url = post_logout_url
        self.server = Server(
            self.sp_metadata,
            self.sp_priv_key,
            certificate=self.sp_cert
        )
        self.server.addProvider(
            PROVIDER_ROLE_IDP,
            self.idp_metadata,
            self.idp_cert,
            self.idp_ca_cert
        )

    def _get_rememberer(self, environ):
        """Get the rememberer"""
        rememberer = environ['repoze.who.plugins'][self.rememberer_name]
        return rememberer

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))

    # IIdentifier
    def identify(self, environ):
        """identify"""
        req = Request(environ)
        if SAML2_FIELD_RESPONSE not in req.POST:
            logger.debug('[saml2.identify] got an empty request')
            return {}

        uri = req.path
        logger.debug('[saml2.identify] uri: %s', uri)

        # path = req.path
        login = Login(self.server)
        try:
            login.processAuthnResponseMsg(req.POST[SAML2_FIELD_RESPONSE])
            # request_id = login.response.inResponseTo
            login.acceptSso()
            # attribs = get_attributes_from_assertion(login.assertion)
            username = login.nameIdentifier
            return {
                'login': username,
                'password': '',
                'repoze.who.userid': username,
                'user': '',
            }
        except Error as msg:
            logger.debug(msg)
            return {}
        return None

    # IIdentifier
    def remember(self, environ, identity):
        """remember"""
        rememberer = self._get_rememberer(environ)
        return rememberer.remember(environ, identity)

    # IIdentifier
    def forget(self, environ, identity):
        """forget"""
        rememberer = self._get_rememberer(environ)
        return rememberer.forget(environ, identity)

    # IAuthenticatorPlugin
    def authenticate(self, environ, identity):
        """authenticate"""
        return identity.get('login')

    # IChallenger
    def challenge(self, environ, status, app_headers, forget_headers):
        """challenge"""
        req = Request(environ)
        if req.path in [self.logout_handler_path, self.post_logout_url]:
            headers = app_headers + forget_headers
            return HTTPFound(headers=headers)
        else:
            came_from = get_came_from(environ)
            logger.debug("[saml2.challenge] RelayState >> '%s'", came_from)
            login = Login(self.server)
            try:
                login.initAuthnRequest()
                login.buildAuthnRequestMsg()
                logger.debug(
                    "[saml2.challenge] RequestID: %r", login.request.iD
                )
                headers = [('Location', login.msgUrl)]
                logger.debug(
                    "[saml2.challenge] Redirected to: %s", login.msgUrl
                )
                cookies = [
                    (_hdr, _val) for (_hdr, _val) in app_headers
                    if _hdr.lower() == 'set-cookie'
                ]
                headers = headers + forget_headers + cookies
                return HTTPFound(headers=headers)
            except Error as msg:
                logger.debug("[saml2.challenge] error: %s", msg)
                raise

    # IMetadataProvider
    def add_metadata(self, environ, identity):
        """add_metadata"""
        return {}


def make_saml2_plugin(
        sp_metadata=None,
        sp_priv_key=None,
        sp_cert=None,
        idp_metadata=None,
        idp_cert=None,
        idp_ca_cert=None,
        remember_name=None,
        logout_handler_path=None,
        post_logout_url=None):
    """Return the plugin"""
    plugin = SAML2Plugin(
        remember_name,
        sp_metadata,
        sp_priv_key,
        sp_cert,
        idp_metadata,
        idp_cert,
        idp_ca_cert,
        logout_handler_path,
        post_logout_url
    )
    return plugin
