import urllib
import urllib2
from xml.dom.minidom import parse, parseString

class Lastfm:
    api_key = '1a1f50151cb39efc730eac9ba810e585'
    base_url = 'http://ws.audioscrobbler.com/2.0/?method='


    def __init__(self):
        self.artists = []
        self.number_of_artists=100

    def url(self, username):
        url = self.base_url + "user.gettopartists&user=" + username +\
        "&api_key=" + self.api_key + "&limit="+str(self.number_of_artists)
        return url

    def urlArtist(self, artist_name):
        url = self.base_url + "artist.getinfo&artist=" + artist_name +\
        "&api_key=" + self.api_key
        return url

    def fetch(self, user, number_of_artists=100):
        self.number_of_artists = number_of_artists
        req = urllib2.Request(self.url(user))
        response = urllib2.urlopen(req)
        xml_response = response.read()
        dom = parseString(xml_response)
        self.parseArtists(dom)

    def fetchArtist(self, artist):
        url = urllib.quote(self.urlArtist(artist), safe="%/:=&?~#+!$,;'@()*[]")
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        xml_response = response.read()
        dom = parseString(xml_response)
        return self.getArtist(dom, 0)

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
        artistData['name'] = artist.getElementsByTagName('name')[0].firstChild.nodeValue.encode('utf8')
        for image in artist.getElementsByTagName('image'):
            if image.getAttribute('size') == 'small':
                try:
                    artistData['thumbnail'] = image.firstChild.nodeValue
                except:
                    artistData['thumbnail'] = ''
            elif image.getAttribute('size') == 'medium':
                try:
                    artistData['image'] = image.firstChild.nodeValue
                except:
                    artistData['image'] = ''
            elif image.getAttribute('size') == 'large':
                try:
                    artistData['largeImage'] = image.firstChild.nodeValue
                except:
                    artistData['largeImage'] =  ''
        return artistData
