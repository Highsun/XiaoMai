
"""
import_data.py

⚙️ 使用方式：
    在项目根目录执行：
        python -m backend.import_data

   注意：请确保当前工作目录是项目根目录（包含 backend/ 文件夹），
"""

from .app import create_app
from .extensions import db
from .models import Artist, Show, show_artists
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
        # —— 清空旧数据 ——
        db.session.execute(show_artists.delete())
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
                image_path=item["image_path"]
            )
            # 先把 show 加入 session，再关联 artist
            db.session.add(show)
            for name in item["artist_name"]:
                artist = Artist.query.filter_by(name=name).first()
                if artist:
                    show.artists.append(artist)

        db.session.commit()

        total_artists = Artist.query.count()
        total_shows = Show.query.count()
        print(f"✅ 成功插入 {total_artists} 位艺术家，{total_shows} 场演出。")

if __name__ == "__main__":
    import_all()
