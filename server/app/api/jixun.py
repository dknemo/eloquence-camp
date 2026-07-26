"""
集训打卡模块 API
"""
from datetime import date, timedelta

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..extensions import db
from ..models.jixun import JixunEvent, JixunSignup, JixunRecord
from ..models.user import User
from ..utils import fail, ok, paginated

bp = Blueprint('jixun', __name__)


def _get_user_id():
    """从JWT获取用户ID（可选登录）"""
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        return int(identity) if identity else None
    except Exception:
        return None


@bp.route('/events', methods=['GET'])
def list_events():
    """集训活动列表"""
    events = JixunEvent.query.order_by(JixunEvent.start_date.desc()).all()
    
    result = []
    for event in events:
        # 计算参与人数
        signup_count = JixunSignup.query.filter_by(event_id=event.id).count()
        
        result.append({
            'id': event.id,
            'title': event.title,
            'start_date': str(event.start_date),
            'end_date': str(event.end_date),
            'total_days': event.total_days,
            'signup_requirement': event.signup_requirement,
            'participant_count': signup_count,
            'has_calendar': event.has_calendar,
        })
    
    return ok({'events': result})


@bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """集训详情"""
    event = JixunEvent.query.get_or_404(event_id)
    return ok(event.to_dict())


@bp.route('/my-signup/<int:event_id>', methods=['GET'])
def my_signup(event_id):
    """查询我是否已报名"""
    user_id = _get_user_id()
    if not user_id:
        return fail(401, '请先登录')
    
    signup = JixunSignup.query.filter_by(user_id=user_id, event_id=event_id).first()
    if signup:
        return ok({
            'signed_up': True,
            'countdown': signup.countdown,
            'think_time': signup.think_time,
            'attempts': signup.attempts,
        })
    else:
        # 返回默认配置
        event = JixunEvent.query.get_or_404(event_id)
        return ok({
            'signed_up': False,
            'countdown': event.default_countdown,
            'think_time': event.default_think_time,
            'attempts': event.default_attempts,
        })


@bp.route('/signup', methods=['POST'])
def signup():
    """报名集训"""
    user_id = _get_user_id()
    if not user_id:
        return fail(401, '请先登录')
    
    data = request.get_json()
    event_id = data.get('event_id')
    if not event_id:
        return fail(400, 'event_id不能为空')
    
    # 检查活动是否存在
    event = JixunEvent.query.get(event_id)
    if not event:
        return fail(404, '活动不存在')
    
    # 检查是否已报名
    existing = JixunSignup.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        # 允许修改配置
        existing.countdown = data.get('countdown', existing.countdown)
        existing.think_time = data.get('think_time', existing.think_time)
        existing.attempts = data.get('attempts', existing.attempts)
        db.session.commit()
        return ok({'message': '报名信息已更新'})
    
    # 创建报名记录
    signup = JixunSignup(
        user_id=user_id,
        event_id=event_id,
        countdown=data.get('countdown', event.default_countdown),
        think_time=data.get('think_time', event.default_think_time),
        attempts=data.get('attempts', event.default_attempts),
    )
    db.session.add(signup)
    db.session.commit()
    
    return ok({'message': '报名成功', 'signup_id': signup.id})


@bp.route('/checkin', methods=['POST'])
def checkin():
    """提交打卡"""
    user_id = _get_user_id()
    if not user_id:
        return fail(401, '请先登录')
    
    data = request.get_json()
    event_id = data.get('event_id')
    day_number = data.get('day_number')
    
    if not event_id or not day_number:
        return fail(400, 'event_id和day_number不能为空')
    
    # 检查是否已报名
    signup = JixunSignup.query.filter_by(user_id=user_id, event_id=event_id).first()
    if not signup:
        return fail(403, '请先报名该集训')
    
    # 创建打卡记录
    record = JixunRecord(
        user_id=user_id,
        event_id=event_id,
        day_number=day_number,
        content_text=data.get('content_text', ''),
        audio_url=data.get('audio_url', ''),
        image_urls=data.get('image_urls', []),
    )
    db.session.add(record)
    db.session.commit()
    
    return ok({
        'message': '打卡成功',
        'record_id': record.id,
    })


@bp.route('/checkin/<int:event_id>', methods=['GET'])
def get_checkins(event_id):
    """获取该活动的打卡记录（同学作业）"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    query = JixunRecord.query.filter_by(event_id=event_id) \
        .order_by(JixunRecord.created_at.desc())
    
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    
    items = []
    for r in records:
        user = User.query.get(r.user_id)
        items.append({
            'id': r.id,
            'user': {
                'nickname': user.nickname if user else f'用户{r.user_id}',
                'avatar_url': user.avatar_url if user else '',
            },
            'day_number': r.day_number,
            'content_text': r.content_text,
            'audio_url': r.audio_url,
            'image_urls': r.image_urls or [],
            'ai_feedback': r.ai_feedback,
            'ai_hints': r.ai_hints,
            'likes_count': r.likes_count,
            'comments_count': r.comments_count,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        })
    
    return paginated(items, {'page': page, 'page_size': page_size, 'total': total})
