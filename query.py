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
    {?observation sosa:hasSimpleResult ?hasSimpleResult}

    {?observation sosa:resultTime ?resultTime.}
}
ORDER BY ?resultTime
''')

for row in qres:
    print("%s %s" % row)