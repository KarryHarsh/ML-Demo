# -*- coding: utf-8 -*-
"""
Created on Mon April  4 13:23:29 2020

@author: Karry Harsh
"""
from flask.views import MethodView
from MLApp.Core.CoreController import CoreController
from flask import request, jsonify

class Helloworld(MethodView, CoreController):
    """
       API to Print Hello World
    """

    def __init__(self):
        self.value = "hello World"
        CoreController.__init__(self)

    def post(self):
        try:
            #return jsonify({"message": self.value})
            return "hello World"
        except Exception as e:
            self._Logger.error("Error in printing hello world : {}".format(e))
            return jsonify({"message": "Invalid Request"})

