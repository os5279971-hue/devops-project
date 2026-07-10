#!/bin/bash
BACKUP_DIR="/home/yaoqi/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_USER="root"
DB_PASS="rootpass123"       # 改成你实际的密码
DB_NAME="yaoqi_db"

mkdir -p $BACKUP_DIR

# 强制走 TCP，端口 3306（默认）
mysqldump -h 127.0.0.1 -u$DB_USER -p$DB_PASS --single-transaction $DB_NAME > $BACKUP_DIR/${DB_NAME}_${DATE}.sql

# 保留 7 天备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup completed: ${DB_NAME}_${DATE}.sql"
