# -*- coding: utf-8 -*-
"""
Created on Mon May  4 11:37:19 2020

@author: sanbiswa
"""
from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from MLApp.Controller.LoanDefaulterPredictor import LoanDefaultPredictor
from MLApp.Controller.hello_world import Helloworld
from MLApp.Core.SingletonMixin import Singleton
from MLApp.Core.CoreController import CoreController


class BaseController(CoreController, Singleton):

    def __init__(self):
        CoreController.__init__(self)

        self._RestApp = Flask(__name__)
        #Get URLprefix details
        self._RestServerURLPrefix = self._ConfigParser.GetSettingValue('Server', 'URLPrefix')

    def RunApp(self):
        self._RestApp.config['APPLICATION_ROOT'] = self._RestServerURLPrefix
        
        CORS(self._RestApp)
        
        self._RegisterResources() # Call defined function for registering url
        #Get server details
        restServerHost = self._ConfigParser.GetSettingValue('Server', 'Host')
        restServerPort = int(self._ConfigParser.GetSettingValue('Server', 'Port'))
        debugMode = eval(self._ConfigParser.GetSettingValue('Server', 'Debug'))
        
        if debugMode:
            self._RestApp.run(host=restServerHost, port=restServerPort, debug=debugMode)
        else:
            #create webserver getway interface
            self._ServerObj = WSGIServer((restServerHost, restServerPort), self._RestApp)
            self._Logger.info('Running on http://{}:{}/ (Press CTRL+C to quit)'.format(restServerHost, restServerPort))
            self._ServerObj.serve_forever()

    def _RegisterResources(self):
        self._Logger.debug('Registering URLS')
        resources = [
                    #(self._RestServerURLPrefix + '/Intellimap/English/AutoincidentUsecasePrediction/', AutoIncUCPred().as_view('AutoIncUCPred'), ['POST']), ###include ur api simillar to this
                    #(self._RestServerURLPrefix + '/Intellimap/checkuser/', UserController().as_view('UserController'), ['POST']) ###include ur api simillar to this
                    (self._RestServerURLPrefix + '/hello',
                     Helloworld().as_view('hello_world'), ['POST']),
                    (self._RestServerURLPrefix + '/loandefaulter',
                     LoanDefaultPredictor().as_view('LoanDefaultPredictor'), ['POST'])
                   
                    ]
        # For All resources,set the url,function,type of call
        for resource in resources:
            #print('>>>>>>>>>>>>>>>')
            #print(resource)
            self._RestApp.add_url_rule((resource[0]), view_func=(resource[1]))