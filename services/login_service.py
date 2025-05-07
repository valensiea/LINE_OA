import requests
import time
class LoginService:
    def __init__(self, login_url, username, password):
        self.login_url = login_url
        self.username = username
        self.password = password
        self.token = None
        self.cookies = None
        self.token_timestamp = 0
        self.token_lifetime = 60 * 60  # 1 ชั่วโมง (แก้ตามจริงถ้าระบบบอกอายุ token)

    def authenticate(self):
        payload = {
            "username": self.username,
            "password": self.password,
            "ref": "android"  # ✅ เพิ่ม ref ให้เหมือนฟังก์ชันปกติ
        }
        response = requests.post(self.login_url, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("accessToken")
            self.cookies = response.cookies.get_dict()
            self.token_timestamp = time.time()
            print("✅ Token refreshed.")
        else:
            print("❌ Login failed:", response.status_code, response.text)

    def get_token(self):
        # ถ้า token หมดอายุ ให้ login ใหม่
        if self.token is None or (time.time() - self.token_timestamp) > self.token_lifetime:
            print("🔄 Token expired or missing. Re-authenticating...")
            self.authenticate()
        return self.token

    def get_cookies(self):
        if self.cookies is None:
            self.authenticate()
        return self.cookies