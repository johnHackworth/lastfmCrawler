import urllib2
from xml.dom.minidom import parse, parseString

class Lastfm:
    api_key = '1a1f50151cb39efc730eac9ba810e585'
    base_url = 'http://ws.audioscrobbler.com/2.0/?method='

    def __init__(self):
        self.artists = []

    def url(self, username):
        url = self.base_url + "user.gettopartists&user=" + username +\
        "&api_key=" + self.api_key + "&limit=100"
        return url

    def fetch(self, user):
        req = urllib2.Request(self.url(user))
        response = urllib2.urlopen(req)
        xml_response = response.read()
        dom = parseString(xml_response)
        self.parseArtists(dom)

    def parseArtists(self, dom):
        self.artists = []
        for i in range(dom.getElementsByTagName('artist').length):
            artist = self.getArtist(dom, i)
            self.artists.append(artist)

    def getArtists(self):
        artist_names = []
        for i in range(len(self.artists)):
            artist_names.append(self.artists[i]['name'])
        return artist_names

    def getArtist(self, dom, index):
        artist = dom.getElementsByTagName('artist')[index]
        artistData = {}
        artistData['name'] = artist.getElementsByTagName('name')[0].firstChild.nodeValue
        for image in artist.getElementsByTagName('image'):
            if image.getAttribute('size') == 'small':
                artistData['thumbnail'] = image.firstChild.nodeValue
            elif image.getAttribute('size') == 'medium':
                artistData['image'] = image.firstChild.nodeValue
            elif image.getAttribute('size') == 'large':
                artistData['largeImage'] = image.firstChild.nodeValue
        return artistData
