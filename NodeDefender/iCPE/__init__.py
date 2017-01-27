from .. import celery, loggHandler
from ..models.manage import icpe as iCPESQL
from ..models.redis import icpe as iCPERedis
from ..models.redis import sensor as SensorRedis
from ..models.redis import cmdclass as CmdclassRedis
from celery.utils.log import get_task_logger
import logging

logger = logging.getLogger('iCPE')
logger.setLevel('INFO')
logger.addHandler(loggHandler)

def Load(icpes = None):
    if icpes is None:
        icpes = iCPESQL.List()
    
    for icpe in icpes:
        iCPERedis.Load(icpe)
        for sensor in icpe.sensors:
            SensorRedis.Load(sensor)
            for cmdclass in sensor.cmdclasses:
                CmdclassRedis.Load(cmdclass)
            else:
                mqtt.sensor.Query(icpe.mac, sensor.sensorid)
    return True


class TopicDescriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError("Must be a string")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete me")

class Topic:
    macaddr = TopicDescriptor("macaddr")
    msgtype = TopicDescriptor("msgtype")
    sensorid = TopicDescriptor("sensorid")
    endpoint = TopicDescriptor("endpoint")
    cmdclass = TopicDescriptor("cmdclass")
    subfunc = TopicDescriptor("subfunc")
    action = TopicDescriptor("action")
    def __init__(self):
        self.macaddr = None
        self.msgtype = None
        self.sensorid = None
        self.endpoint = None
        self.cmdclass = None
        self.subfunc = None
        self.action = None

from . import db, event, decorators
from .msgtype import cmd, err, rpt, rsp
