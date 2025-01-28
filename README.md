# 智能春节祝福生成器

## 项目简介

这是一个单页web应用。用户可以输入接受人的名字，后端将会利用大语言模型的能力，生成一段定制的春节祝福语，告别无趣且千篇一律的复制黏贴。

除了生成春节祝福，还会根据接收人的名字，生成专属的春节对联图片，图片上是大模型定制的满足平仄要求还不缺文采的春联。生成的图片用户可以保存。

## 功能特点

- 个性化祝福语生成
- 定制春节对联生成
- 对联图片生成
- 历史记录查看
- 请求频率限制防止滥用

## 技术栈

- 后端：Flask
- 前端：HTML + CSS + JavaScript
- 数据库：SQLite3
- AI模型：OpenAI qwen-max-2025-01-25
- 图片处理：Pillow

## 环境要求

- Python 3.8+
- OpenAI API Key
- 华文行楷字体文件 (STXINGKA.TTF)

## 安装步骤

1. 克隆项目并进入项目目录：
```bash
git clone [项目地址]
cd 智能春节祝福生成器
```

2. 创建并激活虚拟环境：
```bash
conda create -n greeting python=3.8
conda activate greeting
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 文件中填入你的 OpenAI API Key

5. 准备字体文件：
   - 在 `static/fonts` 目录下放置 STXINGKA.TTF 字体文件

## 运行应用

1. 启动Flask应用：
```bash
python app.py
```

2. 在浏览器中访问：
```
http://localhost:5000
```

## 使用说明

1. 在输入框中输入接收祝福的人的名字
2. 可以选择性地添加额外要求
3. 点击"生成祝福"按钮
4. 等待生成结果
5. 可以保存生成的对联图片
6. 可以查看历史生成记录

## 注意事项

- 请确保有稳定的网络连接
- 需要有效的 OpenAI API Key
- 注意API使用频率限制
- 建议使用现代浏览器访问

## 开发说明

### 生成实现逻辑

得到了对方的姓名后，使用定制的prompt让模型生成回答，然后对回答进行解析，提取出祝福语。

再次使用定制的prompt让模型生成对联，然后对对联进行解析，提取出对联的上下联。
然后使用对联的上下联，使用已经准备好的模板，将文字对联添加到图片，得到对联图片。

### 前端设计

采用红色为主色调，使用css3动画来让页面动起来。设计简洁、大方、美观和现代化。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License



