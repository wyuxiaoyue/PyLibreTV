import os


def getint(key, default):
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
}

PASSWORD = os.getenv("PASSWORD", "")

PORT = getint("PORT", 8080)

REQUEST_TIMEOUT = getint("REQUEST_TIMEOUT", 5)
RETRY_TIMES = getint("RETRY_TIMES", 2)  # 初始请求 + 1次重试 = 总共2次
