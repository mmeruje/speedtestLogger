from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, MetaData, Table


Base = declarative_base()

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
    def __repr__(self):
        return str(self.id)


class Server(Base):
    __tablename__ = 'st_server'
    id        = Column(Integer, primary_key=True)
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
    def __repr__(self):
        return '<Id %r>' % (self.id)


class Entry(Base):
    __tablename__ = 'st_entry'
    id        = Column(Integer, primary_key=True)
    bytes_sent     = Column(String(32))
    download       = Column(String(32))
    timestamp      = Column(String(32))
    share          = Column(String(32))
    bytes_received = Column(String(32))
    ping           = Column(String(32))
    upload         = Column(String(32))
    server         = relationship("Server", backref="st_entry")
    client         = relationship("Client", backref="st_entry")
    def __repr__(self):
        return '<Id %r>' % (self.id)
    
    def sendToDatabase(self):
        try:
            Session = sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            session.add(self)
            session.commit()
            session.close()
        except SQLAlchemyError as e:
            raise Exception(repr(e))
        finally:
            return True


class Log(Base):
    __tablename__ = 'st_log'
    id      = Column(Integer, primary_key=True)
    entryId = Column(Integer)
    message = Column(String(1024))
 

db_uri = "sqlite:///speedtest.db"
engine =  create_engine(db_uri, convert_unicode=False)
metadata = MetaData(engine)
Base.metadata.create_all(engine)