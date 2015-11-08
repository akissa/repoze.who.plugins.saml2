
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

# pylint: disable=invalid-name,bad-builtin
version_info = (0, 0, 1)
__author__ = "Andrew Colin Kissa"
__copyright__ = u"© 2010-2015 Andrew Colin Kissa"
__email__ = "andrew@topdog.za.net"
__version__ = ".".join(map(str, version_info))
