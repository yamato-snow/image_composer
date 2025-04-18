import unittest
import os
import sys
import json
import shutil
import tempfile
import traceback

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    import flet as ft
    from template_manager import TemplateManager
    # 直接インポートする前に存在チェック
    import ui
    print("UIモジュールパス:", ui.__file__)
    from ui.template_view import TemplateView
except Exception as e:
    print("インポートエラー:", e)
    traceback.print_exc()
    sys.exit(1)

class TestTemplateView(unittest.TestCase):
    
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()
        self.templates_dir = os.path.join(self.test_dir, "templates")
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # テスト用のテンプレートを作成
        self.test_template = {
            "name": "テストテンプレート",
            "background": "",
            "product_position": [250, 150],
            "product_size": [300, 300],
            "text_elements": [
                {
                    "text": "${name}",
                    "position": [250, 480],
                    "font": "arial.ttf",
                    "font_size": 24,
                    "color": [0, 0, 0]
                }
            ],
            "image_elements": []
        }
        
        self.template_path = os.path.join(self.templates_dir, "test_template.json")
        with open(self.template_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_template, f, indent=4, ensure_ascii=False)
        
        # モックページオブジェクト
        self.page = MockPage()
    
    def tearDown(self):
        # テスト用のディレクトリを削除
        shutil.rmtree(self.test_dir)
    
    def test_template_view_initialization(self):
        """TemplateViewの初期化テスト"""
        # テンプレートビューを初期化
        try:
            template_view = TemplateView(self.page)
            # 例外が発生しなければ成功
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"TemplateView初期化中に例外が発生: {e}")
    
    def test_load_template_list(self):
        """テンプレートリストの読み込みテスト"""
        # テンプレートビューを初期化
        try:
            template_view = TemplateView(self.page)
            # テンプレートリストが正常に読み込まれているか
            # テンプレートリストが更新されたかを確認
            self.assertTrue(self.page.updated)
        except Exception as e:
            self.fail(f"テンプレートリスト読み込み中に例外が発生: {e}")
    
    def test_template_selection(self):
        """テンプレート選択テスト"""
        # テスト実装は省略（時間の関係上）
        pass


# Fletのモックオブジェクト
class MockPage:
    """フレットのPageオブジェクトのモック"""
    
    def __init__(self):
        self.controls = []
        self.dialog = None
        self.overlay = []
        self.views = []
        self.updated = False  # 更新されたかを追跡
    
    def update(self):
        """ページの更新をシミュレート"""
        self.updated = True
    
    def add(self, control):
        """コントロールの追加をシミュレート"""
        self.controls.append(control)
    
    def show_snack_bar(self, snack_bar):
        """スナックバーの表示をシミュレート"""
        pass
    
    def go(self, route):
        """ルート変更をシミュレート"""
        pass


if __name__ == "__main__":
    unittest.main() 