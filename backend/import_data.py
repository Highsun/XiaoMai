from datetime import datetime
from backend.app import create_app
from backend.extensions import db
from backend.models import Artist, Show

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
        artists_data = [
            {"name": "林俊杰", "image_path": "artists/JJ.JPG", "link": "/artist/jj"},
            {"name": "周杰伦", "image_path": "artists/Jay.JPG", "link": "/artist/jay"},
            {"name": "陶喆",   "image_path": "artists/DT.JPG", "link": "/artist/dt"},
            {"name": "王力宏", "image_path": "artists/WLH.JPG", "link": "/artist/wlh"},
            {"name": "邓紫棋", "image_path": "artists/GEM.JPG", "link": "/artist/gem"},
            {"name": "孙燕姿", "image_path": "artists/SYZ.JPG", "link": "/artist/syz"},
            {"name": "五月天", "image_path": "artists/WYT.JPG", "link": "/artist/wyt"},
            {"name": "单依纯", "image_path": "artists/SYC.JPG", "link": "/artist/syc"},
        ]
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
        raw_shows = [
            # —— 热卖中 —— status="hot"
            {
                "title": "JJ20 FINAL LAP 世界巡回演唱会",
                "date": "2025.06.28-07.13",
                "location": "北京市·国家体育场-鸟巢",
                "price": "380元起",
                "image_path": "concerts/JJ.png",
                "status": "hot",
                "artist_name": "林俊杰"
            },
            {
                "title": "周杰伦《嘉年华》巡回演唱会",
                "date": "2025.06.27-06.29",
                "location": "中国香港·香港启德体育园主场馆",
                "price": "1100元起",
                "image_path": "concerts/Jay.png",
                "status": "hot",
                "artist_name": "周杰伦"
            },
            {
                "title": "陶喆 Soul Power II 世界巡回演唱会",
                "date": "2025.08.09-08.10",
                "location": "深圳市·深圳湾体育中心“春茧”体育场",
                "price": "380元起",
                "image_path": "concerts/DT.png",
                "status": "hot",
                "artist_name": "陶喆"
            },
            {
                "title": "王力宏「最好的地方」巡回演唱会",
                "date": "2025.07.05-07.06",
                "location": "苏州市·苏州奥林匹克体育中心体育馆",
                "price": "480元起",
                "image_path": "concerts/WLH.png",
                "status": "hot",
                "artist_name": "王力宏"
            },
            # —— 即将推出 —— status="upcoming"
            {
                "title": "G.E.M. 邓紫棋 I AM GLORIA 世界巡回演唱会 2.0",
                "date": "2025.07.05",
                "location": "烟台市·烟台体育公园体育场",
                "price": "380元起",
                "image_path": "concerts/GEM.jpeg",
                "status": "upcoming",
                "artist_name": "邓紫棋"
            },
            {
                "title": "孙燕姿《就在日落以后》演唱会",
                "date": "2025.06.13/06.15",
                "location": "北京市·国家体育场-鸟巢",
                "price": "480元起",
                "image_path": "concerts/SYZ.jpeg",
                "status": "upcoming",
                "artist_name": "孙燕姿"
            },
            {
                "title": "汪苏泷 2025 巡回演唱会「十万伏特 2.0」",
                "date": "2025.06.27-06.29",
                "location": "太原市·山西体育中心体育场",
                "price": "380元起",
                "image_path": "concerts/WSL.jpeg",
                "status": "upcoming",
                "artist_name": "五月天"
            },
            {
                "title": "凤凰传奇「吉祥如意」2025 巡回演唱会",
                "date": "2025.06.27-06.29",
                "location": "天津市·天津奥林匹克中心体育场",
                "price": "380元起",
                "image_path": "concerts/FHCQ.jpeg",
                "status": "upcoming",
                "artist_name": "单依纯"
            },
        ]

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
