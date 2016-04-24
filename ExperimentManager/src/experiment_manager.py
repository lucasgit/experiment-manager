#!/usr/bin/env python
'''
Created on Apr 24, 2016

@author: Lucas Lehnert (lucas.lehnert@mail.mcgill.ca)
'''

import subprocess
import json
from math import ceil

class Job:

    def __init__( self, **params ):
        if params.has_key( 'fromDictionary' ):
            params = params['fromDictionary']

        self.__jobName = params['jobName']
        self.__script = params['script']
        self.__resultFile = params['resultFile']
        self.__logFile = params['logFile']
        self.__parameterDict = params['parameter']

    def bashCmd( self, withLogRedirect=False ):
        cmd = ['python', self.__script]
        for ( flag, value ) in self.__parameterDict.items():
            cmd += [flag, str( value )]
        cmd += ['-r', self.__resultFile]
        if withLogRedirect:
            cmd += ['>', self.__logFile, '2>&1']
        return cmd

    def getJobName( self ):
        return self.__jobName

    def getLogFile( self ):
        return self.__logFile

    def toDictionary( self ):
        return {'jobName' : self.__jobName, 'script' : self.__script, 'resultFile' : self.__resultFile, \
                'logFile' : self.__logFile, 'parameter' : self.__parameterDict }

class Experiment:

    def __init__( self, **params ):
        if params.has_key( 'fromDictionary' ):
            params = params['fromDictionary']
            self.__jobList = []
            for p in params:
                self.__jobList.append( Job( fromDictionary=p ) )
        else:
            experimentName = params['name']
            script = params['script']
            resultFileDirectory = params['resultFileDirectory']
            logFileDirectory = params['logFileDirectiory']
            parameter = params['parameter']

            from sklearn.grid_search import ParameterGrid
            parameter = list( ParameterGrid( parameter ) )

            self.__jobList = []
            for i in range( len( parameter ) ):
                jobName = experimentName + ( '_%04d' % i )
                resultFile = resultFileDirectory + '/' + jobName + '.json'
                logFile = logFileDirectory + '/' + jobName + '.out'
                self.__jobList.append( Job( jobName=jobName, script=script, resultFile=resultFile, \
                                            logFile=logFile, parameter=parameter[i] ) )

    def runBashJobs( self, jobsPerProcess=1 ):
        print 'job indices: ' + str( range( 0, len( self.__jobList ), jobsPerProcess ) )
        for i in range( 0, len( self.__jobList ), jobsPerProcess ):
            jobNames = []
            jobCmds = ''
#            print 'grp indices: ' + str( range( i, min( i + jobsPerProcess, len( self.__jobList ) ) ) )
            for j in range( i, min( i + jobsPerProcess, len( self.__jobList ) ) ):
                jobNames.append( self.__jobList[j].getJobName() )
                jobCmds += ' '.join( self.__jobList[j].bashCmd( withLogRedirect=True ) ) + ';'
#            jobCmds += '\''
            print 'Launching ' + ', '.join( jobNames ) + ' ... ',
            subprocess.Popen( ['bash', '-c', jobCmds], shell=False )
            print 'done'

    def getNumberOfJobs( self ):
        return len( self.__jobList )

    def toDictionary( self ):
        return map( lambda j : j.toDictionary(), self.__jobList )

def createExperiment( experimentConf, parameterDict, name=None, script=None, resultDir=None, logDir=None ):
    if parameterDict.has_key( 'parameter' ):
        parameter = parameterDict['parameter']

        if name == None:
            name = parameterDict['name']
        if script == None:
            script = parameterDict['script']
        if resultDir == None:
            resultDir = parameterDict['resultDir']
        if logDir == None:
            logDir = parameterDict['logDir']

    else:
        parameter = parameterDict

    exp = Experiment( name=name, script=script, resultFileDirectory=resultDir, \
                      logFileDirectiory=logDir, parameter=parameter )
    with open( experimentConf, 'wb' ) as fp:
        json.dump( exp.toDictionary(), fp )

    print 'Created ' + str( exp.getNumberOfJobs() ) + ' jobs.'

def launchExperiment( experimentConf, numberOfJobs=None ):
    with open( experimentConf, 'r' ) as fp:
        params = json.load( fp )
        exp = Experiment( fromDictionary=params )
        if numberOfJobs is None:
            jobsPerProcess = 1
        else:
            jobsPerProcess = int( ceil( float( exp.getNumberOfJobs() ) / float( numberOfJobs ) ) )

        print 'Launching ' + str( exp.getNumberOfJobs() ) + ' jobs on ' + str( numberOfJobs ) + ' processes.'
        print 'Launching ' + str( jobsPerProcess ) + ' jobs per process.'

        exp.runBashJobs( jobsPerProcess )

        print 'Done'


def main():
    import argparse
    parser = argparse.ArgumentParser( description='Experiment Launcher', \
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument( 'action', type=str, \
                         help='Can be create or launch for creating or launching an experiment.' )
    parser.add_argument( '-e', '--experiment', type=str, help='Experiment file name or path.' )
    parser.add_argument( '-c', '--experimentConf', type=str, help='Experiment configuration file name or path.' )
    parser.add_argument( '-n', '--name', type=str, default=None, help='Name of the experiment.' )
    parser.add_argument( '-s', '--script', type=str, default=None, help='Name of the script that is launched.' )
    parser.add_argument( '-r', '--resultDir', type=str, default=None, help='Name of the result directory.' )
    parser.add_argument( '-l', '--logDir', type=str, default=None, help='Name of the log directory.' )

    parser.add_argument( '-j', '--jobs', type=int, help='Number of jobs that should be submitted.' )

    args = parser.parse_args()

    experimentFile = args.experiment

    if args.action == 'create':
        with open( args.experimentConf, 'r' ) as fp:
            params = json.load( fp )
            createExperiment( experimentFile, params, name=args.name, script=args.script, \
                              resultDir=args.resultDir, logDir=args.logDir )
    elif args.action == 'launch':
        numberOfJobs = args.jobs
        launchExperiment( experimentFile, numberOfJobs )
    else:
        raise Exception( 'Unrecognized action command ' + str( args.action ) )


if __name__ == '__main__':
    main()
    pass
