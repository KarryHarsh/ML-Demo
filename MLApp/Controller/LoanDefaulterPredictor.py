"""
Created on Mon April  4 13:23:29 2020

@author: Karry Harsh
"""
from flask.views import MethodView
from MLApp.Core.CoreController import CoreController
from flask import request, jsonify
from pkg_resources import resource_filename

#from MLApp.DataStore.Store import DBStore
from MLApp.MLModel.LoanDefaulter.Defaulterpredict import Defaultpredict
from MLApp.Utils.Utils import APIresponse, pickleload
import pandas as pd
import mlflow
from sklearn.preprocessing import LabelEncoder
from MLApp.MLModel.LoanDefaulter import Defaulterpredict
import numpy as np

class LoanDefaultPredictor(MethodView,Defaultpredict):
    """
       API to Predict Loan Defaulter
    """

    def __init__(self):
        Defaultpredict.__init__(self)


    def post(self):
        """
        Post Method to predict loan defaulter prediction
        :return:
        """
        try:
            if request.is_json ==True:
                inputs = request.json
                member_id = inputs["memberid"]
                data = inputs["data"]

                if data == "" or member_id == "":
                    response = APIresponse(StatusCode=405, Message="Incorrect Input format", result='NA')
                    return response

                df = pd.DataFrame(data)
                model = Defaultpredict()
                prediction = model.predict(df)


                output = pd.DataFrame({"prediction":prediction})

                result = output.to_dict(orient="records")
                response = APIresponse(StatusCode=200, Message="Success", result=result)
                return response

        except Exception as e:
            self._Logger.error("Error in fetching Region details : {}".format(e))
            return jsonify({"message": "Invalid Request"})
