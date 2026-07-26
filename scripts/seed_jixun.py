"""
集训打卡模块 — Seed 数据脚本
运行: python scripts/seed_jixun.py
"""
import sys
import os
# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from datetime import date
from app import create_app
from app.extensions import db
from app.models.jixun import JixunEvent

def seed_jixun_events():
    """插入6条集训活动示例数据"""
    app = create_app('development')
    
    with app.app_context():
        # 检查是否已有数据
        count = JixunEvent.query.count()
        if count > 0:
            print(f"⚠️  数据库已有 {count} 条集训数据，跳过seed")
            return
        
        events = [
            {
                "title": "7月7天批判性思维（独立思考）打卡集训",
                "description": """7天'独立思考（批判性思维）'集训，旨在帮助你提升独立思考能力，培养批判性思维习惯。

每日题目：
第1天：如何判断一个信息是否可靠？
第2天：什么是逻辑谬误？举例说明。
第3天：如何区分事实与观点？
第4天：为什么我们需要多角度思考问题？
第5天：如何识别偏见？
第6天：什么是证据？什么样的证据最有说服力？
第7天：总结一周所学，分享一个你运用批判性思维解决的实际案例""",
                "start_date": date(2026, 7, 27),
                "end_date": date(2026, 8, 3),
                "total_days": 7,
                "signup_requirement": "所有人",
                "default_countdown": 45,
                "default_think_time": 30,
                "default_attempts": 8,
                "has_calendar": True,
            },
            {
                "title": "7月7天'结构划分'打卡集训",
                "description": """7天'结构划分'集训，学习如何用结构化思维组织表达内容。

每日题目：
第1天：什么是金字塔原理？如何应用？
第2天：MECE原则是什么？举例说明。
第3天：如何用SCQA框架讲故事？
第4天：时间顺序、空间顺序、重要性顺序的区别与应用。
第5天：如何构建一个清晰的汇报结构？
第6天：演讲中的结构技巧——开头、主体、结尾。
第7天：综合练习——用结构化思维分析一个社会热点话题""",
                "start_date": date(2026, 8, 3),
                "end_date": date(2026, 8, 10),
                "total_days": 7,
                "signup_requirement": "高级会员可报名",
                "default_countdown": 40,
                "default_think_time": 25,
                "default_attempts": 6,
                "has_calendar": True,
            },
            {
                "title": "8月7天即兴演讲打卡集训",
                "description": """7天即兴演讲集训，快速提升临场表达能力。

每日题目：
第1天：30秒自我介绍——如何让人记住你？
第2天：如何用PREP结构快速组织观点？
第3天：面对突发问题，如何冷静回应？
第4天：如何用一个故事打动听众？
第5天：辩论技巧——如何快速反驳对方观点？
第6天：如何将复杂概念讲得通俗易懂？
第7天：综合挑战——3分钟即兴演讲，主题随机抽取""",
                "start_date": date(2026, 8, 10),
                "end_date": date(2026, 8, 17),
                "total_days": 7,
                "signup_requirement": "所有人",
                "default_countdown": 35,
                "default_think_time": 20,
                "default_attempts": 5,
                "has_calendar": True,
            },
            {
                "title": "8月7天公众演讲打卡集训",
                "description": """7天公众演讲集训，从紧张到自信登台。

每日题目：
第1天：克服演讲紧张的方法与实践。
第2天：如何设计一个吸引人的开场白？
第3天：肢体语言在演讲中的作用。
第4天：声音技巧——语调、停顿、重音。
第5天：如何制作有说服力的PPT？
第6天：互动技巧——如何让听众参与进来？
第7天：模拟演讲——完整呈现一次5分钟演讲""",
                "start_date": date(2026, 8, 17),
                "end_date": date(2026, 8, 24),
                "total_days": 7,
                "signup_requirement": "教练团专属",
                "default_countdown": 45,
                "default_think_time": 30,
                "default_attempts": 8,
                "has_calendar": True,
            },
            {
                "title": "9月7天商务沟通打卡集训",
                "description": """7天商务沟通集训，提升职场表达能力。

每日题目：
第1天：电梯演讲——如何在1分钟内说清你的想法？
第2天：如何高效主持会议？
第3天：商务谈判中的沟通技巧。
第4天：如何向上级汇报工作？
第5天：跨部门协作中的沟通策略。
第6天：客户拜访中的语言表达。
第7天：综合演练——模拟一次商务会议""",
                "start_date": date(2026, 9, 1),
                "end_date": date(2026, 9, 8),
                "total_days": 7,
                "signup_requirement": "所有人",
                "default_countdown": 40,
                "default_think_time": 25,
                "default_attempts": 6,
                "has_calendar": True,
            },
            {
                "title": "9月7天 storytelling 打卡集训",
                "description": """7天故事力集训，学会用故事打动人心。

每日题目：
第1天：什么是好的故事？好故事的标准。
第2天：英雄之旅——经典故事结构。
第3天：如何用个人经历讲故事？
第4天：产品故事化——让商品会说话。
第5天：数据故事化——让数字有温度。
第6天：演讲中的故事技巧——何时讲、怎么讲。
第7天：综合创作——写一个属于你的故事并分享""",
                "start_date": date(2026, 9, 8),
                "end_date": date(2026, 9, 15),
                "total_days": 7,
                "signup_requirement": "所有人",
                "default_countdown": 35,
                "default_think_time": 20,
                "default_attempts": 5,
                "has_calendar": True,
            },
        ]
        
        for event_data in events:
            event = JixunEvent(**event_data)
            db.session.add(event)
        
        db.session.commit()
        print(f"✅ 成功插入 {len(events)} 条集训活动数据")

if __name__ == '__main__':
    seed_jixun_events()
