from flask_socketio import emit, send
from NodeDefender import socketio, settings, config

@socketio.on('create', namespace='/mqtt')
def create(host, port, group):
    try:
        NodeDefender.db.mqtt.create(host, port)
    except AttributeError as e:
        emit('error', e, namespace='/general')
    NodeDefender.db.group.add_mqtt(group, host, port)
    NodeDefender.new_mqtt.delay(group.name, mqtt.host, mqtt.port)
    LoadMQTT([mqtt])
    emit('reload', namespace='/general')
    return True

@socketio.on('list', namespace='/mqtt')
def list(group):
    emit('list', NodeDefender.db.mqtt.list(group))
    return True

@socketio.on('info', namespace='/mqtt')
def info(host, port):
    emit('info', NodeDefender.db.mqtt.get(host, port).to_json())
    return True
