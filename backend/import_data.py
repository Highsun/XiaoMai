from datetime import datetime
from backend.app import create_app
from backend.extensions import db
from backend.models import Artist, Show
import json

def parse_date_range(s: str):
    """
    将 "YYYY.MM.DD-YYYY.MM.DD" / "YYYY.MM.DD-MM.DD" /
    "YYYY.MM.DD/MM.DD" / "YYYY.MM.DD" 解析为 (start_date, end_date)
    """
    s = s.replace(" ", "")
    from datetime import datetime as _dt

    # 1) 范围以 '-' 分隔
    if "-" in s:
        left, right = s.split("-", 1)
        parts = right.split(".")
        if len(parts) == 2:  # 右侧缺年份
            year = left.split(".")[0]
            right = f"{year}.{right}"
        sd = _dt.strptime(left, "%Y.%m.%d").date()
        ed = _dt.strptime(right, "%Y.%m.%d").date()
        return sd, ed
    # 2) 范围以 '/' 分隔
    if "/" in s:
        left, right = s.split("/", 1)
        year = left.split(".")[0]
        sd = _dt.strptime(left, "%Y.%m.%d").date()
        ed = _dt.strptime(f"{year}.{right}", "%Y.%m.%d").date()
        return sd, ed
    # 3) 单日期
    d = _dt.strptime(s, "%Y.%m.%d").date()
    return d, d

def import_all():
    # 1. 创建应用并推入上下文
    app = create_app()
    with app.app_context():
        # 2. 清空旧数据
        Show.query.delete()
        Artist.query.delete()
        db.session.commit()

        # 3. 插入艺术家
        with open("/Users/highsun/Desktop/Code/XiaoMai/src/assets/data/artists.json", "r", encoding="utf-8") as f:
            artists_data = json.load(f)

        artist_objs = []
        for item in artists_data:
            artist = Artist(
                name=item["name"],
                image_path=item["image_path"],
                link=item["link"]
                # created_at/updated_at 由模型 default 自动填充
            )
            artist_objs.append(artist)
        db.session.add_all(artist_objs)
        db.session.commit()

        # 4. 构建 name->id 映射
        artist_map = {a.name: a.id for a in Artist.query.all()}

        # 5. 准备演出数据（hot + upcoming）
        with open("/Users/highsun/Desktop/Code/XiaoMai/src/assets/data/shows.json", "r", encoding="utf-8") as f:
            raw_shows = json.load(f)

        # 6. 插入所有 Show
        show_objs = []
        for item in raw_shows:
            sd, ed = parse_date_range(item["date"])
            show = Show(
                title=item["title"],
                start_date=sd,
                end_date=ed,
                location=item["location"],
                price=item["price"],
                status=item["status"],
                image_path=item["image_path"],
                artist_id=artist_map[item["artist_name"]]
                # created_at/updated_at 由模型 default 自动填充
            )
            show_objs.append(show)

        db.session.add_all(show_objs)
        db.session.commit()

        print(f"✅ 插入 {len(artist_objs)} 位艺术家，{len(show_objs)} 场演出。")

if __name__ == "__main__":
    import_all()
