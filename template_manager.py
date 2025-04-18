import os
import json
from data_handler import DataHandler

class TemplateManager:
    def __init__(self, templates_dir="templates"):
        # 絶対パスを取得
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(script_dir, templates_dir)
        self.data_handler = DataHandler()
        
        # テンプレートディレクトリがなければ作成
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # デフォルトテンプレートがなければ作成
        default_path = os.path.join(self.templates_dir, "default.json")
        if not os.path.exists(default_path):
            template = self.data_handler.create_default_template()
            self.data_handler.save_template(template, default_path)
    
    def get_template_list(self):
        """利用可能なテンプレート一覧を取得"""
        templates = []
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".json"):
                template_path = os.path.join(self.templates_dir, filename)
                try:
                    template = self.data_handler.load_template(template_path)
                    templates.append({
                        "name": template.get("name", filename),
                        "path": template_path
                    })
                except:
                    pass
        return templates
    
    def create_template(self, template_data, name):
        """新しいテンプレートを作成"""
        filename = f"{name.replace(' ', '_')}.json"
        template_path = os.path.join(self.templates_dir, filename)
        return self.data_handler.save_template(template_data, template_path)
    
    def update_template(self, template_data, template_path):
        """既存のテンプレートを更新"""
        return self.data_handler.save_template(template_data, template_path)
    
    def delete_template(self, template_path):
        """テンプレートを削除"""
        try:
            os.remove(template_path)
            return True
        except Exception as e:
            print(f"テンプレート削除エラー: {e}")
            return False
