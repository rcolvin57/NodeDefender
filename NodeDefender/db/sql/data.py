from NodeDefender.db.sql import SQL
from datetime import datetime
#from ...iCPE.zwave import commandclass

class HeatModel(SQL.Model):
    __tablename__ = 'heat'
    id = SQL.Column(SQL.Integer, primary_key=True)
    date = SQL.Column(SQL.DateTime)

    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    icpe_id = SQL.Column(SQL.Integer, SQL.ForeignKey('icpe.id'))
    sensor_id = SQL.Column(SQL.Integer, SQL.ForeignKey('sensor.id'))
    
    high = SQL.Column(SQL.Float)
    low = SQL.Column(SQL.Float)
    average = SQL.Column(SQL.Float)

    def __init__(self, heat, date = datetime.now()):
        self.high = heat
        self.low = heat
        self.average = heat
        self.date = date

class PowerModel(SQL.Model):
    __tablename__ = 'power'
    id = SQL.Column(SQL.Integer, primary_key=True)
    date = SQL.Column(SQL.DateTime)

    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    icpe_id = SQL.Column(SQL.Integer, SQL.ForeignKey('icpe.id'))
    sensor_id = SQL.Column(SQL.Integer, SQL.ForeignKey('sensor.id'))

    high = SQL.Column(SQL.Float)
    low = SQL.Column(SQL.Float)
    average = SQL.Column(SQL.Float)
    total = SQL.Column(SQL.Float)

    def __init__(self, power = 0.0, date = datetime.now()):
        self.high = power
        self.low = power
        self.average = power
        self.total = power
        self.date = date

    def to_json(self):
        node = self.node.name if self.node else None
        icpe = self.icpe.macaddr if self.icpe else None
        sensor = self.sensor.sensorid if self.sensor else None
        
        return {'high' : self.high, 'low' : self.low, 'average' : self.average,
                'node' : node, 'icpe' : icpe, 'sensor' : sensor,
                'date' : str(self.date)}

class EventModel(SQL.Model):
    __tablename__ = 'event'
    id = SQL.Column(SQL.Integer, primary_key=True)
    date = SQL.Column(SQL.DateTime)

    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    icpe_id = SQL.Column(SQL.Integer, SQL.ForeignKey('icpe.id'))
    sensor_id = SQL.Column(SQL.Integer, SQL.ForeignKey('sensor.id'))
    commandclass_id = SQL.Column(SQL.Integer, SQL.ForeignKey('commandclass.id'))
    commandclasstype_id = SQL.Column(SQL.Integer,
                                    SQL.ForeignKey('commandclasstype.id'))

    value = SQL.Column(SQL.String(16))

    critical = SQL.Column(SQL.Boolean)
    normal = SQL.Column(SQL.Boolean)

    def __init__(self, value, date = None):
        self.value = value
        self.date = date if date else datetime.now()

    def to_json(self):
        if self.commandclasstype:
            name = self.commandclasstype.name
            icon = eval('commandclass.'+self.commandclass.name+'.'+\
                        self.commandclasstype.name+'.Icon')(self.value)
        elif self.commandclass:
            name = self.commandclass.name
            icon = eval('commandclass.'+self.commandclass.name+'.Icon')\
                        (self.value)
        else:
            name = 'unkown'
            icon = 'fa fa-question'

        return {'iCPE' : self.icpe.macaddr, 'sensor' : self.sensor.productname, 'node' :
                self.icpe.node.name, 'value' : self.value,\
                'date' : str(self.date), 'icon' : icon,\
                'name' : name}
