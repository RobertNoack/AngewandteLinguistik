import collections, re
import geonames

class Certificate(object): 

	def __init__(self, source):
		self.source = source

	def getSource(self):
		return self.source

	def getName(self):
		if(hasattr(self, 'name')):
			return self.name
		else:
			return None

	def setName(self, name):
		self.name = name

	def getYear(self):
		if(hasattr(self, 'year')):
			return self.year
		else:
			return None

	def setYear(self, year):
		self.year = year

	def getLocation(self):
		if(hasattr(self, 'location')):
			return self.location
		else:
			return None

	def setLocation(self, location):
		self.location = location

	def getType(self):
		if(hasattr(self, 'type')):
			return self.type
		else:
			return None

	def setType(self, t):
		self.type = t

	def getCertificates(value):
		certificates = []
		for part in value.split(','):
			cert = Certificate(part)

			if(';' in part):
				part = part[:part.find(';')]

			match = re.match(r'.*(\d{4}([/]\d{2})*).*', part)

			if match:
				cert.setYear(match.group(1))
				part = part.replace(match.group(1), '')

			part = part.replace('.', '').strip()

			if(' ' in part):
				temp = part.split(' ')
				temp = temp[len(temp) - 1]
				if(len(temp) > 3):
					loc = geonames.Location.getLocation(temp)
					if(loc is not None):
						#print(part + ' => ' + loc.getName() + '\ttmp:' + temp )
						cert.setLocation(loc)
			
			temp = part.lower()
			if 'zeugnis' in temp:
				cert.setType('Zeugnis')
			elif 'buch' in temp:
				cert.setType('Buch')
			elif 'schein' in temp:
				cert.setType('Schein')
			elif 'protokoll' in temp:
				cert.setType('Protokoll')
			elif 'genehmigung' in temp:
				cert.setType('Genehmigung')
			elif 'zuweisung' in temp:
				cert.setType('Zuweisung')
			elif 'diplom' in temp:
				cert.setType('Diplom')
			elif 'quittung' in temp:
				cert.setType('Quittung')

			cert.setName(part)

			certificates.append(cert)

		return certificates
		
