import requests
import os
import time
import re

import libtorrent as lt

from bs4 import BeautifulSoup


class TrackerUtils(object):
    main_login_url = 'https://aidoru-online.org/login.php'
    form_login_url = 'https://aidoru-online.org/login.php?type=login'
    main_info_url = 'https://aidoru-online.org'
    get_ttable_url = 'https://aidoru-online.org/get_ttable.php?pcat=H!P&typ=name&scat=11&subbed=&fl=&p={}&searchstr=&deadlive=0'

    payload = {
        'username': '',
        'password': '',
        'do': 'login',
        'language': '',
        'csrfp_token': None,
    }

    session = None

    def __init__(self):
        self._init_session()

    def _init_session(self):
        self.session = requests.session()
        response = self.session.get(self.main_login_url)
        response.raise_for_status()

        self.payload['csrfp_token'] = response.cookies['csrfp_token']
        response = self.session.post(self.form_login_url, data=self.payload)
        response.raise_for_status()

    def get_radio_programs_data(self, how_many_pages=1):
        if self.session is None:
            self._init_session()

        radio_programs_data_list = []
        for page in range(0, how_many_pages):
            get_ttable_url_formated = self.get_ttable_url.format(page)
            response = self.session.get(get_ttable_url_formated)

            soup = BeautifulSoup(response.content, 'html.parser')
            all_tr = soup.find_all('tr', class_='t-row')
            for tr in all_tr:
                all_td = tr.find_all('td')
                title = all_td[1].a['title']
                href = all_td[1].a['href'].split('=')[1].split('&')[0]
                added_date = all_td[9].text
                radio_programs_data_list.append((href, title, added_date))

        return radio_programs_data_list

    def download_torrent(self, inner_identifier, username):
        if self.session is None:
            self._init_session()

        print "download .torrent"
        url = 'https://aidoru-online.org/download.php?id={}'.format(inner_identifier)
        local_filename = os.path.normpath(
            '{}\\hpradiotracker\\static\\hpradiotracker\\media\\{}_{}.torrent'.format(os.getcwd(), inner_identifier, username)
        )

        # Download .torrent file
        response = self.session.get(url)
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk is not None:
                    file.write(chunk)
                    file.flush()

        # download real file from the
        self._download_real_torrent(inner_identifier=inner_identifier, username=username)
        print "end download .torrent"

    def _download_real_torrent(self, inner_identifier, username):

        downloaded_torrent_path = os.path.normpath(
            '{}\\hpradiotracker\\static\\hpradiotracker\\media\\'.format(os.getcwd())
        )
        downloaded_torrent_file = os.path.normpath(
            '{}_{}.torrent'.format(inner_identifier, username)
        )
        downloaded_audio_file = os.path.normpath(
            '{}_{}.mp3'.format(inner_identifier, username)
        )

        ses = lt.session()
        ses.listen_on(6881, 68911)
        info = lt.torrent_info(os.path.normpath(downloaded_torrent_path + '\\' + downloaded_torrent_file))
        # filename, extension = os.path.splitext(info.name())
        info.rename_file(0, str(downloaded_audio_file))

        params = {
            'ti': info,
            'save_path': downloaded_torrent_path,
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True
        }
        handler = ses.add_torrent(params)
        ses.start_dht()

        print('...downloading metadata...')
        while not handler.has_metadata():
            time.sleep(1)
        print('...got metadata, starting torrent download...')
        while handler.status().state != lt.torrent_status.seeding:
            s = handler.status()
            # state_str = ['queued', 'checking', 'downloading metadata',
            #              'downloading', 'finished', 'seeding', 'allocating']
            # print s.progress * 100, '% complete (down: ', s.download_rate / 1000, 'kb/s up: ', s.upload_rate / 1000,
            #  ' kB/s peers: ', ,') ', state_str[s.state], ' ', s.total_download/1000000'
            print ('File: ' + str(downloaded_audio_file) + ' ' + str(s.progress * 100) + '% ' + 'Download:' + str(s.download_rate / 1000) + ' Seeds:' + str(s.num_peers))
            time.sleep(5)

        print('...done')
