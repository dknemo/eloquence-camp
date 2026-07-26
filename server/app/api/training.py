"""
训练题库模块
"""
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..extensions import db
from ..models.training import TrainingItem
from ..models.user import User
from ..services.growth import LEVEL_LABELS, max_difficulty
from ..utils import fail, ok, paginated

bp = Blueprint('training', __name__)


def _current_user():
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        user_id = int(identity) if identity else None
        return User.query.get(user_id) if user_id else None
    except Exception:
        return None


def _enrich_item(item_dict, user):
    level = user.growth_level if user else 'newbie'
    max_d = max_difficulty(level)
    diff = item_dict.get('difficulty') or 1
    locked = diff > max_d and not item_dict.get('owner_user_id')
    item_dict['locked'] = locked
    if locked:
        item_dict['lock_reason'] = f'达到{LEVEL_LABELS.get(level, level)}等级后可练（当前最高⭐{max_d}）'
    return item_dict


@bp.route('/items', methods=['GET'])
def list_items():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    category = request.args.get('category')
    difficulty = request.args.get('difficulty', type=int)
    keyword = request.args.get('keyword')

    user = _current_user()
    query = TrainingItem.query.filter_by(status='online')
    if user:
        query = query.filter(db.or_(TrainingItem.owner_user_id.is_(None), TrainingItem.owner_user_id == user.id))
    else:
        query = query.filter(TrainingItem.owner_user_id.is_(None))

    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if keyword:
        query = query.filter(
            TrainingItem.title.contains(keyword) |
            TrainingItem.tags.contains(keyword)
        )

    total = query.count()
    items = query.order_by(TrainingItem.sort_order.asc())\
                  .offset((page - 1) * page_size)\
                  .limit(page_size).all()

    return paginated(
        [_enrich_item(item.to_dict(), user) for item in items],
        {'page': page, 'page_size': page_size, 'total': total}
    )


@bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    user = _current_user()
    item = TrainingItem.query.get_or_404(item_id)
    if item.status != 'online':
        return fail(404, '训练题不存在或已下架')
    if item.owner_user_id and (not user or item.owner_user_id != user.id):
        return fail(403, '无权访问该练习')
    data = _enrich_item(item.to_dict(), user)
    if user:
        from ..models.common import PracticeRecord
        last = PracticeRecord.query.filter_by(user_id=user.id, training_item_id=item.id)\
            .order_by(PracticeRecord.created_at.desc()).first()
        if last:
            data['last_practice'] = {
                'ai_score': last.ai_score,
                'duration': last.duration,
                'created_at': last.created_at.isoformat() if last.created_at else None,
            }
    return ok(data)


@bp.route('/reviews', methods=['GET'])
def review_list():
    """训练复盘列表 — 返回用户的练习记录及AI点评"""
    from ..models.common import PracticeRecord
    from ..models.training import TrainingItem

    user = _current_user()
    if not user:
        return fail(401, '请先登录')

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    keyword = request.args.get('keyword')
    success_filter = request.args.get('success')

    query = PracticeRecord.query.filter_by(user_id=user.id)\
        .order_by(PracticeRecord.created_at.desc())

    if keyword:
        query = query.join(TrainingItem, PracticeRecord.training_item_id == TrainingItem.id, isouter=True)\
            .filter(TrainingItem.title.contains(keyword))

    if success_filter is not None:
        is_success = success_filter.lower() == 'true'
        if is_success:
            query = query.filter(PracticeRecord.ai_score >= 60)
        else:
            query = query.filter(db.or_(PracticeRecord.ai_score < 60, PracticeRecord.ai_score.is_(None)))

    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()

    items = []
    for r in records:
        title = '练习'
        training_item_id = r.training_item_id
        if training_item_id:
            ti = TrainingItem.query.get(training_item_id)
            if ti:
                title = ti.title
        items.append({
            'id': r.id,
            'training_item_id': training_item_id,
            'title': title,
            'ai_score': r.ai_score,
            'ai_feedback': r.ai_feedback,
            'duration': r.duration,
            'success': r.ai_score is not None and r.ai_score >= 60,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        })

    return ok({'items': items, 'total': total, 'page': page, 'page_size': page_size})
