from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, MetaData, Table, func, distinct, inspect

Base = declarative_base()

errors = {
    "ST_MODELS001" : "An Exception was raised: {0}. ({1})", # For specific Exceptions (i.e., SQLAlchemyError)
    "ST_MODELS002" : "An error ocurred: {0}. ({1})",        # for general Exceptions (i.e., Exceptions)
    "ST_MODELS003" : "There are no entries on the database."
}

def to_dict(obj):
    try:
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
    except Exception as e:
        errorCode = 'ST_MODELS002'
        errorDesc = errors[errorCode].replace("{0}", repr(e)).replace("{1}", Entry.to_dict.__qualname__)
        return {errorCode: errorDesc}


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
        return '<Id %r>' % (self.id)


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
    


class DatabaseHelper:
    def sendElementToDatabase(self, element):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(element) # this shoud be a class instance Entry
            session.commit()
            session.close()
        except SQLAlchemyError as e:
            errorCode = 'ST_MODELS001'
            errorDesc = errors[errorCode].replace("{0}", repr(e)).replace("{1}", DatabaseHelper.sendElementToDatabase.__qualname__)
            return {errorCode: errorDesc}
        except Exception as e:
            errorCode = 'ST_MODELS002'
            errorDesc = errors[errorCode].replace("{0}", repr(e)).replace("{1}", DatabaseHelper.sendElementToDatabase.__qualname__)
            return {errorCode: errorDesc}
        return True

    def getLastEntry(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            # get entries
            entry  = session.query(Entry).order_by(Entry.id.desc()).first()
            if entry == None:
                raise Exception("ST_MODELS003") 
            client = session.query(Client).get(entry.id)
            server = session.query(Server).get(entry.id)
            # turn into python objects
            dict_entry = to_dict(entry)
            dict_entry['client'] = to_dict(client)
            dict_entry['server'] = to_dict(server)
            # close session
            session.close()
            return dict_entry
        except SQLAlchemyError as e:
            errorCode = 'ST_MODELS001'
            errorDesc = errors[errorCode].replace("{0}", repr(e)).replace("{1}", DatabaseHelper.getLastEntry.__qualname__)
            return {errorCode: errorDesc}
        except Exception as e:
            errorCode = e.args[0] if len(e.args) > 0 else 'ST_MODELS002'
            errorDesc = errors[errorCode].replace("{0}", repr(e)).replace("{1}", DatabaseHelper.getLastEntry.__qualname__) 
            return {errorCode: errorDesc}


db_uri = "sqlite:///speedtest.db"
engine =  create_engine(db_uri, convert_unicode=False)
metadata = MetaData(engine)
Base.metadata.create_all(engine)