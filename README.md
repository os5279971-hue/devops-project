<img width="707" height="601" alt="01-Web应用首页" src="https://github.com/user-attachments/assets/efdff31d-e6aa-4d3d-8199-8fbb01cf5037" />
<img width="1237" height="923" alt="02-运维日志页面" src="https://github.com/user-attachments/assets/e13ca230-a0cb-4734-b194-34ddd6dcf265" />
<img width="1907" height="917" alt="03-Grafana监控仪表板" src="https://github.com/user-attachments/assets/603e4608-f9e8-4cbf-82f9-aa220e0a4c4b" />
<img width="1893" height="452" alt="04-Prometheus_up查询" src="https://github.com/user-attachments/assets/83b83d8f-541b-4c5f-8b8f-94dc11525835" />
<img width="1908" height="388" alt="05-Prometheus_身份验证" src="https://github.com/user-attachments/assets/16f54e3d-136e-49fc-be92-d1fdd47bba38" />
<img width="1022" height="95" alt="06-Crontab任务列表" src="https://github.com/user-attachments/assets/df6fec0c-fd74-4a0d-9acb-559a58843406" />
<img width="926" height="267" alt="k8s-pods png" src="https://github.com/user-attachments/assets/ac64f4cc-ec72-49c0-9550-bb052d369f8c" />
<img width="1891" height="518" alt="k8s-nginx-demo png" src="https://github.com/user-attachments/assets/a0066243-8ae4-4946-a8c6-fdc256e03a8c" />

# 姚麒 · 运维自动化管理平台

> Flask + MySQL + Redis + Nginx + Podman | 个人运维实战项目  
> 🔗 GitHub：[os5279971-hue/devops-project](https://github.com/os5279971-hue/devops-project)  
> 🌐 线上演示：[https://123.57.229.2](https://123.57.229.2)（主页） | [https://123.57.229.2/logs](https://123.57.229.2/logs)（运维日志）
> Prometheus控制台[http://123.57.229.2:9090] |Grafana监控大屏[http://123.57.229.2:3000]

---

## 🎯 项目简介

本项目是一个从零搭建的**运维自动化 Web 平台**，用于展示 Linux 运维、Python 开发、数据库管理、缓存优化、容器化部署等综合能力。  
所有服务均采用 Podman 容器化，代码托管于 GitHub，支持一键部署。

---
## ⚙️ Ansible 自动化部署

- **文件**：`ansible/init-server.yml`
- **功能**：一键从 GitHub 拉取项目代码、构建 Docker 镜像、停止旧容器并启动新容器，实现服务更新自动化。
- **运行方式**：
  ```bash
  cd ansible
  ansible-playbook init-server.yml
## 📊 技术栈（更新于 2026-07-09）

| 层级 | 技术 | 说明 |
|------|------|------|
| **Web 框架** | Python 3.9 + Flask | 主应用，MVC 模式 |
| **WSGI 服务器** | Gunicorn | 多 worker 生产环境运行 |
| **反向代理** | Nginx | HTTPS 终结，反代至 Gunicorn |
| **数据库** | MySQL 8.0 (容器) | 用户数据持久化，密码认证 |
| **缓存** | Redis 7 (容器) | 首页用户列表缓存，TTL 60s |
| **容器引擎** | Podman | 全部服务容器化，`--network host` |
| **版本控制** | Git + GitHub | 代码托管，分支管理 |
| **系统** | CentOS / Alibaba Cloud ECS | 阿里云服务器 |

---

## 🚀 核心功能

- ✅ **用户列表**  
  从 MySQL 读取真实用户表，支持缓存自动刷新（60 秒有效期），缓存命中后响应速度提升 80% 以上。

- ✅ **运维日志在线查看** (`/logs`)  
  实时展示服务器上运维脚本（定时备份等）的运行日志，方便排查问题。

- ✅ **容器化一键部署**  
  使用 Dockerfile 构建自定义镜像，搭配 Podman 启动，三行命令即可重建环境。

- ✅ **HTTPS 安全访问**  
  通过 Nginx 配置自签名证书，保护数据传输安全。

---

## 📈 项目成长日志（关键节点）

- **模块 1-3**：阿里云 ECS 基础环境搭建，Podman 入门
- **模块 4-6**：Flask 应用 + Gunicorn + Nginx 上线，HTTPS 配置
- **模块 7-9**：MySQL 容器化，用户表设计，日志页面，Git 版本管理
- **模块 10**（2026-07-09）：**集成 Redis 缓存**，解决容器丢失、密码回溯、版本冲突等一系列生产问题

> 详细的踩坑记录和解决方案请查阅 [CHANGELOG.md](./CHANGELOG.md)

---

## ⚙️ 快速部署（在新服务器上复现）

```bash
# 克隆项目
git clone git@github.com:os5279971-hue/devops-project.git /home/yaoqi/projects
cd /home/yaoqi/projects

# 1. 启动 MySQL
podman run -d --name mymysql \
  -v /var/lib/mysql:/var/lib/mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=rootpass123 \
  -e MYSQL_DATABASE=yaoqi_db \
  -e MYSQL_USER=yaoqi \
  -e MYSQL_PASSWORD='Yaoqi123!' \
  --restart=always \
  mysql:8.0

# 2. 启动 Redis
podman run -d --name myredis \
  -p 6379:6379 \
  redis:latest --requirepass 123456

# 3. 构建 Flask 应用镜像并运行
podman build -t yaoqi-app:v4 .
podman run -d --name yaoqi-app --network host \
  -v /home/yaoqi/scripts:/app/scripts \
  yaoqi-app:v4

# 4. 配置 Nginx 反代（示例配置见项目内 nginx.conf 文件）
sudo nginx -s reload
📁 项目结构
Text
/home/yaoqi/projects/
├── app.py              # Flask 主程序（含 Redis 缓存逻辑）
├── requirements.txt    # Python 依赖
├── Dockerfile          # 容器构建定义
├── README.md           # 项目总览（本文件）
├── CHANGELOG.md        # 完整开发日志与排错记录
├── logs.md             # 早期手动操作笔记
├── scripts/            # 运维脚本（定时备份等）
└── nginx.conf          # Nginx 参考配置
🙋‍♂️ 关于作者
姚麒 | 运维开发工程师

本项目持续迭代，旨在沉淀运维与开发实践能力，欢迎 Issues 交流。

