from flask import Flask, current_app
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from resume import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy(app)
ma = Marshmallow(app)


class BaseModel(db.Model):
    
    """Base data model for all objects"""
    ID = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    createdDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    lastModifiedDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class User(BaseModel, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema':'users'}
    restId = db.Column(db.Integer,db.Sequence('user_sequence'), unique=True)
    userame = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    login = db.relationship("users.login", uselist=False, back_populates="users.user")
    membership = db.relationship("users.membership")
    
   
class Login(BaseModel, db.Model):
    __tablename__ = 'login'
    __table_args__ = {'schema':'users'}
    restId = db.Column(db.Integer,db.Sequence('login_sequence'), unique=True)
    username = db.Column(db.String(80), unique=True)
    passwordHash = db.Column(db.String(80))
    userId = db.Column(UUID(as_uuid=True),db.ForeignKey('users.user.ID'),server_default=db.text("uuid_generate_v4()"))
    user = db.relationship("users.user", back_populates="users.login")

class Memerbership(BaseModel,db.Model):
    __tablename__ = 'membership'
    __table_args__ = {'schema':'users'}
    restId = db.Column(db.Integer,db.Sequence('membership_sequence'), unique=True)
    userId = db.Column(UUID(as_uuid=True),db.ForeignKey('users.user.ID'),server_default=db.text("uuid_generate_v4()"))
    subscriptionId = db.Column(UUID(as_uuid=True),db.ForeignKey('users.subscription.ID'), server_default=db.text("uuid_generate_v4()"))
    roleid = db.Column(UUID(as_uuid=True),db.ForeignKey('users.role.ID'),server_default=db.text("uuid_generate_v4()"))
    productid = db.Column(UUID(as_uuid=True),db.ForeignKey('products.product.ID'),server_default=db.text("uuid_generate_v4()"))
    cancelledDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    user = db.relationship("users.user", back_populates="users.membership")
    role = db.relationship("users.role", back_populates="users.membership")
    product = db.relationship("products.product", back_populates="users.membership")
    subscription = db.relationship("users.subscription", back_populates="users.membership")
    payment = db.relationship("billing.payment")

class Role(BaseModel,db.Model):
    __tablename__ = 'role'
    __table_args__ = {'schema':'users'}
    restId = db.Column(db.Integer,db.Sequence('role_sequence'), unique=True)
    membership = db.relationship("users.membership",uselist=False, back_populates="users.role")

class Product(BaseModel,db.Model):
    __tablename__ = 'product'
    __table_args__ = {'schema':'products'}
    restId = db.Column(db.Integer,db.Sequence('product_sequence'), unique=True)
    displayName = db.Column(db.String(256))
    shortName = db.Column(db.String(55))
    description = db.Column(db.String(1500))
    aboutText = db.Column(db.String(3500))
    price = db.Column(db.Numeric)
    membership = db.relationship("users.membership",uselist=False, back_populates="products.product")

class Tier(db.Model):
    ID =  db.Column(db.Integer,db.Sequence('tier_sequence'), primary_key=True)
    description = db.Column(db.String(160))

class Subscription(BaseModel,db.Model):
    __tablename__ = 'subscription'
    __table_args__ = {'schema':'users'}
    restId = db.Column(db.Integer,db.Sequence('subscription_sequence'), unique=True)
    tier = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    discountLevel = db.Column(db.Numeric)
    cancelledDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    renewalDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    renewalNotificationDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    renewalNotificationSent = db.Column(db.Boolean)
    membership = db.relationship("users.membership", uselist=False, back_populates="users.subscription")

class BillingInfo(BaseModel,db.Model):
    __tablename__ = 'information'
    __table_args__ = {'schema':'billing'}
    restId = db.Column(db.Integer,db.Sequence('billinginfo_sequence'), unique=True)
    userId = db.Column(UUID(as_uuid=True),db.ForeignKey('users.user.ID'),server_default=db.text("uuid_generate_v4()"))
    

class Payment(BaseModel,db.Model):
    __tablename__ = 'payment'
    __table_args__ = {'schema':'billing'}
    restId = db.Column(db.Integer,db.Sequence('payment_sequence'), unique=True)
    transactionAmount = db.Column(db.Numeric)
    discountApplied = db.Column(db.Boolean)
    discountAmount = db.Column(db.Numeric)
    notified = db.Column(db.Boolean)
    lastNotifcationSent = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    userId = db.Column(UUID(as_uuid=True),db.ForeignKey('users.user.ID'),server_default=db.text("uuid_generate_v4()"))
    informationId = db.Column(UUID(as_uuid=True),server_default=db.text("uuid_generate_v4()"))         
    membershipId = db.Column(UUID(as_uuid=True),db.ForeignKey('users.membership.ID'),server_default=db.text("uuid_generate_v4()"))
    paymentDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    daysOverdue = db.Column(db.Integer, nullable=False,default = 0)

class Test(BaseModel, db.Model):
    __tablename__ = 'testing'
    restId = db.Column(db.Integer,db.Sequence('payment_sequence'), unique=True)