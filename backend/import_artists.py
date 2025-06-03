from datetime import datetime
from backend.app import create_app
from backend.extensions import db
from backend.models import Artist

# 1. 通过工厂函数创建 Flask 应用，并推入应用上下文
app = create_app()
with app.app_context():
    # 2. 定义要导入的艺术家数据列表
    artists_data = [
        {
            "name": "林俊杰",
            "image_path": "artists/JJ.JPG",
            "link": "/artist/jj"
        },
        {
            "name": "周杰伦",
            "image_path": "artists/Jay.JPG",
            "link": "/artist/jay"
        },
        {
            "name": "陶喆",
            "image_path": "artists/DT.JPG",
            "link": "/artist/dt"
        },
        {
            "name": "王力宏",
            "image_path": "artists/WLH.JPG",
            "link": "/artist/wlh"
        },
        {
            "name": "邓紫棋",
            "image_path": "artists/GEM.JPG",
            "link": "/artist/gem"
        },
        {
            "name": "孙燕姿",
            "image_path": "artists/SYZ.JPG",
            "link": "/artist/syz"
        },
        {
            "name": "五月天",
            "image_path": "artists/WYT.JPG",
            "link": "/artist/wyt"
        },
        {
            "name": "单依纯",
            "image_path": "artists/SYC.JPG",
            "link": "/artist/syc"
        },
    ]

    # 3. 循环插入每一条记录
    for entry in artists_data:
        artist = Artist(
            name=entry["name"],
            image_path=entry["image_path"],
            link=entry["link"],
            # 如果你的模型中没有 automatic default for created_at/updated_at，
            # 可以手动指定下方两行；否则可删除这两个参数
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(artist)

    # 4. 提交事务
    db.session.commit()
    print(f"成功插入 {len(artists_data)} 条 artist 记录。")
