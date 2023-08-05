# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re

from requests.utils import dict_from_cookiejar

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import try_int
from sickrage.providers import TorrentProvider


class TorrentDayProvider(TorrentProvider):
    def __init__(self):
        super(TorrentDayProvider, self).__init__("TorrentDay", 'https://www.torrentday.com', True)

        self.urls.update({
            'login': '{base_url}/t'.format(**self.urls),
            'search': '{base_url}/V3/API/API.php'.format(**self.urls),
            'download': '{base_url}/download.php/%s/%s'.format(**self.urls)
        })

        self.username = None
        self.password = None

        self.freeleech = False
        self.minseed = None
        self.minleech = None

        self.enable_cookies = True

        self.categories = {
            'Season': {'c14': 1},
            'Episode': {'c2': 1, 'c26': 1, 'c7': 1, 'c24': 1, 'c34': 1},
            'RSS': {'c2': 1, 'c26': 1, 'c7': 1, 'c24': 1, 'c34': 1, 'c14': 1}
        }

        self.cache = TVCache(self, min_time=10)

    def login(self):
        cookie_dict = dict_from_cookiejar(sickrage.srCore.srWebSession.cookies)
        if cookie_dict.get('uid') and cookie_dict.get('pass'):
            return True

        if not self.cookies:
            sickrage.srCore.srLogger.info('You need to set your cookies to use {}'.format(self.name))
            return False

        if not self.add_cookies_from_ui():
            return False

        login_params = {'username': self.username, 'password': self.password, 'submit.x': 0, 'submit.y': 0}

        response = sickrage.srCore.srWebSession.post(self.urls['login'], data=login_params)
        if not response.ok:
            sickrage.srCore.srLogger.warning("[{}]: Unable to connect to provider".format(self.name))
            return False

        if re.search('You tried too often', response.text):
            sickrage.srCore.srLogger.warning("Too many login access attempts")
            return False

        if not dict_from_cookiejar(sickrage.srCore.srWebSession.cookies).get('uid') in response.text:
            sickrage.srCore.srLogger.warning("Failed to login, check your cookies")
            return False

        return True

    def search(self, search_params, age=0, ep_obj=None):
        results = []

        if not self.login():
            return results

        for mode in search_params.keys():
            sickrage.srCore.srLogger.debug("Search Mode: %s" % mode)
            for search_string in search_params[mode]:

                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug("Search string: %s " % search_string)

                search_string = '+'.join(search_string.split())

                post_data = dict({'/browse.php?': None, 'cata': 'yes', 'jxt': 8, 'jxw': 'b', 'search': search_string},
                                 **self.categories[mode])

                if self.freeleech:
                    post_data.update({'free': 'on'})

                try:
                    data = sickrage.srCore.srWebSession.post(self.urls['search'], data=post_data, cache=False).json()
                    torrents = data['Fs'][0]['Cn']['torrents']
                except Exception:
                    sickrage.srCore.srLogger.debug("No data returned from provider")
                    continue

                for torrent in torrents:
                    title = re.sub(r"\[.*=.*\].*\[/.*\]", "", torrent['name'])
                    download_url = self.urls['download'] % (torrent['id'], torrent['fname'])
                    seeders = int(torrent['seed'])
                    leechers = int(torrent['leech'])
                    # FIXME
                    size = -1

                    if not all([title, download_url]):
                        continue

                    # Filter unseeded torrent
                    if seeders < self.minseed or leechers < self.minleech:
                        if mode != 'RSS':
                            sickrage.srCore.srLogger.debug(
                                "Discarding torrent because it doesn't meet the minimum seeders or leechers: {} (S:{} L:{})".format(
                                    title, seeders, leechers))
                        continue

                    item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders,
                            'leechers': leechers, 'hash': ''}

                    if mode != 'RSS':
                        sickrage.srCore.srLogger.debug("Found result: {}".format(title))

                    results.append(item)

        # Sort all the items by seeders if available
        results.sort(key=lambda k: try_int(k.get('seeders', 0)), reverse=True)

        return results
