# 项目踩坑日志 (CHANGELOG)

> 记录企业级 DevOps 运维平台从零搭建到完善全过程的错误、原因与解决方案，便于复盘与面试展示。

## 2026‑06‑30：ECS 环境搭建与 Flask 部署

### ① 无法通过公网 IP 访问 Flask 应用
- **现象**：执行 `python app.py` 后，浏览器访问 `http://123.57.229.2:5000` 无响应。
- **原因**：阿里云安全组未放行 5000 端口；另外 Flask 开发服务器默认监听 127.0.0.1，外网无法访问。
- **解决**：
  - 在阿里云控制台的安全组规则中添加入方向规则：允许 TCP 5000 端口。
  - 修改 `app.run()` 参数为 `host='0.0.0.0'`，使 Flask 监听所有网络接口。

### ② Nginx 反向代理后页面出现 502 Bad Gateway
- **现象**：配置 Nginx 反代后访问域名返回 502。
- **原因**：Nginx 配置中 `proxy_pass` 指向 `http://127.0.0.1:5000`，但 Gunicorn 未启动或未监听正确端口。
- **解决**：
  - 确认 Gunicorn 已启动并监听 5000 端口：`gunicorn -w 4 -b 0.0.0.0:5000 app:app`。
  - 检查 Nginx 配置文件中 `proxy_pass` 地址无误。

### ③ HTTPS 配置后浏览器提示证书不受信任
- **现象**：使用自签名证书后浏览器报安全警告。
- **原因**：自签名证书不被浏览器认可；Let‘s Encrypt 自动签发需要域名验证。
- **解决**：更换为 Let’s Encrypt 免费证书，并配置自动续期脚本（`certbot renew`）。

---

## 2026‑07‑01 ~ 07‑05：数据库与缓存集成

### ④ MySQL 8.0 远程连接报错 “Authentication plugin caching_sha2_password”
- **现象**：Python 连接 MySQL 时报错 `Authentication plugin caching_sha2_password cannot be loaded`。
- **原因**：MySQL 8.0 默认采用 `caching_sha2_password` 认证插件，较旧版本的 PyMySQL 不支持。
- **解决**：
  - 方案一：升级 PyMySQL 到最新版 `pip install --upgrade pymysql`。
  - 方案二：将用户认证插件改为 `mysql_native_password`：`ALTER USER 'yaoqi'@'%' IDENTIFIED WITH mysql_native_password BY 'Yaoqi123!';`

### ⑤ Redis 容器启动后无法通过 Python 客户端连接
- **现象**：`redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379`。
- **原因**：`redis` 容器运行时设置了 `--requirepass 123456`，但代码中未提供密码。
- **解决**：在 Redis 连接代码中加入 `password='123456'`：`redis.StrictRedis(host='localhost', port=6379, password='123456')`。

### ⑥ Docker 容器内访问宿主机 MySQL 被拒
- **现象**：Flask 容器中连接 `127.0.0.1:3306` 失败。
- **原因**：容器默认使用桥接网络，与宿主机网络隔离，`127.0.0.1` 指向容器自身而不是宿主机。
- **解决**：启动 Flask 容器时使用 `--network host` 模式，使容器直接使用宿主机网络栈，此时 `127.0.0.1:3306` 即可访问宿主机 MySQL。

---

## 2026‑07‑06 ~ 07‑08：Kubernetes 入门

### ⑦ kubectl 执行命令报错 “the server doesn’t have a resource type ‘deployment’”
- **现象**：`kubectl apply -f k8s-demo.yaml` 后提示找不到 Deployment 资源。
- **原因**：Docker Desktop 的 Kubernetes 功能未完全启用或集群未正常运行。
- **解决**：重启 Docker Desktop，在设置中勾选 “Enable Kubernetes”，等待集群启动完成后再试。

### ⑧ kubectl get pods 显示 “NotFound” 或 “No resources found”
- **现象**：已经 apply 了 YAML，但 `kubectl get pods` 无任何资源。
- **原因**：YAML 文件中 Deployment 名称拼写错误（例如写成了 `nginx-deploy` 而 Service 中引用的是 `nginx-deployment`）。
- **解决**：使用 `kubectl get deployments` 检查实际创建的 Deployment 名称，确保 Service 的 `selector` 匹配该名称。

### ⑨ NodePort 访问时连接被拒绝
- **现象**：通过 `localhost:30080` 访问 Nginx 失败。
- **原因**：NodePort 端口未在防火墙或安全组中放行；或者 Service 配置错误。
- **解决**：在本地防火墙放行 30080 端口；确认 Service 的 `targetPort` 与 Pod 容器端口一致。

---

## 2026‑07‑09 ~ 07‑10：Ansible 自动化部署

### ⑩ Ansible 执行报错：The Python 2 yum module is needed
- **现象**：`ansible-playbook init-server.yml` 运行到 `yum` 模块时抛出 `The Python 2 yum module is needed`。
- **原因**：CentOS 7 系统上 Ansible 默认使用 Python 3 执行模块，而 `yum` 模块依赖 Python 2 的 yum 库。
- **解决**：
  - 最终采用 **`raw` 模块** 直接运行系统命令：`raw: yum install -y git podman`，绕过 Python 版本依赖。
  - 尝试过 `vars: ansible_python_interpreter: /usr/bin/python2`，但某些环境仍因缺少 Python 2 的 yum 绑定而失败。

### ⑪ Ansible git 模块克隆仓库超时
- **现象**：`fatal: unable to access 'https://github.com/...': Failed to connect to github.com port 443`。
- **原因**：ECS 网络环境访问 GitHub HTTPS 端口不稳定，经常超时。
- **解决**：将仓库地址从 `https://` 改为 `git@github.com:os5279971-hue/devops-project.git`（SSH 协议），并确保目标主机（ECS 的 root 用户）已添加 GitHub SSH 公钥。

### ⑫ Playbook 缩进错误导致解析失败
- **现象**：`ansible-playbook` 报错 “Error: ... expected <block end> but found '-'”。
- **原因**：在终端直接粘贴 YAML 内容时，缩进（空格数量）被破坏，`tasks:` 下的 `- name:` 未对齐。
- **解决**：使用 `nano` 或 `vim` 编辑器手动调整缩进，每个 `- name:` 前保留 **4 个空格**（不能是 Tab）。

---

## 2026‑07‑11：项目整理与 Git 版本控制

### ⑬ git push 被拒绝 (non-fast-forward)
- **现象**：`error: failed to push some refs ... non-fast-forward`。
- **原因**：本地 `latest_branch` 与远程 `main` 分支没有共同历史，且远程有新的提交，本地落后。
- **解决**：使用 `git push -f origin latest_branch:main` 强制覆盖远程分支（确保本地内容正确后使用），或者先 `git pull --rebase` 再推送。

### ⑭ GitHub 上 README 图片无法显示
- **现象**：README 中引用的图片显示为叉号。
- **原因**：图片尚未上传到 GitHub 仓库的 `screenshots/` 目录，或者路径拼写不一致。
- **解决**：通过 GitHub 网页界面手动上传截图到 `screenshots/` 文件夹，并核对文件名与 README 中的引用一致。

---

## 2026‑07‑12 ~ 至今：文档与完善

### ⑮ README 编辑时终端卡死
- **现象**：使用 `cat > README.md << 'EOF'` 粘贴大量文本时终端无响应，无法继续输入。
- **原因**：粘贴内容中包含特殊字符（如反引号、EOF），提前终止了输入流。
- **解决**：改用 `nano README.md` 逐段粘贴，每段完成后保存（`Ctrl+O`）再继续，避免一次性粘贴过多内容。

### ⑯ 项目目录结构混乱，缺少必要文件
- **现象**：仓库中散落日志文件（`flask.log`, `gunicorn.log`）、`__pycache__` 目录，且缺少 `nginx.conf`, `docker-compose.yml` 等。
- **原因**：初期项目未规划清晰的目录结构，文件随意放置在根目录。
- **解决**：
  - 清理日志和缓存，将 `*.log` 和 `__pycache__` 加入 `.gitignore`。
  - 创建 `k8s/`、`ansible/`、`screenshots` 目录，将对应文件移入。
  - 从系统 `/etc/nginx/conf.d/myapp.conf` 复制为项目中的 `nginx.conf`。
  - 编写完整的 `docker-compose.yml` 描述现有服务。

---

> **持续更新中**：后续遇到的新问题会继续补充至此文档，作为个人技术积累与面试总结。
