# -*- coding: utf-8 -*-
"""
Created on Wed April  14 23:07:19 2021

@author: Karry Harsh
"""
import os
import sys
import logging.config
from pkg_resources import resource_filename  # @UnresolvedImport

from MLApp.Core.CoreController import CoreController
from MLApp.Controller.BaseController import BaseController


from sys import exit

class MLApps(CoreController):

    def __init__(self):
        super(MLApps, self).__init__()
        #Load MLAppconfig file
        configFilePath = resource_filename('MLApp', 'Conf/MLApp.conf')
        self._ConfigParser.LoadConfigFile(configFilePath)
        # Load MLModel config file 
        MLconfigFilePath = resource_filename('MLApp', 'Conf/MLModel.conf')
        self._ConfigParser.LoadConfigFile(MLconfigFilePath)
        # Retrieve working folder path
        workingFolderPathStr = self._ConfigParser.GetSettingValue('General', 'WorkingFolderPath')
        self._WorkingFolderPath = os.path.abspath(os.path.expandvars(os.path.expanduser(workingFolderPathStr)))
        #print (self._WorkingFolderPath)
        
        #Configure logging
        self._ConfigureLogging()
        
        #Instantiate base controller to get server details and run API
        self._BaseController = BaseController.getInstance()

    def _ConfigureLogging(self):
        logConfigFilePath = resource_filename('MLApp', 'Conf/MLAppLogging.conf')
        #Get log details
        logsFolderPathStr = self._ConfigParser.GetSettingValue('Logging', 'LogsFolderPath')
        
        logsFolderPath = os.path.abspath(os.path.expandvars(os.path.expanduser(logsFolderPathStr)))
        #print (logsFolderPath)
        if not os.path.exists(logsFolderPath):
            os.makedirs(logsFolderPath)

        logFileName = self._ConfigParser.GetSettingValue('Logging', 'LogFileName')

        logFilePath = os.path.join(logsFolderPath, logFileName)
        logging.config.fileConfig(logConfigFilePath, {'logFilePath' : ("%r" % logFilePath)}, False)

    def RunApp(self, argv):
        return self._BaseController.RunApp()

def main():
    argv = sys.argv[1:]

    mlapp = MLApps()
    try:
        mlapp.RunApp(argv)
       # mlapp.RunApp()
    except (KeyboardInterrupt, SystemExit):
        exit(0)

if __name__ == '__main__':
    main()