import sys
import urllib
import urllib.parse
import urllib.request
import simplejson as json
DOMAIN = 'http://api.geonames.org/'
USERNAME = 'asv2015' #username

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

def fetchJson(method, params):
	uri = DOMAIN + '%s?%s' % (method, urllib.parse.urlencode(params))
	resource = urllib.request.urlopen(uri).readlines()
	js = json.loads(resource[0])
	return js

def getLocation(city):
	method = 'postalCodeSearchJSON'
	params = {'placename':city, 'username':USERNAME}
	results = fetchJson(method, params)

	if('postalCodes' in results):
		if(len(results['postalCodes']) > 0):
			postalCode = results['postalCodes'][0]
			if ('placeName' in postalCode and 'lng' in postalCode and 'lat' in postalCode):
				return Location(postalCode['placeName'], postalCode['lng'], postalCode['lat'])

	return None

if __name__ == '__main__':
	l = getLocation('Leipzig')
	if(l is None):
		print('Not found')
	else:
		print("name: " + l.getName() + " lng: " + str(l.getLng()) + " lat: " + str(l.getLat()))
