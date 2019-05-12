from SpeedTesterModule import SpeedTester
import json, falcon 

errors = {
    "ST_APIH000" : "Fatal error. {1}",
    "ST_APIH001" : "An exception was raised: {0}. {1}",
    "ST_APIH002" : "A speedtest is already running. Please wait for the result."
}

class SpeedTestDataAPIHandler:
    
    def __init__(self):
        self.stInstance = SpeedTester()
        self.dbHelper = self.stInstance.dbHelper
    
    def on_get(self, req, resp):
        """
            GET request handler. 
            TODO: filter request.

            Right now is returning the last entry that was inserted on the database.
        """
        lastEntry = self.dbHelper.getLastEntry()
        resp.status = falcon.HTTP_200
        resp.media = lastEntry
        return resp

    def on_post(self, req, resp):
        """
            POST request handler
            
            POST will perform a speedtest.
            If a speedtest is already being performed, it will return a HTTP 400.
        """
        status = "OK"
        #
        if self.stInstance.isRunning == True or self.stInstance.performSpeedtestFlag == True:
            errorCode   = 'ST_APIH002'
            errorDesc   = errors[errorCode].replace("{0}", SpeedTestDataAPIHandler.on_post.__qualname__) if errorCode in errors else errors['ST_APIH000']
            #
            status = "NOK"
            resp.status = falcon.HTTP_400
            resp.media  = {
                "status" : status,
                errorCode : errorDesc
            }
            return resp
        self.stInstance.performSpeedtest()
        resp.status = falcon.HTTP_200
        resp.media  = {
            "status": status,
            "data"  : {

            }
        }
        return resp
    
    def on_patch(self, req, resp):
        """
            PATCH request handler

            PATCH will be used as the hourly speedtest switch (ON/OFF)
        """
        if self.stInstance.stInterval != 0:
            self.stInstance.stInterval = 0
        else:
             self.stInstance.stInterval = 60*60
        #
        nextRun = self.stInstance.lastRunTime + self.stInstance.stInterval if self.stInstance.stInterval != 0 else None
        #
        resp.status = falcon.HTTP_200
        resp.media  = {
            "status": "OK",
            "data"  : {
                    "interval" : str(self.stInstance.stInterval),
                    "nextRun"  : str(nextRun) if nextRun != None else "N/A"
                 }
            }
        return resp