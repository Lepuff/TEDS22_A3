import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME
from rdflib import Namespace
from rdflib import Graph, Literal, URIRef
messages = []
messagescount = 0



# define the rdf graph
# namespaces

g = Graph()
g.bind("sosa", SOSA)
g.bind("time", TIME)
g.bind("xsd", XSD)
g.bind("rdfs", RDFS)
g.bind("rdf", RDF)

g.bind("qudt-1-1", Namespace("http://qudt.org/1.1/schema/qudt#"))
g.bind("qudt-unit-1-1", Namespace("http://qudt.org/1.1/vocab/quantity#"))
g.bind("cdt", Namespace("http://w3id.org/lindt/custom_datatypes#"))
base = Namespace("http://example.org/data/")
g.bind("base", base)

#types

earthAtmosphere = base['earthAtmosphere']
g.add((earthAtmosphere,RDF.type, SOSA.FeatureOfInterest))
g.add((earthAtmosphere, RDFS.label, Literal("Earth Atmosphere", lang="en")))

sensor_atmospheric_pressure = base['sensor_atmospheric_pressure']

sensor_bmp282 = base['sensor_bmp282']
g.add((sensor_bmp282, RDF.type, SOSA.Sensor))
g.add((sensor_bmp282, RDFS.label, Literal("Bosch Sensortec BMP282", lang="en")))
g.add((sensor_bmp282,SOSA.observes,sensor_atmospheric_pressure))

iphone = base['iphone']
g.add((iphone, RDF.type ,SOSA.Platform))
g.add((iphone, RDFS.label,Literal("iPhone", lang="en")))
g.add((iphone,RDFS.comment,Literal("Apple iPhone 7", lang="en")))
g.add((iphone, SOSA.hosts, sensor_bmp282))





print(g.serialize(format='ttl'))