# Author: seedboy
# URL: https://github.com/seedboy
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
from urlparse import urljoin

from requests.utils import dict_from_cookiejar

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import bs4_parser, convert_size, try_int, validate_url
from sickrage.providers import TorrentProvider


class IPTorrentsProvider(TorrentProvider):
    def __init__(self):
        super(IPTorrentsProvider, self).__init__("IPTorrents", 'https://iptorrents.eu', True)

        self.urls.update({
            'login': '{base_url}/take_login.php'.format(**self.urls),
            'search': '{base_url}/t?%s%s&q=%s&qf=#torrents'.format(**self.urls)
        })

        self.username = None
        self.password = None

        self.freeleech = False
        self.enable_cookies = True

        self.minseed = None
        self.minleech = None

        self.categories = '73=&60='

        self.custom_url = ""

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

        login_params = {'username': self.username, 'password': self.password, 'login': 'submit'}

        login_url = self.urls['login']
        if self.custom_url:
            if not validate_url(self.custom_url):
                sickrage.srCore.srLogger.warning("Invalid custom url: {}".format(self.custom_url))
                return False

            login_url = urljoin(self.custom_url, self.urls['login'].split(self.urls['base_url'])[1])

        response = sickrage.srCore.srWebSession.post(login_url, data=login_params, timeout=30)
        if not response.ok:
            sickrage.srCore.srLogger.warning("[{}]: Unable to connect to provider".format(self.name))
            return False

        # Invalid username and password combination
        if re.search('Invalid username and password combination', response.text):
            sickrage.srCore.srLogger.warning(u"Invalid username or password. Check your settings")
            return False

        # You tried too often, please try again after 2 hours!
        if re.search('You tried too often', response.text):
            sickrage.srCore.srLogger.warning(
                u"You tried too often, please try again after 2 hours! Disable IPTorrents for at least 2 hours")
            return False

        # Captcha!
        if re.search('Captcha verification failed.', response.text):
            sickrage.srCore.srLogger.warning(u"Stupid captcha")
            return False

        return True

    def search(self, search_strings, age=0, ep_obj=None):
        results = []

        freeleech = '&free=on' if self.freeleech else ''

        if not self.login():
            return results

        for mode in search_strings:
            sickrage.srCore.srLogger.debug("Search Mode: %s" % mode)
            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug("Search string: %s " % search_string)

                # URL with 50 tv-show results, or max 150 if adjusted in IPTorrents profile
                search_url = self.urls['search'] % (self.categories, freeleech, search_string)
                search_url += ';o=seeders' if mode != 'RSS' else ''

                if self.custom_url:
                    if not validate_url(self.custom_url):
                        sickrage.srCore.srLogger.warning("Invalid custom url: {}".format(self.custom_url))
                        return results
                    search_url = urljoin(self.custom_url, search_url.split(self.urls['base_url'])[1])

                sickrage.srCore.srLogger.debug("Search URL: %s" % search_url)

                try:
                    data = sickrage.srCore.srWebSession.get(search_url).text
                except Exception:
                    sickrage.srCore.srLogger.debug("No data returned from provider")
                    continue

                try:
                    data = re.sub(r'(?im)<button.+?<[/]button>', '', data, 0)
                    with bs4_parser(data) as html:
                        if not html:
                            sickrage.srCore.srLogger.debug("No data returned from provider")
                            continue

                        if html.find(text='No Torrents Found!'):
                            sickrage.srCore.srLogger.debug("Data returned from provider does not contain any torrents")
                            continue

                        torrent_table = html.find('table', id='torrents')
                        torrents = torrent_table.find_all('tr') if torrent_table else []

                        # Continue only if one Release is found
                        if len(torrents) < 2:
                            sickrage.srCore.srLogger.debug("Data returned from provider does not contain any torrents")
                            continue

                        for result in torrents[1:]:
                            try:
                                title = result.find_all('td')[1].find('a').text
                                download_url = self.urls['base_url'] + result.find_all('td')[3].find('a')['href']
                                size = convert_size(result.find_all('td')[5].text, -1)
                                seeders = int(result.find('td', attrs={'class': 'ac t_seeders'}).text)
                                leechers = int(result.find('td', attrs={'class': 'ac t_leechers'}).text)
                            except (AttributeError, TypeError, KeyError):
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
                except Exception as e:
                    sickrage.srCore.srLogger.error("Failed parsing provider. Error: %r" % e)

        # Sort all the items by seeders if available
        results.sort(key=lambda k: try_int(k.get('seeders', 0)), reverse=True)

        return results

