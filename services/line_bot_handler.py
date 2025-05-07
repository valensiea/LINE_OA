import requests

class LineBotHandler:
    def __init__(self, channel_token):
        self.channel_token = channel_token

    def reply_message(self, reply_token, text):
        url = "https://api.line.me/v2/bot/message/reply"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.channel_token}"
        }
        data = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": text}]
        }
        requests.post(url, headers=headers, json=data)

    def send_flex_message(self, reply_token, bubbles, alt_text):
        flex_message = {"type": "carousel", "contents": bubbles}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.channel_token}"
        }
        body = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "flex",
                    "altText": alt_text,
                    "contents": flex_message
                }
            ]
        }
        requests.post('https://api.line.me/v2/bot/message/reply',
                      headers=headers, json=body)

    def get_profile(self, user_id):
        headers = {"Authorization": f"Bearer {self.channel_token}"}
        url = f"https://api.line.me/v2/bot/profile/{user_id}"
        return requests.get(url, headers=headers).json()

    def push_message(self, user_id, message):
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.channel_token}"
        }
        body = {"to": user_id, "messages": [{"type": "text", "text": message}]}
        requests.post(url, headers=headers, json=body)
