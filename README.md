# 1Moment
记录生活之美，留住珍贵时刻 —— 1Monent

1Moment是一个基于Django和Vue3的全栈项目。

## 项目结构

```
1Moment/
├── moment/                 # Django后端项目
│   ├── db.sqlite3         # SQLite数据库文件
│   ├── manage.py          # Django项目管理脚本
│   ├── photos/            # 照片管理应用
│   │   ├── models.py      # 数据模型
│   │   ├── api.py        # API接口
│   │   └── migrations/    # 数据库迁移文件
│   └── moment/            # Django项目配置目录
│
└── web/                   # Vue3前端项目
    ├── public/            # 静态资源目录
    ├── src/              # 源代码目录
    │   ├── components/   # Vue组件
    │   │   ├── PhotoUpload.vue    # 照片上传组件
    │   │   └── PhotoGrid.vue      # 照片网格展示组件
    │   └── assets/       # 静态资源
    │       └── main.css  # 全局样式（包含Tailwind配置）
    ├── index.html        # 入口HTML文件
    ├── package.json      # 项目依赖配置
    ├── tailwind.config.js # Tailwind CSS配置
    └── vite.config.ts    # Vite构建工具配置
```

## 技术栈

### 后端
- Django 4.2.19  
- django-ninja 1.3.0
- Pillow
- SQLite

### 前端
- Vue 3
- TypeScript
- Vite
- Tailwind CSS
- DaisyUI
- Heroicons

## 功能实现

### 后端API接口
1. 照片管理
   - POST /api/photos/upload - 上传照片
   - GET /api/photos - 获取照片列表
   - GET /api/photos/{photo_id} - 获取照片详情

2. 相册管理
   - POST /api/albums - 创建相册
   - GET /api/albums - 获取相册列表
   - POST /api/photos/{photo_id}/albums/{album_id} - 添加照片到相册

3. 标签管理
   - POST /api/tags - 创建标签
   - GET /api/tags - 获取标签列表
   - POST /api/photos/{photo_id}/tags/{tag_name} - 为照片添加标签

### 前端组件
1. PhotoUpload组件
   - 支持拖拽上传
   - 支持多文件上传
   - 实时上传进度显示
   - 支持取消上传

2. 样式框架
   - 使用Tailwind CSS实现响应式布局
   - 使用DaisyUI组件库美化界面
   - 自定义组件样式类
     ```css
     .card-photo - 照片卡片样式
     .photo-grid - 响应式照片网格布局
     .btn-primary - 主要按钮样式
     ```

## 开发进度
1. ✅ 后端框架搭建
   - 完成数据模型设计（Photo、Album、Tag）
   - 实现基础API接口
     - 照片上传与管理
     - 相册创建与管理
     - 标签创建与管理
   - 配置媒体文件处理
   - 支持照片缩略图生成

2. ✅ 前端框架搭建
   - 集成Vue3和TypeScript
   - 集成Tailwind CSS和DaisyUI
   - 实现基础路由配置
     - 首页 (/)
     - 照片列表 (/photos)
     - 照片上传 (/upload)
     - 关于页面 (/about)

3. 🚧 进行中
   - 照片上传组件开发
   - 照片网格展示组件
   - 相册管理界面
   - 标签管理界面
   - 前后端API对接

4. ⏳ 待开发
   - 用户认证系统
   - 照片编辑功能
   - 照片搜索功能
   - 照片EXIF信息展示
   - 照片地理位置展示
   - 批量操作功能
   - 分享功能
