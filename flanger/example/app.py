
# 引入FlangerApp
from flanger.app import FlangerApp
from models import *

# 实例化FlangerApp (Flanger核心对象)，当Flask一样用就行
app = FlangerApp(__name__)

# 给app写入配置文件 (当Flask一样用)
app.config.from_object("settings")

# ORM，Migrate, Script 等flask的插件 该怎么用仍然怎么用
db.init_app(app)

# 初始化Flanger的功能（必须在导入配置之后init）
app.init()


if __name__ == '__main__':
    # 启动开发服务器
    app.run(debug=True,host='0.0.0.0', port=28080)
