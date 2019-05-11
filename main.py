import json, time, speedtest
from models import Client, Server, Entry


def performSpeedtest():
    try:
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        s.results.share()
        return s.results.dict()
    except:
        raise Exception("An error has ocurred when trying to perform speedtest.")

        
def sendResultToDatabase(data):
    try:
        client = data['client']
        server = data['server']
        entry  = data

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
        e1 = Entry (id=timeId,bytes_sent=bytes_sent,download=download,timestamp=timestamp,share=share,bytes_received=bytes_received,ping=ping,upload=upload)
        c1 = Client(id=timeId,rating=rating,loggedin=loggedin,isprating=isprating,ispdlavg=ispdlavg,ip=ip,isp=isp,lon=lon,ispulavg=ispulavg,country=country,lat=lat)
        s1 = Server(id=timeId,latency=latency,name=name,url=url,country=country,lon=lon,cc=cc,host=host,sponsor=sponsor,url2=url2,lat=lat,d=d)

        # append client and server to entry
        e1.client.append(c1)
        e1.server.append(s1)
        
        # send to database and 
        success = e1.sendToDatabase()

        if not success : 
            raise Exception("Something wrong happened.")
        else:
            return True
    except Exception as e:
        print(repr(e))
        exit()



if __name__ == "__main__":
    try:
        data   = performSpeedtest()
        result = sendResultToDatabase(data)
    except Exception as e:
        print(repr(e))


