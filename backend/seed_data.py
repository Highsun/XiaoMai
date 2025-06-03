from datetime import datetime, date
from backend.app import create_app
from backend.extensions import db
from backend.models import Show, Artist


# -----------------------------------------------------------------------------
# —— 辅助函数：将前端的 date 字符串解析为 Python date 对象 —— 
# 前端可能有三种格式：
#   1. "YYYY.MM.DD-YYYY.MM.DD"        # 例如 "2025.06.28-07.13"
#   2. "YYYY.MM.DD- MM.DD"            # 例如 "2025.06.27-06.29"（同上）
#   3. "YYYY.MM.DD/ MM.DD"            # 例如 "2025.06.13/06.15" —— 表示同年度的两天
#   4. "YYYY.MM.DD"                   # 例如 "2025.07.05"（只有一个日期）
# 本函数返回 (start_date: date, end_date: date)
# 如果只传入单日期，则 end_date == start_date。
# -----------------------------------------------------------------------------
def parse_date_range(date_str: str) -> (date, date):
    """
    将格式如 "2025.06.28-07.13" 或 "2025.06.27-06.29" 或 "2025.06.13/06.15" 或 "2025.07.05"
    等字符串，解析成两个 date 对象 (start_date, end_date)。
    """
    # 先规范化：去掉所有空格
    s = date_str.replace(" ", "")

    # 如果包含 '-' ，则可以拆成 "起始"-"结束"
    if "-" in s:
        # 例如 "2025.06.28-07.13" 或 "2025.06.27-06.29"
        left, right = s.split("-", 1)
        # left 一定是 "YYYY.MM.DD"
        # right 可能是 "MM.DD" 或 "YYYY.MM.DD"
        if len(right.split(".")) == 2:
            # 右侧只有月日，需要补上年份
            year = left.split(".")[0]
            start_year, start_mon, start_day = left.split(".")
            end_str = f"{year}.{right}"
        else:
            # 右侧已经包含年份，比如 "2025.07.13"
            end_str = right

        start_str = left
        # 将 "YYYY.MM.DD" 转成 date
        start_date = datetime.strptime(start_str, "%Y.%m.%d").date()
        end_date = datetime.strptime(end_str, "%Y.%m.%d").date()
        return start_date, end_date

    # 如果包含 '/' ，则拆成两段 “当年”
    if "/" in s:
        # 例如 "2025.06.13/06.15"
        left, right = s.split("/", 1)
        # left 一定是 "YYYY.MM.DD"
        year = left.split(".")[0]
        start_date = datetime.strptime(left, "%Y.%m.%d").date()
        # 右侧如 "06.15"，先补年
        end_str = f"{year}.{right}"
        end_date = datetime.strptime(end_str, "%Y.%m.%d").date()
        return start_date, end_date

    # 否则只有一个日期，比如 "2025.07.05"
    single = datetime.strptime(s, "%Y.%m.%d").date()
    return single, single


# -----------------------------------------------------------------------------
# —— 主函数：将三组示例数据写入数据库 —— 
# -----------------------------------------------------------------------------
def seed():
    app = create_app()
    # 推送应用上下文
    app.app_context().push()

    # 1) 清空原有数据（如果你重复运行脚本，避免重复插入）
    Show.query.delete()
    Artist.query.delete()
    db.session.commit()

    # -------------------------------------------------------------------------
    # 2) 定义“热卖中”（HotShows）数据
    #   对应 Show 模型的字段：
    #     title, start_date, end_date, location, price, status="hot", image_path
    #   image_path 必须与 uploads/concerts/ 下的文件名一致
    # -------------------------------------------------------------------------
    raw_hot_shows = [
        {
            "title": "JJ20 FINAL LAP 世界巡回演唱会",
            "date": "2025.06.28-07.13",
            "location": "北京市·国家体育场-鸟巢",
            "price": "380元起",
            "image_path": "concerts/JJ.png",
        },
        {
            "title": "周杰伦《嘉年华》巡回演唱会",
            "date": "2025.06.27-06.29",
            "location": "中国香港·香港启德体育园主场馆",
            "price": "1100元起",
            "image_path": "concerts/Jay.png",
        },
        {
            "title": "陶喆 Soul Power II 世界巡回演唱会",
            "date": "2025.08.09-08.10",
            "location": "深圳市·深圳湾体育中心“春茧”体育场",
            "price": "380元起",
            "image_path": "concerts/DT.png",
        },
        {
            "title": "王力宏「最好的地方」巡回演唱会",
            "date": "2025.07.05-07.06",
            "location": "苏州市·苏州奥林匹克体育中心体育馆",
            "price": "480元起",
            "image_path": "concerts/WLH.png",
        },
    ]

    hot_shows_objs = []
    for item in raw_hot_shows:
        start_d, end_d = parse_date_range(item["date"])
        show = Show(
            title=item["title"],
            start_date=start_d,
            end_date=end_d,
            location=item["location"],
            price=item["price"],
            status="hot",
            image_path=item["image_path"],
        )
        hot_shows_objs.append(show)

    # -------------------------------------------------------------------------
    # 3) 定义“即将推出”（Upcomings）数据
    #   status="upcoming"
    # -------------------------------------------------------------------------
    raw_upcoming_shows = [
        {
            "title": "G.E.M. 邓紫棋 I AM GLORIA 世界巡回演唱会 2.0",
            "date": "2025.07.05",
            "location": "烟台市·烟台体育公园体育场",
            "price": "380元起",
            "image_path": "concerts/GEM.jpeg",
        },
        {
            "title": "孙燕姿《就在日落以后》演唱会",
            "date": "2025.06.13/06.15",
            "location": "北京市·国家体育场-鸟巢",
            "price": "480元起",
            "image_path": "concerts/SYZ.jpeg",
        },
        {
            "title": "汪苏泷 2025 巡回演唱会「十万伏特 2.0」",
            "date": "2025.06.27-06.29",
            "location": "太原市·山西体育中心体育场",
            "price": "380元起",
            "image_path": "concerts/WSL.jpeg",
        },
        {
            "title": "凤凰传奇「吉祥如意」2025 巡回演唱会",
            "date": "2025.06.27-06.29",
            "location": "天津市·天津奥林匹克中心体育场",
            "price": "380元起",
            "image_path": "concerts/FHCQ.jpeg",
        },
    ]

    upcoming_shows_objs = []
    for item in raw_upcoming_shows:
        start_d, end_d = parse_date_range(item["date"])
        show = Show(
            title=item["title"],
            start_date=start_d,
            end_date=end_d,
            location=item["location"],
            price=item["price"],
            status="upcoming",
            image_path=item["image_path"],
        )
        upcoming_shows_objs.append(show)

    # -------------------------------------------------------------------------
    # 4) 定义“艺术家”（Artists）数据
    #   仅需要 name, image_path, link
    # -------------------------------------------------------------------------
    raw_artists = [
        {"name": "林俊杰", "image_path": "artists/JJ.JPG", "link": "/artist/jj"},
        {"name": "周杰伦", "image_path": "artists/Jay.JPG", "link": "/artist/jay"},
        {"name": "陶喆", "image_path": "artists/DT.JPG", "link": "/artist/dt"},
        {"name": "王力宏", "image_path": "artists/WLH.JPG", "link": "/artist/wlh"},
        {"name": "邓紫棋", "image_path": "artists/GEM.JPG", "link": "/artist/gem"},
        {"name": "孙燕姿", "image_path": "artists/SYZ.JPG", "link": "/artist/syz"},
        {"name": "五月天", "image_path": "artists/WYT.JPG", "link": "/artist/wyt"},
        {"name": "单依纯", "image_path": "artists/SYC.JPG", "link": "/artist/syc"},
    ]

    artists_objs = []
    for item in raw_artists:
        artist = Artist(
            name=item["name"],
            image_path=item["image_path"],
            link=item["link"],
        )
        artists_objs.append(artist)

    # -------------------------------------------------------------------------
    # 5) 将所有对象一次性插入数据库
    # -------------------------------------------------------------------------
    db.session.add_all(hot_shows_objs + upcoming_shows_objs + artists_objs)
    db.session.commit()

    print("Seed data inserted successfully.")  


if __name__ == "__main__":
    seed()
