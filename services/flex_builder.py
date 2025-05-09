class FlexBuilder:
    @staticmethod
    def build_report_card(data):
        bubbles = []
        for idx, item in enumerate(data, start=1):
            bubble = {
                "type": "bubble",
                "size": "kilo",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {"type": "text", "text": f"ลำดับที่: {idx}", "weight": "bold", "size": "sm", "color": "#3366CC"},
                        {"type": "text", "text": f"ผู้รับผิดชอบ: {item.get('assigneeName')}", "weight": "bold", "size": "sm"},
                        {"type": "text", "text": f"เบอร์โทร: {item.get('phone')}", "size": "sm", "color": "#555555"},
                        {"type": "text", "text": f"วันที่แจ้งซ่อม: {item.get('createDate')}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"วันที่เริ่มทำ: {item.get('responseDate')}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"วันที่ปิด: {item.get('returnDate')}", "size": "sm", "wrap": True}
                    ]
                }
            }
            bubbles.append(bubble)
        return bubbles
