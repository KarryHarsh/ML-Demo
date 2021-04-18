# -*- coding: utf-8 -*-
"""
Created on Wed April 29 23:07:19 2020

@author: sanbiswa
"""
from logging import getLogger
from configparser import ConfigParser
from MLApp.Core.SingletonMixin import Singleton

class ConfigManager(Singleton):

    def __init__(self):
        self._SettingsParser = ConfigParser()
        self._SettingsParser.optionxform = str
    
    #Load config
    def LoadConfigFile(self, configFilePath):
        self._SettingsParser.read(configFilePath)

    #Read config
    def GetSettingValue(self, sectionName, settingName):
        return self._SettingsParser.get(sectionName, settingName)


class CoreController(object):

    def __init__(self):
        super(CoreController, self).__init__()
        self._Logger = getLogger(type(self).__module__) #create object of Logger
        self._ConfigParser = ConfigManager.getInstance() #getInstance used to instantiate singleton class