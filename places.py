__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2020, Research Squirrel Engineers, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Florian Thiery"
__email__ = "rse@fthiery.de"
__status__ = "draft"

# import dependencies
import uuid
import pandas as pd
import os
import codecs
import datetime

# set paths
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path + "\\" + "query.csv"
file_out = dir_path + "\\" + "places.ttl"

# read csv file
data = pd.read_csv(
    file_in, # relative python path to subdirectory
    encoding='utf-8',
    sep=',', # deliminiter
    quotechar="'",  # single quote allowed as quote character
    usecols=['s', 'wkt'], # only load the  columns specified
    skiprows=0, # skip X rows of the file
    na_values=['.', '??'] # take any '.' or '??' values as NA
)

# create triples from dataframe
outStr = ""
lines = []
for index, row in data.iterrows():
    label = str(row['s']).replace("findspot:","")
    lines.append(str(row['s']) + " " + "geosparql:hasGeometry " + str(row['s']) + "_geom .")
    lines.append(str(row['s']) + "_geom " + "rdf:type" + " <http://www.opengis.net/ont/sf#the_geom> .")
    point = str(row['wkt'])
    point = "\"<http://www.opengis.net/def/crs/EPSG/0/4326> " + point + "\"^^geosparql:wktLiteral"
    lines.append(str(row['s']) + "_geom " + "geosparql:asWKT " + point + ".")
    lines.append("")

# write output file
file = codecs.open(file_out, "w", "utf-8")
file.write("# create triples from" + "\r\n")
file.write("# " + file_in + "\r\n")
file.write("# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n")
file.write("# by python script" + "\r\n\r\n")
prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\nPREFIX owl: <http://www.w3.org/2002/07/owl#> \r\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \r\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\nPREFIX geosparql: <http://www.opengis.net/ont/geosparql#>\r\n"
prefixes += "PREFIX findspot: <http://143.93.114.104/rest/samian/findspots/>\r\n"
prefixes += "\r\n"
file.write(prefixes)
for line in lines:
    file.write(line)
    file.write("\r\n")
file.close()
