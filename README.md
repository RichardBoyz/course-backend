# 指南
## 環境
- python 建議 3.10 以上

```pip install poetry```

- 在此專案目錄下執行 ```poetry shell```
- 接著執行 ```poetry install```

- 專案目錄底下建立 db.sqlite3 檔案
  -

## 執行

- 執行 ``` python manage.py migrate

- 會在 vscode 右下看到執行環境 3.10.x 64-bit 請點選後選擇 3.10.x (course-...:Poetry)
  -

- 接著產生launch.json 執行 debugger 即可

- 如果沒辦法選擇 poetry 環境，請用 pip install 安裝以下 package 後執行 ``` python manage.py runserver ```
    ```
    Django = "^5.0.3"
    djangorestframework = "^3.15.1"
    django-filter = "^24.2"
    django-cors-headers = "^4.3.1"
    PyJWT = "^2.8.0"
    ```
