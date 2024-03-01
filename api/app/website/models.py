from app import db


class Website(db.Model):
    __tablename__ = 'Domain'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    second_domain = db.Column(db.String(100))
    sub_domain_num = db.Column(db.String(100))
    ctime = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, second_domain, sub_domain_num):
        self.second_domain = second_domain
        self.sub_domain_num = sub_domain_num

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    
if __name__ == '__main__':
    pass
