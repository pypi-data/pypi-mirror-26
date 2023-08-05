from notmm.dbapi.orm import RelationProxy, XdserverProxy

db = XdserverProxy(db_name='moviereviews')
db._sync()

class ActorManager(object):
    pass
class MovieCastingManager(object):
    pass


