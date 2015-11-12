import sys
try:
    import unittest2
except ImportError:
    if sys.version_info < (2, 7):
        raise
    import unittest as unittest2


from repoze.who.interfaces import (
    IChallenger,
    IIdentifier,
    IAuthenticator,
    IMetadataProvider
)
from zope.interface.verify import verifyClass

from repoze.who.plugins.saml2 import SAML2Plugin


class SAML2PluginTestCase(unittest2.TestCase):

    def test_implements(self):
        verifyClass(IChallenger, SAML2Plugin)
        verifyClass(IIdentifier, SAML2Plugin)
        verifyClass(IAuthenticator, SAML2Plugin)
        verifyClass(IMetadataProvider, SAML2Plugin)

if __name__ == "__main__":
    unittest2.main()
