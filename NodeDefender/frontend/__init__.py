import logging
import NodeDefender.frontend.views
import NodeDefender.frontend.sockets

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def load(app, socketio, loggHandler):
    logger.addHandler(loggHandler)
    NodeDefender.frontend.views.load_views(app)
    NodeDefender.frontend.sockets.load_sockets(socketio)
    logger.info("Frontend loaded")
    return True

