import requests
from bs4 import BeautifulSoup
import os
import re
import platform
from pathlib import Path
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_default_download_dir():
    """获取系统默认下载目录"""
    system = platform.system()
    if system == "Windows":
        return str(Path.home() / "Downloads")
    elif system == "Darwin":  # macOS
        return str(Path.home() / "Downloads")
    else:  # Linux/Unix
        return str(Path.home() / "Downloads")

def sanitize_filename(title):
    """清理文件名中的非法字符"""
    cleaned = re.sub(r'[\\/*?:"<>|]', '', title)
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned[:100].strip('_')

def get_dynamic_html(url):
    print("🔄 Rendering page with browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html

def find_audio_sources(soup):
    sources = []
    
    # 标准audio标签
    for audio in soup.find_all('audio'):
        if audio.get('src'):
            sources.append(audio['src'])
        for source in audio.find_all('source'):
            if source.get('src'):
                sources.append(source['src'])
    
    # JavaScript中的音频URL
    for script in soup.find_all('script'):
        if script.string:
            matches = re.findall(r'(https?://[^\s"\'\\]+?\.(?:mp3|m4a|wav|aac))', script.string)
            sources.extend(matches)
    
    return list(set(sources))

def download_audio(url, download_dir=None):
    # 设置下载目录
    if not download_dir:
        download_dir = get_default_download_dir()
    
    download_path = Path(download_dir)
    try:
        download_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 下载目录：{download_path.resolve()}")
    except Exception as e:
        print(f"❌ 无法创建目录：{str(e)}")
        return

    try:
        html = get_dynamic_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.title.string.strip() if soup.title else 'untitled'
        print(f"📝 网页标题：{title}")
        
        audio_sources = find_audio_sources(soup)
        print(f"🔍 找到 {len(audio_sources)} 个音频源")
        
        if not audio_sources:
            print("❌ 未找到有效音频链接")
            return

        filename_base = sanitize_filename(title)
        ext = '.m4a'

        for index, audio_url in enumerate(audio_sources):
            full_audio_url = urljoin(url, audio_url)
            print(f"🌐 正在处理：{full_audio_url}")
            
            # 生成文件名
            filename = f"{filename_base}_{index}{ext}" if len(audio_sources) > 1 else f"{filename_base}{ext}"
            full_path = download_path / filename
            
            # 处理重名文件
            counter = 1
            while full_path.exists():
                new_filename = f"{filename_base}_{index}_{counter}{ext}"
                full_path = download_path / new_filename
                counter += 1

            # 下载文件
            print(f"⬇️ 下载到：{full_path}")
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                    'Referer': url
                }
                
                with requests.get(full_audio_url, headers=headers, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    with open(full_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"✅ 保存成功\n")
                
            except Exception as e:
                print(f"❌ 下载失败：{str(e)}\n")

    except Exception as e:
        print(f"⚠️ 发生错误：{str(e)}")

if __name__ == "__main__":
    target_url = input("请输入网页URL: ")
    
    # 获取自定义下载路径
    custom_dir = input(f"输入下载目录（留空使用默认 {get_default_download_dir()}）: ").strip()
    
    download_audio(target_url, custom_dir if custom_dir else None)