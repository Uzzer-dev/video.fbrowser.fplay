# -*- coding: utf-8 -*-
# Module: default
# Author: Uzzer
# Created on: 26.03.2020
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

from codequick import Route, Resolver, Listitem, utils, run
import urlquick
import simplejson as json

url_constructor = utils.urljoin_partial("http://nserv.host:5300")

@Route.register
def root(plugin):
    item = Listitem()
    item.label = "RFork online"

    site_url = url_constructor("/")

    item.set_callback(open_site, url=site_url)

    yield item


@Route.register
def open_site(plugin, url, search_query=None):
    if search_query:
        url = url = url + "?search=" + search_query
    url = url_constructor(url)

    site_body_raw = urlquick.get(url)
    site_body_decoded = json.loads(site_body_raw.text)

    if 'channels' in site_body_decoded:
        for channel in site_body_decoded['channels']:
            link = Listitem()
            if 'title' in channel:
                link.label = utils.strip_tags(channel['title'])
            if 'logo_30x30' in channel:
                link.art['thumb'] = channel['logo_30x30']
            if 'playlist_url' in channel:
                if 'search_on' in channel:
                    link.set_callback(user_input, url=channel['playlist_url'])
                else:
                    link.set_callback(open_site, url=channel['playlist_url'])
            elif 'stream_url' in channel:
                link.set_callback(play_media, url=channel['stream_url'])

            yield link
        

@Route.register
def play_media(plugin, url):
    print(url)
    item = Listitem(content_type='video')
    item.label = "Play"
    item.set_callback(url)

    yield item


@Route.register
def user_input(plugin, url):
    item = Listitem()

    yield item.search(open_site, url)
    


if __name__ == "__main__":
    run()
