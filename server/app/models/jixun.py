"""
集训打卡模块 — 数据库模型
"""
from datetime import datetime

from ..extensions import db


class JixunEvent(db.Model):
    __tablename__ = 'jixun_events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)  # 详情介绍文字
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, default=7)
    signup_requirement = db.Column(db.String(100), default='所有人')
    default_countdown = db.Column(db.Integer, default=45)
    default_think_time = db.Column(db.Integer, default=30)
    default_attempts = db.Column(db.Integer, default=8)
    has_calendar = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'total_days': self.total_days,
            'signup_requirement': self.signup_requirement,
            'default_countdown': self.default_countdown,
            'default_think_time': self.default_think_time,
            'default_attempts': self.default_attempts,
            'has_calendar': self.has_calendar,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class JixunSignup(db.Model):
    __tablename__ = 'jixun_signups'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('jixun_events.id', ondelete='CASCADE'), nullable=False)
    countdown = db.Column(db.Integer, default=45)
    think_time = db.Column(db.Integer, default=30)
    attempts = db.Column(db.Integer, default=8)
    signed_up_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='uk_user_event'),)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'countdown': self.countdown,
            'think_time': self.think_time,
            'attempts': self.attempts,
            'signed_up_at': self.signed_up_at.isoformat() if self.signed_up_at else None,
        }


class JixunRecord(db.Model):
    __tablename__ = 'jixun_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('jixun_events.id', ondelete='CASCADE'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)  # 第几天
    content_text = db.Column(db.Text, default='')
    audio_url = db.Column(db.String(512), default='')
    image_urls = db.Column(db.JSON, default=list)
    ai_feedback = db.Column(db.Text, default='')
    ai_hints = db.Column(db.Text, default='')
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'day_number': self.day_number,
            'content_text': self.content_text,
            'audio_url': self.audio_url,
            'image_urls': self.image_urls or [],
            'ai_feedback': self.ai_feedback,
            'ai_hints': self.ai_hints,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
