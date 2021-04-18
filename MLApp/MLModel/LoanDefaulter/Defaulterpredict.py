# -*- coding: utf-8 -*-
"""
Created on Mon April  18 13:23:29 2021

@author: Karry Harsh
"""

from MLApp.Core.CoreController import CoreController
#from MLApp.DataStore.Store import DBStore
from pkg_resources import resource_filename
from MLApp.Utils.Utils import APIresponse, pickleload


import pandas as pd
import numpy as np

class Defaultpredict(CoreController):
    """
        Model Infrencing for loan defaulter prediction:
        """
    def __init__(self):
        CoreController.__init__(self)
        # self.df = df
#        self._dbSession = DBStore.getInstance()

        self.selected_feature = self._ConfigParser.GetSettingValue(
            "LoanDefaulter", "Selected_feature"
        )
        self.employ_len_dict = self._ConfigParser.GetSettingValue(
            "LoanDefaulter", "Employ_len_Dict"
        )
        self.Mean_var_dict = self._ConfigParser.GetSettingValue(
            "LoanDefaulter", "Mean_var_dict"
        )
        self.FrequentLabels = self._ConfigParser.GetSettingValue(
            "LoanDefaulter", "FrequentLabels"
        )
        self.Encoderlabel = self._ConfigParser.GetSettingValue(
            "LoanDefaulter", "labelEncoder"
        )
        self.modelfile = self._ConfigParser.GetSettingValue(
            "LoanDefaulter", "modelfile"
        )
        self.feature_selected = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/" + self.selected_feature
        )
        self.dict_employ_len = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/" + self.employ_len_dict
        )
        self.dict_Mean_var = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/" + self.Mean_var_dict
        )
        self.Freqlabels = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/" + self.FrequentLabels
        )
        self.labelEncoder = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/" + self.Encoderlabel
        )
        self.model = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/model/" + self.modelfile
        )
        self.classes = resource_filename(
            "MLApp", "MLModel/LoanDefaulter/artifacts/" + "classes.npy"
        )

    def featureselection(self, df):
        """
                Select features from all the input data
                :param df: raw input data with all values.
                :return: dataframe with selected features
                """
        try:
            # converting blank value to NaN value.
            df = df.replace(' ', np.nan)
            df["Long_emp_length"] = ""  # adding additional feature col.

            # loading list of features
            features = pd.read_csv(self.feature_selected)
            self.features = [x for x in features["0"]]
            df = df[self.features]
            return df
        except Exception as e:
            self._Logger.error("Error in Feature Selection: {}".format(e))

    def featureprepare(self,df):
        """
        Prepare feature for model infrencing.
        :param df: selected feature for dataframe
        :return: dataframe with selected features
        """
        try:
            df = self.featureselection(df)
            emp_len_dict= pickleload(self.dict_employ_len) # Load emp len
            df['emp_length'] = df['emp_length'].map(emp_len_dict)
            df['Long_emp_length'] = df['emp_length'].apply(lambda x: 'Yes' if x == 10 else 'No') # creating new feature
            df["emp_title"].fillna('Missing', inplace=True)

            # Handling missing numerical value
            dict_Mean_var = pickleload(self.dict_Mean_var)
            for col, mean_val in dict_Mean_var.items():
                df[col].fillna(mean_val, inplace=True)

            # Handling rare values
            Freqlabels = pickleload(self.Freqlabels)
            for variable, frequent_labels in Freqlabels.items():
                df[variable] = np.where(df[variable].isin(frequent_labels), df[variable], 'Rare')

            # Encoding Categorical features
            x = pickleload(self.labelEncoder)
            for features, labels in x.items():
                df.loc[:, features] = labels.transform(df.loc[:, features])
            return df
        except Exception as e:
            self._Logger.error("Error in feature preparation: {}".format(e))

    def predict(self,df):
        """
        model Infrencing
        :param df: feature prepare for dataframe
        :return: predicted values
                """
        df = self.featureprepare(df)
        model = pickleload(self.model)
        prediction = model.predict(df)
        return prediction




