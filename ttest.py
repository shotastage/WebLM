import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_with_beautifulsoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # ここでBeautiful Soupを使用してスクレイピングを行う
    # 例: タイトルを取得
    title = soup.title.string if soup.title else "No title found"
    return title

def scrape_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモードで実行
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        # JavaScriptの実行を待つ
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # ここでSeleniumを使用してスクレイピングを行う
        # 例: タイトルを取得
        title = driver.title
        return title
    finally:
        driver.quit()

def hybrid_scrape(url, needs_javascript=False):
    if needs_javascript:
        return scrape_with_selenium(url)
    else:
        return scrape_with_beautifulsoup(url)

# 使用例
static_url = "https://ja.wikipedia.org/wiki/Apple"
dynamic_url = "https://shotach.com/posts/dht-nc"

print(f"Static page title: {hybrid_scrape(static_url)}")
print(f"Dynamic page title: {hybrid_scrape(dynamic_url, needs_javascript=True)}")
