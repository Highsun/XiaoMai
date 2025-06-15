"""
import_data.py

⚙️ 使用方式：
    在项目根目录执行：
        python -m backend.import_data

   注意：请确保当前工作目录是项目根目录（包含 backend/ 文件夹），
"""

from .app import create_app
from .extensions import db
from .models import Artist, Show, show_artists, Order, OrderItem
import json
from datetime import datetime as _dt

def parse_date_range(s: str):
    s = s.replace(" ", "")
    if "-" in s:
        left, right = s.split("-", 1)
        parts = right.split(".")
        if len(parts) == 2:
            year = left.split(".")[0]
            right = f"{year}.{right}"
        sd = _dt.strptime(left, "%Y.%m.%d").date()
        ed = _dt.strptime(right, "%Y.%m.%d").date()
        return sd, ed
    if "/" in s:
        left, right = s.split("/", 1)
        year = left.split(".")[0]
        sd = _dt.strptime(left, "%Y.%m.%d").date()
        ed = _dt.strptime(f"{year}.{right}", "%Y.%m.%d").date()
        return sd, ed
    d = _dt.strptime(s, "%Y.%m.%d").date()
    return d, d

def import_all():
    app = create_app()
    with app.app_context():
        # —— 清空旧数据（顺序不能错） ——
        db.session.execute(show_artists.delete())
        OrderItem.query.delete()
        Order.query.delete()
        Show.query.delete()
        Artist.query.delete()
        db.session.commit()

        # —— 导入艺术家数据 ——
        with open("src/assets/data/artists.json", "r", encoding="utf-8") as f:
            artists_data = json.load(f)

        artist_objs = [
            Artist(
                name=item["name"],
                image_path=item["image_path"],
                link=item["link"]
            )
            for item in artists_data
        ]
        db.session.add_all(artist_objs)
        db.session.commit()

        # —— 导入演出数据 ——
        with open("src/assets/data/shows.json", "r", encoding="utf-8") as f:
            raw_shows = json.load(f)

        for item in raw_shows:
            sd, ed = parse_date_range(item["date"])
            show = Show(
                title=item["title"],
                tag=item["tag"],
                start_date=sd,
                end_date=ed,
                location=item["location"],
                price=item["price"],
                status=item["status"],
                ticket_status=item["ticket_status"],
                image_path=item["image_path"],
                sessions=item.get("sessions", []),
                price_tiers=item.get("price_tiers", []),
                map_url=item.get("map_url", "")
            )
            db.session.add(show)
            # 关联多对多
            for name in item.get("artist_name", []):
                artist = Artist.query.filter_by(name=name).first()
                if artist:
                    show.artists.append(artist)

        db.session.commit()

        total_artists = Artist.query.count()
        total_shows = Show.query.count()
        print(f"✅ 成功插入 {total_artists} 位艺术家，{total_shows} 场演出。")

        # —— 批量导入票夹订单测试数据（user_id=1） ——
        test_orders = [
            {
                "show_title": "JJ20 FINAL LAP 世界巡回演唱会",
                "artist_name": "林俊杰",
                "seat_number": "B区 1排 8号",
                "price": 1880,
                "status": "paid",  # 交易成功
                "ticket_status": "未使用",
                "qr_code": "/uploads/已核销.png",
                "order_time": "2025-05-26 20:00:22",
                "expire_at": "2025-05-10 23:59:59"
            },
            {
                "show_title": "周杰伦《嘉年华》巡回演唱会",
                "artist_name": "周杰伦",
                "seat_number": "A区 3排 12号",
                "price": 1100,
                "status": "paid",
                "ticket_status": "未使用",
                "qr_code": "/uploads/已核销.png",
                "order_time": "2025-03-15 12:00:34",
                "expire_at": "2025-07-20 23:59:59"
            },
            {
                "show_title": "陶喆 Soul Power II 世界巡回演唱会",
                "artist_name": "陶喆",
                "seat_number": "C区 2排 5号",
                "price": 780,
                "status": "paid",
                "ticket_status": "已使用",
                "qr_code": "/uploads/已核销.png",
                "order_time": "2025-04-25 11:55:57",
                "expire_at": "2025-04-28 23:59:59"
            },
            {
                "show_title": "【哈尔滨】五月天 2025五月天25周年巡回演唱会",
                "artist_name": "五月天",
                "seat_number": "D区 6排 19号",
                "price": 580,
                "status": "cancelled",  # 已取消
                "ticket_status": "已过期",
                "qr_code": "/uploads/已核销.png",
                "order_time": "2025-06-01 19:30:47",
                "expire_at": "2025-06-13 23:59:59"
            },
        ]
        test_user_id = 1
        for o in test_orders:
            show = Show.query.filter_by(title=o["show_title"]).first()
            if not show:
                print(f"❌ 没找到演出《{o['show_title']}》，请检查 shows 数据！")
                continue
            order = Order(
                user_id=test_user_id,
                total_price=o["price"],
                status=o["status"],
                created_at=_dt.strptime(o["order_time"], "%Y-%m-%d %H:%M:%S"),
                updated_at=_dt.strptime(o["order_time"], "%Y-%m-%d %H:%M:%S"),
            )
            db.session.add(order)
            db.session.flush()  # 获得order.id
            item = OrderItem(
                order_id=order.id,
                show_id=show.id,
                quantity=1,
                unit_price=o["price"],
                created_at=_dt.strptime(o["order_time"], "%Y-%m-%d %H:%M:%S"),
                seat_number=o["seat_number"],
                qr_code=o["qr_code"],
                ticket_status=o["ticket_status"],
                expire_at=_dt.strptime(o["expire_at"], "%Y-%m-%d %H:%M:%S"),
            )
            db.session.add(item)
        db.session.commit()
        total_orders = Order.query.count()
        print(f"✅ 成功插入 {total_orders} 条订单及票夹测试数据。")

if __name__ == "__main__":
    import_all()
