# coding=utf-8
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

from requests.compat import urljoin
from requests.utils import dict_from_cookiejar

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import try_int, convert_size, bs4_parser
from sickrage.providers import TorrentProvider


class ABNormalProvider(TorrentProvider):
    def __init__(self):
        super(ABNormalProvider, self).__init__("ABNormal", 'https://abnormal.ws', True)

        # Credentials
        self.username = None
        self.password = None

        # Torrent Stats
        self.minseed = None
        self.minleech = None

        # URLs
        self.urls.update({
            'login': '{base_url}/login.php'.format(**self.urls),
            'search': '{base_url}/torrents.php'.format(**self.urls),
        })

        # Proper Strings
        self.proper_strings = ['PROPER']

        # Cache
        self.cache = TVCache(self, min_time=30)

    def login(self):
        if any(dict_from_cookiejar(sickrage.srCore.srWebSession.cookies).values()):
            return True

        login_params = {
            'username': self.username,
            'password': self.password,
        }

        response = sickrage.srCore.srWebSession.post(self.urls['login'], data=login_params).text
        if not response:
            sickrage.srCore.srLogger.warning('Unable to connect to provider')
            return False

        if not re.search('torrents.php', response):
            sickrage.srCore.srLogger.warning('Invalid username or password. Check your settings')
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []

        if not self.login():
            return results

        # Search Params
        search_params = {
            'way': 'DESC',
            'cat[]': ['TV|SD|VOSTFR',
                      'TV|HD|VOSTFR',
                      'TV|SD|VF',
                      'TV|HD|VF',
                      'TV|PACK|FR',
                      'TV|PACK|VOSTFR',
                      'TV|EMISSIONS',
                      'ANIME']
        }

        for mode in search_strings:
            sickrage.srCore.srLogger.debug('Search Mode: {0}'.format(mode))

            for search_string in search_strings[mode]:

                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug('Search string: {}'.format(search_string))

                # Sorting: Available parameters: ReleaseName, Seeders, Leechers, Snatched, Size
                search_params['order'] = ('Seeders', 'Time')[mode == 'RSS']
                search_params['search'] = re.sub(r'[()]', '', search_string)
                data = sickrage.srCore.srWebSession.get(self.urls['search'], params=search_params).text
                if not data:
                    continue

                with bs4_parser(data) as html:
                    torrent_table = html.find(class_='torrent_table')
                    torrent_rows = torrent_table('tr') if torrent_table else []

                    # Continue only if at least one Release is found
                    if len(torrent_rows) < 2:
                        sickrage.srCore.srLogger.debug('Data returned from provider does not contain any torrents')
                        continue

                    # Catégorie, Release, Date, DL, Size, C, S, L
                    labels = [label.get_text(strip=True) for label in torrent_rows[0]('td')]

                    # Skip column headers
                    for result in torrent_rows[1:]:
                        cells = result('td')
                        if len(cells) < len(labels):
                            continue

                        try:
                            title = cells[labels.index('Release')].get_text(strip=True)
                            download_url = urljoin(self.urls['base_url'],
                                                   cells[labels.index('DL')].find('a', class_='tooltip')['href'])
                            if not all([title, download_url]):
                                continue

                            seeders = try_int(cells[labels.index('S')].get_text(strip=True))
                            leechers = try_int(cells[labels.index('L')].get_text(strip=True))

                            # Filter unseeded torrent
                            if seeders < self.minseed or leechers < self.minleech:
                                if mode != 'RSS':
                                    sickrage.srCore.srLogger.debug(
                                        'Discarding torrent because it doesn\'t meet the minimum seeders or leechers: '
                                        '{} (S:{} L:{})'.format(title, seeders, leechers))
                                continue

                            size_index = labels.index('Size') if 'Size' in labels else labels.index('Taille')

                            units = ['O', 'KO', 'MO', 'GO', 'TO', 'PO']
                            size = convert_size(cells[size_index].get_text(), -1, units)

                            item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders,
                                    'leechers': leechers, 'hash': ''}

                            if mode != 'RSS':
                                sickrage.srCore.srLogger.debug('Found result: {0}'.format(title))

                            results.append(item)
                        except StandardError:
                            continue

        # Sort all the items by seeders if available
        results.sort(key=lambda k: try_int(k.get('seeders', 0)), reverse=True)

        return results
