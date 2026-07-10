# 项目成长日志 (CHANGELOG)

此文件按时间倒序记录了项目各阶段的建设过程、遇到的问题及解决方法，是项目最原始的“成长档案”。

---

## 2026-07-08 ~ 2026-07-09 | 模块 10：Redis 缓存集成

### ✅ 主要工作
- 为首页用户列表增加 Redis 缓存（键：`user_list_cache`，过期时间 60 秒）
- 解决因之前 MySQL 容器丢失导致的数据库连接异常、密码遗忘、版本冲突等一系列生产问题
- 重构应用镜像为 `yaoqi-app:v4`，更新依赖，修复代码缩进错误
- 保持页面简洁，仅核心功能 + Redis 缓存

### ❌ 遇到的问题 & 解决方法

| 时间 | 问题描述 | 原因分析 | 解决步骤 |
|------|----------|----------|----------|
| 07-09 上午 | 网站 502，Gunicorn 日志显示 `IndentationError: expected an indented block` | 手动添加 Redis 代码块时缩进错误（Tab/空格混用） | 使用正确缩进的完整 `app.py` 覆盖原文件 |
| 07-09 上午 | Flask 运行时提示 `ModuleNotFoundError: No module named 'redis'` | `requirements.txt` 中未包含 `redis` 依赖 | 添加 `redis` 到 `requirements.txt` 并重新构建镜像 |
| 07-09 上午 | 忘记 MySQL 用户 `yaoqi` 的密码 | 长时间未登录，密码未记录 | 通过 `podman exec -it mymysql mysql -uroot -p'Yaoqi123!'` 验证；若仍不匹配则启动带 `--skip-grant-tables` 的临时容器重置密码 |
| 07-09 上午 | 启动临时 MySQL 容器时报端口冲突，无法绑定 3306 | 宿主机自带的系统 mysql 服务占用了 3306 | 执行 `systemctl stop mysqld && systemctl disable mysqld` 关闭并禁用系统服务 |
| 07-09 上午 | 挂载旧数据目录启动正式容器后立即退出，日志报 `InnoDB initialization has started... Cannot boot server version 80027 on data directory built by version 80045` | 宿主机数据目录是 MySQL 8.0.45 版本初始化的，而拉取的 `mysql:8.0` 镜像实际版本为 8.0.27，低版本无法读取高版本数据文件 | 备份旧数据目录 `mv /var/lib/mysql /var/lib/mysql_old`，新建空目录，用 8.0.27 镜像初始化新数据库 |
| 07-09 上午 | 尝试拉取 `mysql:8.0.45` 镜像以匹配旧数据版本，但失败 | 阿里云镜像加速器 `szwm34t9.mirror.aliyuncs.com` 尚未缓存该版本；临时注释掉加速器后直连 Docker Hub 时，ECS 网络超时（被墙） | 放弃匹配旧版本，改用 `mysql:8.0`（8.0.27）重建，旧数据保留备份 |
| 07-09 下午 | 新建 MySQL 后网页报错 `Table 'yaoqi_db.users' doesn't exist` | 新数据库为空，未创建表结构 | 执行 SQL 创建 `users` 表并插入示例数据 |
| 07-09 下午 | 美化前端页面后用户反馈“看起来高级但没有用” | 添加了虚构的企业级字段和员工数据，与项目实际情况不符 | 恢复原始简洁页面，只保留核心功能 + Redis 缓存 |
| 07-09 晚 | `git push` 卡住，长时间无响应 | 服务器通过 HTTPS 协议连接 GitHub 受网络影响，卡在数据传输阶段 | 切换为 SSH 协议推送：生成 SSH 密钥，添加到 GitHub，`git remote set-url` 修改远程地址，解决卡死 |

---

## 2026-07-07 前 | 模块 1-9：基础架构搭建（概要）

- **模块 1-3**：阿里云 ECS 购买与初始化；安装 Podman、Git、Python；学习容器基础命令
- **模块 4-6**：编写第一个 Flask 应用；使用 Gunicorn 启动；编写 Dockerfile 构建镜像；配置 Nginx 反代及 HTTPS 自签名证书，实现域名访问
- **模块 7-9**：部署 MySQL 容器，创建数据库和用户；Flask 连接 MySQL 展示用户列表；实现数据持久化；增加 `/logs` 路由查看运维脚本日志；配置 Git 并推送至 GitHub

> 早期详细操作手记详见仓库内的 `logs.md` 文件。

