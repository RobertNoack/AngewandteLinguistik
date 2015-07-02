import sys
import urllib
import urllib.parse
import urllib.request
import json

DOMAIN = 'http://api.geonames.org/'
USERNAME = 'asv2015' #username
MAPS = 'https://maps.google.de/maps?q='

class Location(object): 

	def __init__(self, name, lng, lat):
		self.name = name
		self.lng = lng
		self.lat = lat

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
		method = 'postalCodeSearchJSON'
		params = {'placename':city, 'username':USERNAME}
		results = Location.fetchJson(method, params)

		if('postalCodes' in results):
			if(len(results['postalCodes']) > 0):
				postalCode = results['postalCodes'][0]
				if ('placeName' in postalCode and 'lng' in postalCode and 'lat' in postalCode):
					return Location(postalCode['placeName'], postalCode['lng'], postalCode['lat'])
			else:
				if ' ' in city:
					for part in city.split(' '):
						return Location.getLocation(part)
						if(l is not None):
							return l

		return None

if __name__ == '__main__':
	if(len(sys.argv) > 0):
		l = Location.getLocation(sys.argv[len(sys.argv) - 1])
		if(l is None):
			print('Not found')
		else:
			print("name: " + l.getName() + " lng: " + str(l.getLng()) + " lat: " + str(l.getLat()) + " url: " + str(l.getUrl()))
	else:
		print('No location')
