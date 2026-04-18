#VERSION: 2.00
#AUTHORS: DrPurp

import json
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter


class eztv(object):
    url = 'https://eztvx.to'
    name = 'EZTV'
    supported_categories = {
        'all': 'all',
        'tv': 'tv'
    }

    def __init__(self):
        pass

    def download_torrent(self, info):
        print(download_file(info))

    # DO NOT CHANGE the name and parameters of this function
    def search(self, what, cat='all'):
        keywords = what.replace('%20', '+').replace('-', '+')
        page = 1

        while True:
            api_url = '{}/api/get-torrents?limit=100&page={}&Keywords={}'.format(
                self.url, page, keywords
            )

            try:
                response = retrieve_url(api_url)
                data = json.loads(response)
            except Exception as e:
                break

            torrents = data.get('torrents', [])
            if not torrents:
                break

            for torrent in torrents:
                # Prefer magnet, fall back to .torrent URL
                link = torrent.get('magnet_url') or torrent.get('torrent_url', '')
                if not link:
                    continue

                result = {
                    'link':       link,
                    'name':       torrent.get('title', 'Unknown'),
                    'size':       self._format_size(torrent.get('size_bytes', -1)),
                    'seeds':      int(torrent.get('seeds', 0)),
                    'leech':      int(torrent.get('peers', 0)),
                    'engine_url': self.url,
                    'desc_link':  torrent.get('episode_url', self.url),
                }
                prettyPrinter(result)

            # Stop if we've exhausted all results
            total = data.get('torrents_count', 0)
            if page * 100 >= int(total) or len(torrents) < 100:
                break

            page += 1

    def _format_size(self, size_bytes):
        """Convert bytes to a human-readable size string."""
        try:
            size_bytes = int(size_bytes)
        except (TypeError, ValueError):
            return '-1'

        if size_bytes < 0:
            return '-1'
        elif size_bytes < 1024 ** 2:
            return '{:.1f} KB'.format(size_bytes / 1024)
        elif size_bytes < 1024 ** 3:
            return '{:.1f} MB'.format(size_bytes / (1024 ** 2))
        else:
            return '{:.2f} GB'.format(size_bytes / (1024 ** 3))