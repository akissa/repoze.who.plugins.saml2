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
from lasso import SAML2_ATTRIBUTE_NAME_FORMAT_BASIC


def get_attributes_from_assertion(assertion):
    attributes = dict()
    if not assertion:
        return attributes
    for _statement in assertion.attributeStatement:
        for attribute in _statement.attribute:
            name = None
            nickname = None
            _format = SAML2_ATTRIBUTE_NAME_FORMAT_BASIC
            try:
                name = attribute.name.decode('ascii')
            except BaseException:
                pass
            else:
                try:
                    if attribute.nameFormat:
                        _format = attribute.nameFormat.decode('ascii')
                    if attribute.friendlyName:
                        nickname = attribute.friendlyName
                except BaseException:
                    pass
                try:
                    values = attribute.attributeValue
                    if values:
                        attributes[(name, _format)] = []
                        if nickname:
                            attributes[nickname] = attributes[(name, _format)]
                    for value in values:
                        content = [_any.exportToXml() for _any in value.any]
                        content = ''.join(content)
                        attributes[
                            (name, _format)
                        ].append(content.decode('utf8'))
                except BaseException:
                    pass
    attributes['__issuer'] = assertion.issuer.content
    attributes['__nameid'] = assertion.subject.nameID.content
    return attributes
