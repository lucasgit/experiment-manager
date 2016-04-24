'''
Created on Apr 22, 2016

@author: Lucas Lehnert (lucas.lehnert@mail.mcgill.ca)
'''

import json

config = {}

params = {}
params['-e'] = [500]
params['-i'] = [5000]
params['-a'] = [.1, .2, .3, .4, .5]

config['parameter'] = params
config['name'] = 'test'
config['script'] = 'test_experiment.py'
config['resultDir'] = '../experiment'
config['logDir'] = '../experiment'

with open( '../test.json', 'wb' ) as fp:
    json.dump( config, fp )
