#!/usr/bin/env python3
import unittest
import os
import tempfile
import shutil
import json
from template_manager import TemplateManager
from data_handler import DataHandler

class TestTemplateManager(unittest.TestCase):
    """TemplateManagerクラスの単体テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        # テスト用ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()
        
        # テスト用のテンプレートディレクトリを作成
        self.templates_dir = os.path.join(self.test_dir, "templates")
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # TemplateManagerインスタンスを作成（テスト用ディレクトリを使用）
        self.template_manager = TemplateManager(self.templates_dir)
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        # テスト用ディレクトリを削除
        shutil.rmtree(self.test_dir)
    
    def test_init_creates_default_template(self):
        """初期化時にデフォルトテンプレートが作成されるかテスト"""
        # デフォルトテンプレートファイルが存在するか確認
        default_path = os.path.join(self.templates_dir, "default.json")
        self.assertTrue(os.path.exists(default_path), "デフォルトテンプレートが作成されていません")
        
        # ファイルの内容を確認
        with open(default_path, 'r', encoding='utf-8') as f:
            template = json.load(f)
        
        self.assertIn("name", template, "テンプレートに'name'キーがありません")
        self.assertEqual(template["name"], "デフォルトテンプレート", "テンプレート名が一致しません")
    
    def test_get_template_list(self):
        """テンプレート一覧取得をテスト"""
        # テスト用のテンプレートファイルを追加
        template1 = self.template_manager.data_handler.create_default_template()
        template1["name"] = "テスト用テンプレート1"
        template1_path = os.path.join(self.templates_dir, "test1.json")
        self.template_manager.data_handler.save_template(template1, template1_path)
        
        template2 = self.template_manager.data_handler.create_default_template()
        template2["name"] = "テスト用テンプレート2"
        template2_path = os.path.join(self.templates_dir, "test2.json")
        self.template_manager.data_handler.save_template(template2, template2_path)
        
        # テンプレート一覧を取得
        templates = self.template_manager.get_template_list()
        
        # 結果を検証
        self.assertIsNotNone(templates, "テンプレート一覧の取得に失敗しました")
        self.assertGreaterEqual(len(templates), 3, "テンプレート数が想定と異なります (デフォルト + 追加2件)")
        
        # 追加したテンプレートが含まれているか確認
        template_names = [t["name"] for t in templates]
        self.assertIn("テスト用テンプレート1", template_names, "追加したテンプレート1が一覧に含まれていません")
        self.assertIn("テスト用テンプレート2", template_names, "追加したテンプレート2が一覧に含まれていません")
    
    def test_create_template(self):
        """テンプレート作成をテスト"""
        # 新しいテンプレートを作成
        template_data = self.template_manager.data_handler.create_default_template()
        template_data["name"] = "新規テンプレート"
        
        # テンプレートを保存
        result = self.template_manager.create_template(template_data, "新規テンプレート")
        
        # 結果を検証
        self.assertTrue(result, "テンプレートの作成に失敗しました")
        
        # ファイルが作成されたか確認
        expected_path = os.path.join(self.templates_dir, "新規テンプレート.json")
        self.assertTrue(os.path.exists(expected_path), "テンプレートファイルが作成されていません")
        
        # ファイル内容を確認
        with open(expected_path, 'r', encoding='utf-8') as f:
            saved_template = json.load(f)
        
        self.assertEqual(saved_template["name"], "新規テンプレート", "保存されたテンプレート名が一致しません")
    
    def test_update_template(self):
        """テンプレート更新をテスト"""
        # テスト用のテンプレートファイルを作成
        template = self.template_manager.data_handler.create_default_template()
        template["name"] = "更新前テンプレート"
        template_path = os.path.join(self.templates_dir, "update_test.json")
        self.template_manager.data_handler.save_template(template, template_path)
        
        # テンプレートを更新
        template["name"] = "更新後テンプレート"
        result = self.template_manager.update_template(template, template_path)
        
        # 結果を検証
        self.assertTrue(result, "テンプレートの更新に失敗しました")
        
        # 更新内容を確認
        with open(template_path, 'r', encoding='utf-8') as f:
            updated_template = json.load(f)
        
        self.assertEqual(updated_template["name"], "更新後テンプレート", "テンプレートが正しく更新されていません")
    
    def test_delete_template(self):
        """テンプレート削除をテスト"""
        # テスト用のテンプレートファイルを作成
        template = self.template_manager.data_handler.create_default_template()
        template_path = os.path.join(self.templates_dir, "delete_test.json")
        self.template_manager.data_handler.save_template(template, template_path)
        
        # ファイルが作成されたことを確認
        self.assertTrue(os.path.exists(template_path), "テスト用テンプレートが作成されていません")
        
        # テンプレートを削除
        result = self.template_manager.delete_template(template_path)
        
        # 結果を検証
        self.assertTrue(result, "テンプレートの削除に失敗しました")
        self.assertFalse(os.path.exists(template_path), "テンプレートファイルが削除されていません")
    
    def test_delete_nonexistent_template(self):
        """存在しないテンプレートの削除をテスト"""
        # 存在しないテンプレートのパス
        nonexistent_path = os.path.join(self.templates_dir, "nonexistent.json")
        
        # 削除を試みる
        result = self.template_manager.delete_template(nonexistent_path)
        
        # 結果を検証
        self.assertFalse(result, "存在しないテンプレート削除時のエラーハンドリングに失敗しました")

if __name__ == "__main__":
    unittest.main() 