# Xiaoyuzhou Podcast Episodes Downloader

🎵 自动下载网页内嵌音频的Python脚本，支持动态加载页面

灵感来源：小红书账户@南瓜大王，手动下载方法见：1 南瓜大王发布了一篇小红书笔记，快来看吧！ 😆 267IUFQeIo1k6ZE 😆 http://xhslink.com/a/tABozuIps5r5，复制本条信息，打开【小红书】App查看精彩内容！

## 功能特性

- ✅ 自动检测网页中的音频资源（包括动态加载内容）
- ✅ 支持多种音频源格式：
  - 标准HTML5 `<audio>`标签
  - 嵌套`<source>`标签
  - JavaScript动态加载的音频
- ✅ 智能文件名生成：
  - 基于网页标题自动命名
  - 自动过滤非法字符
  - 自动处理重名文件
- ✅ 支持主流浏览器渲染（Chrome无头模式）
- ✅ 下载进度实时显示
- 📂 自动保存到系统下载目录

## 快速开始

### 前置要求

- Python
- Chrome浏览器（[下载地址](https://www.google.com/chrome/)）
- ChromeDriver（[下载地址](https://chromedriver.chromium.org/)）(我没有专门下载过这个)

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/Jiangyue-Wang/dl_xiaoyuzhou
cd dl_xiaoyuzhou
```

2. 安装包
```bash
pip install -r requirements.txt
```

3. 配置Chrome Driver (一般不需要)
```bash
# Mac/Linux
mv chromedriver /usr/local/bin/

# Windows
# 将chromedriver.exe放入系统PATH路径
```

4. 运行
```bash
python dl.py
```

5. 根据系统指示粘贴url并设定下载目录即可

