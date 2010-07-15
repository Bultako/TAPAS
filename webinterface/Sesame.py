""" Sesame class to handle Sesame name revolver service
	Created 2005-06-11 by Shui Hung Kwok
	See http://cdsweb.u-strasbg.fr/doc/sesame.htx
"""

from urllib import *
from urlparse import *
import VOTable
import xml.sax
import xml.sax.handler
import sys

SesameURL = "http://vizier.u-strasbg.fr/viz-bin/nph-sesame" 

class Sesame (object):
	CatalogOpt = "SNV" # S simbad, N ned, V vizier, A All
	OutputOpt = "-oxp" # xp for xml as text/plain rather then text/xml (-ox)

	def __init__ (self, urn=SesameURL, opt=CatalogOpt, opt1=OutputOpt):
		"""	Initializes Sesame URL and options
		"""
		self.urn = urn
		self.catOpt = opt
		self.outOpt = opt1
		# Sesame

	def buildQuery (self, name, all=True):
		"""	Builds query URL for use with HTTP GET
			If all is true, then all known identifiers shall be returned.
		"""
		opt = self.catOpt
		opt1 = self.outOpt
		if all:
			opt += 'A'
			opt1 += 'I' # all idendifiers
		queryURL = "%s/%s/%s?%s" % (self.urn, opt1, opt, quote (name))
		return queryURL

	def resolveRaw (self, name, all=True):
		""" Performs a raw query.
			Returns what the server returns.
		"""
		query = self.buildQuery (name, all)
		print "query=", query
		hcon = urlopen (query)
		res = hcon.read ()
		hcon.close ()
		return res
	
	def resolve (self, name, all=True):
		"""	Performs a query.
			Extracts the ra and dec from the results.
		"""
		query = self.buildQuery (name, all)
		self.xml = xml = VOTable.VOTable (query)
		self.getCoord ()
		return (self.ra, self.dec)

	def getCoord (self):
		"""	Helper method to extract ra and dec from XML.
		"""
		resolvers = self.xml.root.Sesame.Target.Resolver
		for r in resolvers:
			try:
				self.ra = float (r.jradeg.content)
				self.dec = float (r.jdedeg.content)
				return
			except Exception, e1:
				try:
					self.ra = float (r.jradeg[0].content)
					self.dec = float (r.jdedeg[0].content)
					return
				except Exception, e2:
					pass
		else:
			raise Exception, "no ra/dec found"
		# getCoord

	def getAliases (self):
		"""	Extracts aliases for the given target.
			Returns a list of names.
		"""
		res = []
		for resolver in self.xml.root.Sesame.Target.Resolver:
			try:
				for a in resolver.alias:
					res.append (a.content)
			except:
				pass
		return res

def resolveName (name):
	""" Convenient method.
		Returns (ra,dec) as tuple.
	"""	
	if not name:
		return
	sesame = Sesame ()
	sesame.resolve (name)
	return (sesame.ra, sesame.dec)

if __name__ == "__main__":
	sesame = Sesame ()
	print sesame.resolveRaw (sys.argv[1])
	#print ', '.join (sesame.getAliases ())
	#print "%s, %s" % (sesame.ra, sesame.dec)
	#print "RA=%f, DEC=%f" % resolveName (sys.argv[1])

