# Author: Idan Gutman
# Modified by jkaberg, https://github.com/jkaberg for SceneAccess
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
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
import urllib

from requests.utils import dict_from_cookiejar

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import bs4_parser, convert_size, try_int
from sickrage.providers import TorrentProvider


class HDTorrentsProvider(TorrentProvider):
    def __init__(self):
        super(HDTorrentsProvider, self).__init__("HDTorrents", 'http://hd-torrents.org', True)

        self.urls.update({
            'login': '{base_url}/login.php'.format(**self.urls),
            'search': '{base_url}/torrents.php?search=%s&active=1&options=0%s'.format(**self.urls),
            'rss': '{base_url}/torrents.php?search=&active=1&options=0%s'.format(**self.urls),
            'home': '{base_url}/%s'.format(**self.urls)
        })

        self.username = None
        self.password = None

        self.minseed = None
        self.minleech = None

        self.categories = "&category[]=59&category[]=60&category[]=30&category[]=38"
        self.proper_strings = ['PROPER', 'REPACK']

        self.cache = TVCache(self, min_time=10)

    def _check_auth(self):

        if not self.username or not self.password:
            sickrage.srCore.srLogger.warning(
                "Invalid username or password. Check your settings".format(self.name))

        return True

    def login(self):
        if any(dict_from_cookiejar(sickrage.srCore.srWebSession.cookies).values()):
            return True

        login_params = {'uid': self.username,
                        'pwd': self.password,
                        'submit': 'Confirm'}

        try:
            response = sickrage.srCore.srWebSession.post(self.urls['login'], data=login_params, timeout=30).text
        except Exception:
            sickrage.srCore.srLogger.warning("Unable to connect to provider".format(self.name))
            return False

        if re.search('You need cookies enabled to log in.', response):
            sickrage.srCore.srLogger.warning(
                "Invalid username or password. Check your settings".format(self.name))
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []

        if not self.login():
            return results

        for mode in search_strings.keys():
            sickrage.srCore.srLogger.debug("Search Mode: %s" % mode)
            for search_string in search_strings[mode]:

                if mode != 'RSS':
                    searchURL = self.urls['search'] % (urllib.quote_plus(search_string), self.categories)
                else:
                    searchURL = self.urls['rss'] % self.categories

                sickrage.srCore.srLogger.debug("Search URL: %s" % searchURL)
                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug("Search string: %s" % search_string)

                try:
                    data = sickrage.srCore.srWebSession.get(searchURL).text
                    results += self.parse(data, mode)
                except Exception:
                    sickrage.srCore.srLogger.debug("No data returned from provider")

        return results

    def parse(self, data, mode):
        """
        Parse search results from data
        :param data: response data
        :param mode: search mode
        :return: search results
        """

        results = []

        if data.find('No torrents here') != -1:
            sickrage.srCore.srLogger.debug("Data returned from provider does not contain any torrents")
            return results

        # Search result page contains some invalid html that prevents html parser from returning all data.
        # We cut everything before the table that contains the data we are interested in thus eliminating
        # the invalid html portions
        try:
            index = data.lower().index('<table class="mainblockcontenttt"')
        except ValueError:
            sickrage.srCore.srLogger.debug("Could not find table of torrents mainblockcontenttt")
            return results

        with bs4_parser(data[index:]) as html:
            if not html:
                sickrage.srCore.srLogger.debug("No html data parsed from provider")
                return results

            torrent_rows = []
            torrent_table = html.find('table', class_='mainblockcontenttt')
            if torrent_table:
                torrent_rows = torrent_table('tr')

            if not torrent_rows:
                sickrage.srCore.srLogger.debug("Could not find results in returned data")
                return results

            # Cat., Active, Filename, Dl, Wl, Added, Size, Uploader, S, L, C
            labels = [label.a.get_text(strip=True) if label.a else label.get_text(strip=True) for label in
                      torrent_rows[0]('td')]

            # Skip column headers
            for result in torrent_rows[1:]:
                try:
                    cells = result.findChildren('td')[:len(labels)]
                    if len(cells) < len(labels):
                        continue

                    title = cells[labels.index('Filename')].a.get_text(strip=True)
                    seeders = try_int(cells[labels.index('S')].get_text(strip=True))
                    leechers = try_int(cells[labels.index('L')].get_text(strip=True))
                    torrent_size = cells[labels.index('Size')].get_text()

                    size = convert_size(torrent_size, -1)
                    download_url = self.urls['base_url'] + '/' + cells[labels.index('Dl')].a['href']

                    if not all([title, download_url]):
                        continue

                    item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders,
                            'leechers': leechers, 'hash': ''}

                    if mode != 'RSS':
                        sickrage.srCore.srLogger.debug("Found result: {}".format(title))

                    results.append(item)
                except Exception:
                    sickrage.srCore.srLogger.error("Failed parsing provider")

        return results