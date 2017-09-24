import NodeDefender
import NodeDefender.icpe.sensor.command
import NodeDefender.icpe.sensor.commandclass

def verify_list(icpe, *sensors):
    known = [sensor.sensorid for sensor in NodeDefender.db.sensor.list(icpe)]

    for sensor in sensors:
        if sensor not in known:
            NodeDefender.db.sensor.create(icpe, sensor)

    for sensor in known:
        if sensor not in sensors:
            NodeDefender.db.sensor.delete(icpe, sensor)
    return True

def sensor_info(icpe, sensorid, **payload):
    sensor = NodeDefender.db.sensor.get_sql(icpe, sensorid)
    
    sensor.sleepable = bool(eval(payload['sleepable']))
    sensor.wakeup_interval = payload['wakeup_interval']

    info = NodeDefender.icpe.zwave.devices.info(payload['vid'], payload['pid'])
    if info is None:
        return False
    try:
        sensor.vendor_id = payload['vid']
        sensor.product_id = payload['pid']
        sensor.product_type = info['ProductTypeId']
        sensor.vendor_name = info['Brand']
        sensor.product_name = info['Name']
        sensor.device_type = info['DeviceType']
        sensor.library_type = info['LibraryType']
    except KeyError:
        print(info)
        return False

    NodeDefender.icpe.sensor.commandclass.\
            commandclasses(icpe, sensorid, *payload['clslist_0'].split(','))
    
    NodeDefender.db.sensor.save_sql(sensor)
    NodeDefender.db.redis.sensor.load(sensor)
    return NodeDefender.db.sensor.get(icpe, sensorid)

def event(mac_address, sensor_id, CommandClass, **payload):
    if CommandClass == 'info':
        return True
    data = NodeDefender.icpe.zwave.event(mac_address, sensor_id, \
                                         CommandClass, **payload)
    if not data:
        return False

    commandclass = data['commandclass']['name']
    commandclasstype = data['commandclasstype']['name']\
            if data['commandclasstype'] else None

    NodeDefender.db.field.update(mac_address, sensor_id, data['fields']['name'], \
                    **{'value' : data['value'], 'state' : data['state']})
    NodeDefender.db.data.sensor.event.put(mac_address, sensor_id,\
                                       commandclass, commandclasstype,\
                                       data['state'], data['value'])
    return True
