import pandas as pd
import os
import json

class DataHandler:
    def __init__(self):
        pass
    
    def load_csv(self, csv_path):
        """CSVファイルをロード"""
        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception as e:
            print(f"CSVロードエラー: {e}")
            return None
    
    def load_template(self, template_path):
        """テンプレートJSONファイルをロード"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
            return template
        except Exception as e:
            print(f"テンプレートロードエラー: {e}")
            return self.create_default_template()
    
    def save_template(self, template, template_path):
        """テンプレートをJSON形式で保存"""
        try:
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"テンプレート保存エラー: {e}")
            return False
    
    def create_default_template(self):
        """デフォルトテンプレートを生成"""
        return {
            "name": "デフォルトテンプレート",
            "background": "",
            "product_position": (250, 150),
            "product_size": (300, 300),
            "text_elements": [
                {
                    "text": "${name}",
                    "position": (250, 480),
                    "font": "arial.ttf",
                    "font_size": 24,
                    "color": (0, 0, 0)
                },
                {
                    "text": "¥${price}",
                    "position": (250, 520),
                    "font": "arial.ttf",
                    "font_size": 32,
                    "color": (255, 0, 0)
                }
            ],
            "image_elements": []
        }
