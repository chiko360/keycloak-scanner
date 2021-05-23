from typing import List

from keycloak_scanner.properties import add_kv
from keycloak_scanner.scanners.json_result import JsonResult
from keycloak_scanner.scanners.realm_scanner import Realm, Realms
from keycloak_scanner.scanners.scanner import Scanner
from keycloak_scanner.scanners.scanner_pieces import Need

URL_PATTERN = '{}/auth/realms/{}/.well-known/openid-configuration'


class WellKnown(JsonResult):

    def __init__(self, realm: Realm, **kwargs):
        self.realm = realm
        super().__init__(**kwargs)


WellKnownList = List[WellKnown]


class WellKnownScanner(Need[Realms], Scanner):

    def __init__(self, **kwars):
        super().__init__(**kwars)

    def perform(self, realms: Realms, **kwargs):

        result: WellKnownList = []

        for realm in realms:

            url = URL_PATTERN.format(super().base_url(), realm.name)
            r = super().session().get(url)

            if r.status_code != 200:
                super().verbose('Bad status code for realm {} {}: {}'.format(realm, url, r.status_code))

            else:
                super().info('Find a well known for realm {} {}'.format(realm, url))
                result.append(WellKnown(realm, name=realm.name, url=url, json=r.json()))

        return result
