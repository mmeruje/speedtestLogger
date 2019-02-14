#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    TODO:
        - A small front-end system to consult and filter the results;
        - Incremental tweaks such as:
            - Console parameter parsing to let the script be more or less verbose;
            - SpeedTesting on demand (API calls).

    NOTE: You'll need to install speedtest-cli and sqlalchemy .

"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
import json, time, speedtest

Base = declarative_base()

"""
    Configure the database connection (SQLite for now.)
"""
db_uri = "sqlite:///speedtestLogger.db"
engine =  create_engine(db_uri, convert_unicode=False)

"""
    Class definitions
"""
class Entry(Base):
    __tablename__ = 'st_entry'
    id             = Column(Integer, primary_key=True)
    bytes_sent     = Column(String(32))
    download       = Column(String(32))
    timestamp      = Column(String(32))
    share          = Column(String(128))
    bytes_received = Column(String(32))
    ping           = Column(String(32))
    upload         = Column(String(32))
    server         = relationship("Server", backref="st_entry")
    client         = relationship("Client", backref="st_entry")


class Client(Base):
    __tablename__ = 'st_client'
    id        = Column(Integer, primary_key=True)
    rating    = Column(String(32))
    loggedin  = Column(String(32))
    isprating = Column(String(32))
    ispdlavg  = Column(String(32))
    ip        = Column(String(32))
    isp       = Column(String(32))
    lon       = Column(String(32))
    ispulavg  = Column(String(32))
    country   = Column(String(32))
    lat       = Column(String(32))
    entryId   = Column(Integer, ForeignKey('st_entry.id'))


class Server(Base):
    __tablename__ = 'st_server'
    id      = Column(Integer, primary_key=True)
    latency = Column(String(32))
    name    = Column(String(32))
    url     = Column(String(128))
    country = Column(String(32))
    lon     = Column(String(32))
    cc      = Column(String(32))
    host    = Column(String(32))
    sponsor = Column(String(32))
    url2    = Column(String(128))
    lat     = Column(String(32))
    d       = Column(String(32))
    entryId = Column(Integer, ForeignKey('st_entry.id'))

metadata = MetaData(engine)
Base.metadata.create_all(engine)


"""
    Get data from speedtest(.net), using speedtest-cli
"""
s = speedtest.Speedtest()
print(" * Getting the best server...")
bestServer = s.get_best_server()
print(" * Best server: " + str(bestServer['sponsor']))
print("   Latency    : " + str(bestServer['latency']) + " ms")
print("   Name       : " + str(bestServer['name']))
print("   Country    : " + str(bestServer['country']))
print(" ")
print(" * Download testing...")
downloadVal = s.download()
print(" * Upload testing...")
uploadVal   = s.upload()
print(" ")
print(" * Results: ")
print("   Download: ~" + "%.2f Mbps" % (downloadVal/1000000)) # values are presented in bits, so:
print("   Upload  : ~" + "%.2f Mbps" % (uploadVal/1000000))   # 1 bit = 0,001 kbits = 0,000001 megabits
results = s.results.dict()
print("   Ping    : " + str(results['ping']) + " ms")
s.results.share()

client = results['client']
server = results['server']
entry  = results

# hum... url2 can be empty // please report if there are more fields that can be empty
server['url2'] = None if 'url2' not in server else server['url2']

"""
    Create entries
"""
try:
    timeId = str(int(round(time.time())))
    e1 = Entry( id=timeId ,bytes_sent=entry['bytes_sent'],download=entry['download'],timestamp=entry['timestamp'],share=entry['share'],bytes_received=entry['bytes_received'],ping=entry['ping'],upload=entry['upload'])
    c1 = Client(id=timeId ,rating=client['rating'],loggedin=client['loggedin'],isprating=client['isprating'],ispdlavg=client['ispdlavg'],ip=client['ip'],isp=client['isp'],lon=client['lon'],ispulavg=client['ispulavg'],country=client['country'],lat=client['lat'])
    e1.client.append(c1)
    s1 = Server(id=timeId ,latency=server['latency'],name=server['name'],url=server['url'],country=server['country'],lon=server['lon'],cc=server['cc'],host=server['host'],sponsor=server['sponsor'],url2=server['url2'],lat=server['lat'],d=server['d'])
    e1.server.append(s1)
except:
    print("SQLAlchemyError : An error has ocurred while trying to create the ORM class instance.")
    exit()

"""
    Write to the database
"""
try:
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add(e1)
    session.commit()
except SQLAlchemyError as e:
    print("SQLAlchemyError : An error has ocurred while trying to save the result.")
    exit()
finally:
    session.close()
    print(" * Finished: Everything went well.")






