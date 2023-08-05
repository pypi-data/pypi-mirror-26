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

import json
import traceback
from urlparse import urljoin

import sickrage
from sickrage.notifiers import srNotifiers


class PushbulletNotifier(srNotifiers):
    def __init__(self):
        super(PushbulletNotifier, self).__init__()
        self.name = 'pushbullet'
        self.url = 'https://api.pushbullet.com/v2/'
        self.TEST_EVENT = 'Test'

    def test_notify(self, pushbullet_api):
        sickrage.srCore.srLogger.debug("Sending a test Pushbullet notification.")
        return self._sendPushbullet(
            pushbullet_api,
            event=self.TEST_EVENT,
            message="Testing Pushbullet settings from SiCKRAGE",
            force=True
        )

    def get_devices(self, pushbullet_api):
        sickrage.srCore.srLogger.debug("Retrieving Pushbullet device list.")
        headers = {'Content-Type': 'application/json', 'Access-Token': pushbullet_api}

        try:
            return sickrage.srCore.srWebSession.get(urljoin(self.url, 'devices'), headers=headers).text
        except Exception:
            sickrage.srCore.srLogger.debug(
                'Pushbullet authorization failed with exception: %r' % traceback.format_exc())
            return False

    def _notify_snatch(self, ep_name):
        if sickrage.srCore.srConfig.PUSHBULLET_NOTIFY_ONSNATCH:
            self._sendPushbullet(pushbullet_api=None, event=self.notifyStrings[self.NOTIFY_SNATCH] + " : " + ep_name,
                                 message=ep_name)

    def _notify_download(self, ep_name):
        if sickrage.srCore.srConfig.PUSHBULLET_NOTIFY_ONDOWNLOAD:
            self._sendPushbullet(pushbullet_api=None, event=self.notifyStrings[self.NOTIFY_DOWNLOAD] + " : " + ep_name,
                                 message=ep_name)

    def _notify_subtitle_download(self, ep_name, lang):
        if sickrage.srCore.srConfig.PUSHBULLET_NOTIFY_ONSUBTITLEDOWNLOAD:
            self._sendPushbullet(pushbullet_api=None,
                                 event=self.notifyStrings[self.NOTIFY_SUBTITLE_DOWNLOAD] + " : " + ep_name + " : " + lang,
                                 message=ep_name + ": " + lang)

    def _notify_version_update(self, new_version="??"):
        if sickrage.srCore.srConfig.USE_PUSHBULLET:
            self._sendPushbullet(pushbullet_api=None, event=self.notifyStrings[self.NOTIFY_GIT_UPDATE],
                                 message=self.notifyStrings[self.NOTIFY_GIT_UPDATE_TEXT] + new_version)

    def _sendPushbullet(self, pushbullet_api=None, pushbullet_device=None, event=None, message=None, force=False):
        if not (sickrage.srCore.srConfig.USE_PUSHBULLET or force):
            return False

        pushbullet_api = pushbullet_api or sickrage.srCore.srConfig.PUSHBULLET_API
        pushbullet_device = pushbullet_device or sickrage.srCore.srConfig.PUSHBULLET_DEVICE

        sickrage.srCore.srLogger.debug("Pushbullet event: %r" % event)
        sickrage.srCore.srLogger.debug("Pushbullet message: %r" % message)
        sickrage.srCore.srLogger.debug("Pushbullet api: %r" % pushbullet_api)
        sickrage.srCore.srLogger.debug("Pushbullet devices: %r" % pushbullet_device)

        post_data = {
            'title': event.encode('utf-8'),
            'body': message.encode('utf-8'),
            'type': 'note'
        }

        if pushbullet_device:
            post_data['device_iden'] = pushbullet_device.encode('utf8')

        headers = {'Content-Type': 'application/json', 'Access-Token': pushbullet_api}

        try:
            response = sickrage.srCore.srWebSession.post(
                urljoin(self.url, 'pushes'),
                data=json.dumps(post_data),
                headers=headers
            )
        except Exception:
            sickrage.srCore.srLogger.debug(
                'Pushbullet authorization failed with exception: %r' % traceback.format_exc())
            return False

        if response.status_code == 410:
            sickrage.srCore.srLogger.debug('Pushbullet authorization failed')
            return False

        if not response.ok:
            sickrage.srCore.srLogger.debug('Pushbullet call failed with error code %r' % response.status_code)
            return False

        sickrage.srCore.srLogger.debug("Pushbullet response: %r" % response.text)

        if not response.text:
            sickrage.srCore.srLogger.error("Pushbullet notification failed.")
            return False

        sickrage.srCore.srLogger.debug("Pushbullet notifications sent.")
        return (True, response.text)[event is self.TEST_EVENT or event is None]
