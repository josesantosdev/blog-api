from app import db
from sqlalchemy import BigInteger, String


class RevokedToken(db.Model):

    __tablename__ = 'revoked_tokens'

    id_token = db.Column(BigInteger, primary_key=True)
    jti = db.Column(String(100), nullable=False)


    def save(self):
        db.session.add(self)
        db.session.commit()