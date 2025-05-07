import requests

class RepairService:
    def __init__(self, company_id, login_service):
        self.company_id = company_id
        self.base_url = f"https://testapi.systemstone.com/rest/11.4/company/{company_id}"
        self.login_service = login_service

    def _get_headers(self):
        token = self.login_service.token
        return {
            'Content-type': 'application/json; charset=UTF-8',
            'Authorization': f'Bearer {token}'
        }

    def _get_cookies(self):
        return self.login_service.get_cookies()

    def get_in_progress(self, user_id):
        url = f"{self.base_url}/repair/in-progress/{user_id}"
        response = requests.get(url, headers=self._get_headers(), cookies=self._get_cookies())
        if response.status_code != 200:
            self.login_service.authenticate()
            response = requests.get(url, headers=self._get_headers(), cookies=self._get_cookies())
            print(response.status_code)
        return response.json()

    def get_completed(self, user_id):
        url = f"{self.base_url}/repair/recent-completed/{user_id}"
        response = requests.get(url, headers=self._get_headers(), cookies=self._get_cookies())
        if response.status_code != 200:
            self.login_service.authenticate()
            response = requests.get(url, headers=self._get_headers(), cookies=self._get_cookies())
            print(response.status_code)
        return response.json()
