import json, time, speedtest, threading, time
from models import Client, Server, Entry, DatabaseHelper

errors = {
    "ST_SPEEDT001" : "An Exception was raised: {0}. ({1})", # For specific Exceptions (i.e., SQLAlchemyError)
    "ST_SPEEDT002" : "An error ocurred: {0}. ({1})",        # for general Exceptions (i.e., Exceptions)
    "ST_SPEEDT003" : "An error has ocurred when trying to perform speedtest."
}

class SpeedTester():
    
    def __init__(self, interval=1):
        # a nice TODO: read a config file...
        # Auxiliary variables
        self.setIsRunning(False)
        self.performSpeedtestFlag = False
        self.dbHelper             = DatabaseHelper()
        self.stInterval           = 60 * 60          # each hour (60m * 60s), if 0, deactivate
                                                     # hourly check

        self.lastRunTime          = int(time.time()) # simply to avoid a "run upon start". 
                                                     # if you want to run as soon as the
                                                     # server is up, put 0 here
        # threading stuff:
        self.interval             = interval
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def executeSpeedtest(self):
        try:
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download()
            s.upload()
            s.results.share()
            return s.results.dict()
        except:
            raise Exception("ST_SPEEDT003")
    
    def sendResultToDatabase(self, data):
        try:
            entry  = data
            client = data['client']
            server = data['server']
             
            timeId         = str(int(round(time.time())))
            # "Sanitize" dictionaries
            bytes_sent     = entry['bytes_sent']     if 'bytes_sent'     in entry else ""
            download       = entry['download']       if 'download'       in entry else ""
            timestamp      = entry['timestamp']      if 'timestamp'      in entry else ""
            share          = entry['share']          if 'share'          in entry else ""
            bytes_received = entry['bytes_received'] if 'bytes_received' in entry else ""
            ping           = entry['ping']           if 'ping'           in entry else ""
            upload         = entry['upload']         if 'upload'         in entry else ""
             
            rating         = client['rating']        if 'rating'    in client else ""
            loggedin       = client['loggedin']      if 'loggedin'  in client else ""
            isprating      = client['isprating']     if 'isprating' in client else ""
            ispdlavg       = client['ispdlavg']      if 'ispdlavg'  in client else ""
            ip             = client['ip']            if 'ip'        in client else ""
            isp            = client['isp']           if 'isp'       in client else ""
            lon            = client['lon']           if 'lon'       in client else ""
            ispulavg       = client['ispulavg']      if 'ispulavg'  in client else ""
            country        = client['country']       if 'country'   in client else ""
            lat            = client['lat']           if 'lat'       in client else ""
            
            latency        = server['latency']       if 'latency'   in server else ""
            name           = server['name']          if 'name'      in server else ""
            url            = server['url']           if 'url'       in server else ""
            country        = server['country']       if 'country'   in server else ""
            lon            = server['lon']           if 'lon'       in server else ""
            cc             = server['cc']            if 'cc'        in server else ""
            host           = server['host']          if 'host'      in server else ""
            sponsor        = server['sponsor']       if 'sponsor'   in server else ""
            url2           = server['url2']          if 'url2'      in server else ""
            lat            = server['lat']           if 'lat'       in server else ""
            d              = server['d']             if 'd'         in server else ""
            
            # instantiate classes 
            e1 = Entry (id=timeId,bytes_sent=bytes_sent,download=download,
                timestamp=timestamp,share=share,bytes_received=bytes_received,
                ping=ping,upload=upload)
            #
            c1 = Client(id=timeId,rating=rating,loggedin=loggedin,isprating=isprating,
                ispdlavg=ispdlavg,ip=ip,isp=isp,lon=lon,ispulavg=ispulavg,
                country=country,lat=lat)
            #
            s1 = Server(id=timeId,latency=latency,name=name,url=url,country=country,
                lon=lon,cc=cc,host=host,sponsor=sponsor,url2=url2,lat=lat,d=d)
            
            # append client and server to entry
            e1.client.append(c1)
            e1.server.append(s1)
            
            # send to database 
            success = self.dbHelper.sendElementToDatabase(e1)
            
            if not success: 
                raise Exception("Something wrong happened.")
            else:
                return True
        except Exception as e :
            errorCode = 'ST_SPEEDT002'
            errorDesc = errors[errorCode].replace("{0}", e.args[0] ).replace("{1}", SpeedTester.sendResultToDatabase.__qualname__)
            return {errorCode, errorDesc}
    
        
    def setIsRunning(self, running):
        self.isRunning = running
    
    def getIsRunning(self, running):
        return self.isRunning 

    def getLastEntry(self):
        return self.dbHelper.getLastEntry()
    
    def performSpeedtest(self):
        if self.isRunning == False and self.performSpeedtestFlag == False:
            self.performSpeedtestFlag = True

    def run(self):
        while True:
            time.sleep(1)
            now = int(time.time())
            hourlyCheck = now > self.lastRunTime + self.stInterval if self.stInterval != 0 else False

            if hourlyCheck or (self.performSpeedtestFlag == True and  self.isRunning == False) :
                try:
                    self.setIsRunning(True)
                    self.performSpeedtestFlag = False
                    #
                    data = self.executeSpeedtest()
                    self.sendResultToDatabase(data)
                    #
                    self.lastRunTime = int(time.time())
                    self.setIsRunning(False)
                except:
                    self.setIsRunning(False)
            