import re

from datetime import datetime
from time import time
from uuid import uuid4

from flask import request, url_for
from flask_login import UserMixin

from models.helper.super_model import SuperModel, db
from models.helper.enums import SessionEnum, GenderEnum

from utils.mail_helper import send_confirmation_mail

from werkzeug.security import generate_password_hash, check_password_hash

email_regex = re.compile(r"\w+@\w+\.\w+")
phone_regex = re.compile(r"[1-9][0-9]{9}")

roles = db.Table(
    "roles",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("user_role.id"), primary_key=True),
)


CONFIRMATION_EXPIRATION_DELTA = 1800


class UserModel(UserMixin, db.Model, SuperModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.male)

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sessions = db.relationship("UserSessionModel", backref="user", lazy=True)
    confirmation = db.relationship(
        "UserConfirmationModel", lazy="dynamic", cascade="all, delete-orphan",
    )
    reviews = db.relationship("ReviewModel", backref="user", lazy=True)
    cart = db.relationship("CartModel", backref="user", lazy=True, uselist=True)
    address = db.relationship("AddressModel", backref="user", lazy=True)
    roles = db.relationship(
        "UserRoleModel",
        secondary=roles,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.email}>"

    @property
    def most_recent_confirmation(self) -> "UserConfirmationModel":
        return self.confirmation.order_by(
            db.desc(UserConfirmationModel.expire_at)
        ).first()

    def pre_save(self):
        if not self.check_password_already_hashed():
            self.password = self.get_password_hash(self.password)
        assert email_regex.match(self.email), "Email is not valid"
        assert phone_regex.match(str(self.phone_no)), "Phone No is not valid"

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return generate_password_hash(password)

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for(
            "useremailconfirm", confirmation_id=self.most_recent_confirmation.id
        )
        send_confirmation_mail(self.email, link)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def check_password_already_hashed(self):
        if self.password.startswith("pbkdf2:sha256:"):
            return True
        return False


class UserSessionModel(db.Model, SuperModel):
    __tablename__ = "user_session"

    # here we will have virtual column of "user" as there is backref in UserModel
    # user
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20), nullable=True)
    type = db.Column(db.Enum(SessionEnum), default=SessionEnum.web)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    tokens = db.relationship("UserSessionTokenModel", backref="session", lazy=True)
    cart = db.relationship("CartModel", backref="session", lazy=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.ip}>"


class UserSessionTokenModel(db.Model, SuperModel):
    __tablename__ = "user_session_token"

    # here we will have virtual column of "session" as there is backref in UserModel
    # session
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    refresh_token = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session_id = db.Column(db.Integer, db.ForeignKey("user_session.id"), nullable=False)


class UserRoleModel(db.Model, SuperModel):
    __tablename__ = "user_role"

    # users
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(20), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.role}>"


class UserConfirmationModel(db.Model, SuperModel):
    __tablename__ = "user_confirmation"

    # user
    id = db.Column(db.String, primary_key=True, default=uuid4().hex)
    expire_at = db.Column(db.Integer, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    user = db.relationship("UserModel")

    def pre_save(self):
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.confirmed}>"
