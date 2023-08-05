# coding=utf-8
# Author: CristianBB
#
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals

import re

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import bs4_parser, try_int
from sickrage.providers import TorrentProvider


class EliteTorrentProvider(TorrentProvider):
    def __init__(self):
        super(EliteTorrentProvider, self).__init__('EliteTorrent', 'http://www.elitetorrent.net', True)

        self.onlyspasearch = None
        self.minseed = None
        self.minleech = None

        self.urls.update({
            'search': '{base_url}/torrents.php'.format(**self.urls)
        })

        self.cache = TVCache(self)

    def search(self, search_strings, age=0, ep_obj=None):
        results = []
        lang_info = '' if not ep_obj or not ep_obj.show else ep_obj.show.lang

        """
        Search query:
        http://www.elitetorrent.net/torrents.php?cat=4&modo=listado&orden=fecha&pag=1&buscar=fringe

        cat = 4 => Shows
        modo = listado => display results mode
        orden = fecha => order
        buscar => Search show
        pag = 1 => page number
        """

        search_params = {
            'cat': 4,
            'modo': 'listado',
            'orden': 'fecha',
            'pag': 1,
            'buscar': ''

        }

        for mode in search_strings:
            sickrage.srCore.srLogger.debug("Search Mode: {0}".format(mode))

            # Only search if user conditions are true
            if self.onlyspasearch and lang_info != 'es' and mode != 'RSS':
                sickrage.srCore.srLogger.debug("Show info is not spanish, skipping provider search")
                continue

            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug("Search string: {0}".format(search_string))

                search_string = re.sub(r'S0*(\d*)E(\d*)', r'\1x\2', search_string)
                search_params['buscar'] = search_string.strip() if mode != 'RSS' else ''

                data = sickrage.srCore.srWebSession.get(self.urls['search'], params=search_params).text
                if not data:
                    continue

                try:
                    with bs4_parser(data) as html:
                        torrent_table = html.find('table', class_='fichas-listado')
                        torrent_rows = torrent_table('tr') if torrent_table else []

                        if len(torrent_rows) < 2:
                            sickrage.srCore.srLogger.debug("Data returned from provider does not contain any torrents")
                            continue

                        for row in torrent_rows[1:]:
                            try:
                                download_url = self.urls['base_url'] + row.find('a')['href']
                                row_title = row.find('a', class_='nombre')['title']
                                title = self._processTitle(row_title.encode('latin-1').decode('utf8'))

                                seeders = try_int(row.find('td', class_='semillas').get_text(strip=True))
                                leechers = try_int(row.find('td', class_='clientes').get_text(strip=True))

                                # seeders are not well reported. Set 1 in case of 0
                                seeders = max(1, seeders)

                                # Provider does not provide size
                                size = -1

                            except (AttributeError, TypeError, KeyError, ValueError):
                                continue

                            if not all([title, download_url]):
                                continue

                            # Filter unseeded torrent
                            if seeders < self.minseed or leechers < self.minleech:
                                if mode != 'RSS':
                                    sickrage.srCore.srLogger.debug(
                                        "Discarding torrent because it doesn't meet the minimum seeders or leechers: "
                                        "{} (S:{} L:{})".format(title, seeders, leechers))
                                continue

                            item = {'title': title, 'link': download_url, 'size': size, 'seeders': seeders,
                                    'leechers': leechers, 'hash': ''}

                            if mode != 'RSS':
                                sickrage.srCore.srLogger.debug("Found result: {}".format(title))

                            results.append(item)
                except Exception:
                    sickrage.srCore.srLogger.error("Failed parsing provider")

        # Sort all the items by seeders if available
        results.sort(key=lambda k: try_int(k.get('seeders', 0)), reverse=True)

        return results

    @staticmethod
    def _processTitle(title):

        # Quality, if no literal is defined it's HDTV
        if 'calidad' not in title:
            title += ' HDTV x264'

        title = title.replace('(calidad baja)', 'HDTV x264')
        title = title.replace('(Buena calidad)', '720p HDTV x264')
        title = title.replace('(Alta calidad)', '720p HDTV x264')
        title = title.replace('(calidad regular)', 'DVDrip x264')
        title = title.replace('(calidad media)', 'DVDrip x264')

        # Language, all results from this provider have spanish audio, we append it to title (avoid to download undesired torrents)
        title += ' SPANISH AUDIO'
        title += '-ELITETORRENT'

        return title.strip()
