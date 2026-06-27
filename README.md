# 个人信息管理系统

基于 Django 的个人信息管理系统，支持用户注册登录、个人信息管理、日程安排管理。

## 功能

- 用户注册与登录
- 个人信息查看与编辑
- 日程增删改查
- 日程搜索与分页
- 中英双语支持

## 快速开始

```bash
# 安装依赖
uv sync

# 初始化数据库
uv run python manage.py migrate

# 创建管理员
uv run python manage.py createsuperuser

# 启动服务
uv run python manage.py runserver
```

访问 http://127.0.0.1:8000/

## 配置

复制 `.env.example` 为 `.env`，按需修改配置。

## 技术栈

- Python 3.12+
- Django 6.0
- Bootstrap 5
- SQLite（默认）/ MySQL / PostgreSQL

## 国际化

系统支持中文和英文。通过导航栏的语言切换器切换语言。

## 英文文档

See [README_EN.md](README_EN.md) for English documentation.

## License

MIT
