from flask import Flask
import pymysql
import redis

app = Flask(__name__)

DB_HOST = 'localhost'
DB_USER = 'yaoqi'
DB_PASSWORD = 'Yaoqi123!'
DB_NAME = 'yaoqi_db'

# Redis 配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'

def get_db_connection():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    return conn

def get_redis_client():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    return r

@app.route('/')
def hello():
    try:
        # 先查 Redis 缓存
        r = get_redis_client()
        cached_html = r.get('user_list_cache')
        if cached_html:
            return cached_html

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT VERSION()")
        mysql_version = cursor.fetchone()[0]
        conn.close()

        html = f'<h1>Hello, 姚麒!</h1>'
        html += f'<p>数据库连接成功！当前数据库：yaoqi_db | MySQL 版本：{mysql_version}</p>'
        html += f'<p>用户总数：<b>{user_count}</b></p>'
        html += '<hr>'
        html += '<h2>用户列表</h2>'
        html += '<table border="1" cellpadding="5">'
        html += '<tr><th>ID</th><th>姓名</th><th>邮箱</th><th>创建时间</th></tr>'
        for user in users:
            html += f'<tr><td>{user[0]}</td><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td></tr>'
        html += '</table>'

        # 缓存到 Redis，有效期 60 秒
        r.setex('user_list_cache', 60, html)

        return html

    except Exception as e:
        return f'数据库或 Redis 连接失败，错误信息：{str(e)}'

@app.route('/logs')
def show_logs():
    import os
    logs = {}
    log_dir = '/app/scripts'
    if os.path.exists(log_dir):
        for filename in sorted(os.listdir(log_dir)):
            if filename.endswith('.log'):
                filepath = os.path.join(log_dir, filename)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                logs[filename] = lines[-20:]
    else:
        logs['error'] = ['日志目录不存在']

    html = '<h1>运维脚本运行日志</h1>'
    for name, lines in logs.items():
        html += f'<h2>{name}</h2><pre>' + ''.join(lines) + '</pre><hr>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
