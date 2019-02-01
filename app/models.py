from app.app import db
import datetime


class Installation(db.Model):
    __tablename__ = 'installation'

    id           = db.Column(db.Integer, primary_key=True)
    install_id   = db.Column(db.Integer, unique=True, nullable=False)
    sub_id       = db.Column(db.Integer)
    api_key      = db.Column(db.String)
    created_date = db.Column(db.DateTime(timezone=True))
    enabled_date = db.Column(db.DateTime(timezone=True))
    last_update  = db.Column(db.DateTime(timezone=True))
    last_used    = db.Column(db.DateTime(timezone=True))
    hit_count    = db.Column(db.Integer)
    enabled      = db.Column(db.Boolean, default=True)

    def __init__(self, install_id, sub_id=None, api_key=None):
        self.install_id = install_id
        self.sub_id     = sub_id
        self.api_key    = api_key
        #self.created_date = datetime.date.today().strftime("%Y-%m-%d")
        self.created_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return '<id {}>'.format(self.id)

