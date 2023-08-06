"""
Example using bootalchemy (if the model is within the same module)
"""
#from _yaml import ScannerError
from .bootalchemy.loader import Loader, YamlLoader
from odm2api.ODM2 import serviceBase
import odm2api.ODM2.models as models
import yaml
from collections import OrderedDict

from yaml.loader import Loader
from yaml import scanner
import re

import pprint

pp = pprint.PrettyPrinter(indent=8)

class YamlFunctions(object):
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.iteritems())

    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)

    def __init__(self, session, engine):
        self._session = session
        self._engine = engine

    def reconstructFile(self, values):
        anchor_pattern = r'(?<=- )(&\w*)\s?(?={.*})'
        alias_pattern = r'(\*[\w]*)'
        line_pattern = r"(?<=- )('&\w*')\s?({.*})"

        fixedAnchor = re.sub(anchor_pattern, r"'\1'", values)
        fixedAlias = re.sub(alias_pattern, r"'\1'", fixedAnchor)
        reconstructedFile = re.sub(line_pattern, r"{\1:\2}", fixedAlias)

        return reconstructedFile


        # pprint(reconstructedFile)

    def extractYaml(self, filename):
        file_values = open(filename).read()

        ## Reconstruct file to match boot alchemy's format
        reconstructed_values = self.reconstructFile(file_values)

        ## Load modified yaml file
        s = yaml.load(reconstructed_values)
        return s

    def loadFromFile(self, filename):
        """
        Open a yodaparser file to be loaded into the SQLAlchemy connection
        :filename: path to yaml file
        """
        self._session.autoflush = False
        s = self.extractYaml(filename)
        type = None
        if 'YODA' in s:
            print "<YODA Field FOUND! ... Manually removing it using 'dict.pop'> " \
                  "else it'll crash the program as sqlalchemy doesn't know what to do with it"
            s.pop('YODA')


        yl = YamlLoader(models)

        timeSeries = None
        if "TimeSeriesResultValues" in s:
            print "Found TimeSeriesResults"
            timeSeries = s.pop('TimeSeriesResultValues')

        references = yl.from_list(self._session, [s])

        # load the Time Series Result information
        self._session.flush()

        if timeSeries:
            ts_values = yl.loadTimeSeriesResults(timeSeries,  self._session, self._engine)


        # self._session.flush()
        self._session.commit()


    def loadFromFiles(self, files):
        """
        Load data from a list of yaml files
        """
        if not isinstance(files, list):
            files = [files]

        for item in files:
            self.loadFromFile(item)

    def writeValues(self, data, file_path):
        import os

        print "PWD: ", os.getcwd()
        with open(file_path, 'w') as outfile:
            outfile.write(yaml.dump(data, default_flow_style=True))

    def saveToDB(self):
        self._session.commit()

    def printValues(self, s):

        pp.pprint([s])

        for k, v in s.iteritems():
            print '-' * 45
            print k
            print '-' * 45
            for values in v:
                if isinstance(values, dict):
                    for item in values.iteritems():
                        print item
                    print

                elif isinstance(values, basestring):
                    print values












