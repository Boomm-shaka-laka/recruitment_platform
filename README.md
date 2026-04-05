# recruitment_platform

```bash
pip install -r requirements.txt
```

## WSL2 手动安装 Playwright Chromium 完整流程

### 1. 获取下载链接
```bash
conda activate platform  # 激活你的环境
playwright install --dry-run chromium
```
输出里会看到两个下载链接，复制备用：
```
chrome-linux64.zip          → https://cdn.playwright.dev/...
chrome-headless-shell-linux64.zip → https://cdn.playwright.dev/...
```

---

### 2. Windows 下载文件
在 Windows 浏览器里（走代理）直接访问上面两个链接下载，保存到桌面或任意目录。

---

### 3. WSL2 里解压到指定目录
```bash
# 创建目录
mkdir -p ~/.cache/ms-playwright/chromium-1208
mkdir -p ~/.cache/ms-playwright/chromium_headless_shell-1208

# 解压（注意：盘符小写，无冒号）
unzip /mnt/e/Desktop/chrome-linux64.zip \
  -d ~/.cache/ms-playwright/chromium-1208/

unzip /mnt/e/Desktop/chrome-headless-shell-linux64.zip \
  -d ~/.cache/ms-playwright/chromium_headless_shell-1208/

# 创建标记文件（让 Playwright 识别为已安装）
touch ~/.cache/ms-playwright/chromium-1208/INSTALLATION_COMPLETE
touch ~/.cache/ms-playwright/chromium_headless_shell-1208/INSTALLATION_COMPLETE

# 添加可执行权限
chmod +x ~/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome
chmod +x ~/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell
```

---

### 4. 安装缺失的系统依赖库
```bash
sudo /home/cjy/anaconda3/envs/platform/bin/playwright install-deps chromium
```

---

### 5. 验证
```bash
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto('https://example.com')
    print(page.title())  # 输出 Example Domain 即成功
    b.close()
"
```

---

### 注意事项
- Windows 盘符在 WSL2 里统一用 **小写 + 无冒号**，如 `E:\` → `/mnt/e/`
- `playwright install` 会**删除**不符合结构的目录，所以每次重装前不要手动乱放文件
- 如果终端有残留代理变量导致连接失败，用 `unset https_proxy http_proxy` 清除后再操作