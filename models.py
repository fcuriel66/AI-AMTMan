from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import backref

db = SQLAlchemy()   # Define db as SQLAlchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'User= {self.name}, ID= {self.id}'


class Aircraft(db.Model):
    __tablename__ = 'aircrafts'
    serial_n = db.Column(db.Integer, primary_key=True, unique=True)
    type = db.Column(db.String(10), nullable=False)
    registration = db.Column(db.String(10))
    year_model = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Integer, nullable=False)      # In hours
    tsmo_airframe = db.Column(db.Integer, nullable=False)   # In hours
    tsmo_left_e = db.Column(db.Integer, nullable=False)     # In hours
    tsmo_right_e = db.Column(db.Integer, nullable=False)    # In hours
    total_cycles = db.Column(db.Integer, nullable=False)
    operational_life_time = db.Column(db.Integer, nullable=False)   # In months

    def __repr__(self):
        return (f"<Aircraft {self.type}: {self.serial_n}, "
                f"Op. Lifetime: {self.operational_life_time}, Year: {self.year_model}>")


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    service_name = db.Column(db.String(20), nullable=False)
    service_periodicity = db.Column(db.Integer, nullable=False)     # In months
    # Foreign Key w/users table
    aircraft_serial = db.Column(db.Integer, db.ForeignKey('aircrafts.serial_n'))
    # "SQL" type of relationship to users
    user = db.relationship('Aircraft', backref=db.backref('services', lazy=True))

    def __repr__(self):
        return f"<Service {self.service_name}, {self.service_periodicity}>"


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    text = db.Column(db.String(500), nullable=False)
    # Foreign Keys w/aircrafts and users tables
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.serial_n'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # SQL relationship to users and aircrafts
    user = db.relationship('User', backref=db.backref('requests', lazy=True))
    aircraft = db.relationship('Aircraft', backref=db.backref('requests'), lazy=True)

    def __repr__(self):
        return f"<Request:\n {self.text}>"


class FetchedTask(db.Model):
    __tablename__ = 'fetched_tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    text = db.Column(db.String(15000))
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
    request = db.relationship('Request', backref=db.backref('fetched_tasks', lazy=True))

