import rdflib
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME
from rdflib import Namespace


g = Graph()
g.parse("pressure.ttl", format="turtle")

# query the graph 
qres = g.query('''
SELECT DISTINCT ?hasSimpleResult ?resultTime
WHERE {
    sosa:hasSimpleResult ?hasSimpleResult & sosa:resultTime ?resultTim
}
order by asc(?resultTime)
 
''')

print(qres)

