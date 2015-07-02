import sys
import urllib
import urllib.parse
import urllib.request
import json
import collections

DOMAIN = 'http://api.geonames.org/'
USERNAME = 'asv2015' #username
MAPS = 'https://maps.google.de/maps?q='

class Location(object): 

	def __init__(self, geonameId, name, lng, lat):
		self.geonameId = geonameId
		self.name = name
		self.lng = lng
		self.lat = lat

	locationCache = collections.OrderedDict()

	def getGeonameId(self):
		return self.geonameId

	def getName(self):
		return self.name

	def getLng(self):
		return self.lng

	def getLat(self):
		return self.lat

	def getUrl(self):
		return MAPS + str(self.lat) + ',' + str(self.lng)

	def fetchJson(method, params):
		uri = DOMAIN + '%s?%s' % (method, urllib.parse.urlencode(params))
		response = urllib.request.urlopen(uri)
		content = response.read()
		js = json.loads(content.decode("utf8"))
		return js

	def getLocation(city):
		if city in Location.locationCache:
			return Location.locationCache[city]
		else:
			method = 'searchJSON'
			params = {'q':city, 'maxRows':1, 'username':USERNAME}
			try:
				results = Location.fetchJson(method, params)
				if('totalResultsCount' in results):
					if(results['totalResultsCount'] > 0):
						geoname = results['geonames'][0]
						if ('geonameId' in geoname and 'name' in geoname and 'lng' in geoname and 'lat' in geoname):
							loc = Location(geoname['geonameId'], geoname['name'], geoname['lng'], geoname['lat'])
							Location.locationCache[city] = loc
							return loc
					else:
						if ' ' in city:
							for part in city.split(' '):
								return Location.getLocation(part)
								if(l is not None):
									return l
				
			except urllib.error.HTTPError:
				print('cityParseError (' + city + ')')
		return None

if __name__ == '__main__':
	if(len(sys.argv) > 0):
		l = Location.getLocation(sys.argv[len(sys.argv) - 1])
		if(l is None):
			print('Not found')
		else:
			print("geonameId:" + str(l.getGeonameId()) + " name: " + l.getName() + " lng: " + str(l.getLng()) + " lat: " + str(l.getLat()) + " url: " + str(l.getUrl()))
	else:
		print('No location')
