#!/usr/bin/env python3
import unittest
import os
import tempfile
import shutil
import json
import pandas as pd
from data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    """DataHandlerクラスの単体テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        # テスト用ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()
        
        # DataHandlerインスタンスを作成
        self.data_handler = DataHandler()
        
        # テスト用ファイルのパスを設定
        self.csv_path = os.path.join(self.test_dir, "test_data.csv")
        self.template_path = os.path.join(self.test_dir, "test_template.json")
        
        # テスト用CSVを作成
        self.create_test_csv()
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        # テスト用ディレクトリを削除
        shutil.rmtree(self.test_dir)
    
    def create_test_csv(self):
        """テスト用CSVファイルを作成"""
        data = {
            'id': [1, 2, 3],
            'name': ['テスト商品1', 'テスト商品2', 'テスト商品3'],
            'price': [1000, 2000, 3000],
            'image_file': ['test1.png', 'test2.png', 'test3.png']
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False)
    
    def test_load_csv(self):
        """CSVファイルのロードをテスト"""
        # CSVファイルを読み込み
        df = self.data_handler.load_csv(self.csv_path)
        
        # 結果を検証
        self.assertIsNotNone(df, "CSVのロードに失敗しました")
        self.assertEqual(len(df), 3, "行数が一致しません")
        self.assertEqual(list(df.columns), ['id', 'name', 'price', 'image_file'], "列名が一致しません")
        self.assertEqual(df.iloc[0]['name'], 'テスト商品1', "データ内容が一致しません")
    
    def test_load_csv_not_exist(self):
        """存在しないCSVファイルのロードをテスト"""
        # 存在しないファイルを読み込み
        df = self.data_handler.load_csv(os.path.join(self.test_dir, "not_exist.csv"))
        
        # 結果を検証
        self.assertIsNone(df, "存在しないCSVファイルのロードエラーハンドリングに失敗しました")
    
    def test_create_default_template(self):
        """デフォルトテンプレート生成をテスト"""
        # デフォルトテンプレートを生成
        template = self.data_handler.create_default_template()
        
        # 結果を検証
        self.assertIsNotNone(template, "デフォルトテンプレートの生成に失敗しました")
        self.assertIn("name", template, "テンプレートに'name'キーがありません")
        self.assertIn("text_elements", template, "テンプレートに'text_elements'キーがありません")
        self.assertGreater(len(template["text_elements"]), 0, "テキスト要素がありません")
    
    def test_save_and_load_template(self):
        """テンプレートの保存と読み込みをテスト"""
        # デフォルトテンプレートを生成して保存
        template = self.data_handler.create_default_template()
        template["name"] = "テスト用テンプレート"
        
        # テンプレートを保存
        result = self.data_handler.save_template(template, self.template_path)
        self.assertTrue(result, "テンプレートの保存に失敗しました")
        self.assertTrue(os.path.exists(self.template_path), "テンプレートファイルが作成されていません")
        
        # 保存したテンプレートを読み込み
        loaded_template = self.data_handler.load_template(self.template_path)
        
        # 結果を検証
        self.assertIsNotNone(loaded_template, "テンプレートの読み込みに失敗しました")
        self.assertEqual(loaded_template["name"], "テスト用テンプレート", "テンプレート名が一致しません")
        self.assertEqual(len(loaded_template["text_elements"]), len(template["text_elements"]), "テキスト要素の数が一致しません")
    
    def test_load_template_not_exist(self):
        """存在しないテンプレートの読み込みをテスト"""
        # 存在しないファイルを読み込み
        result = self.data_handler.load_template(os.path.join(self.test_dir, "not_exist.json"))
        
        # 結果を検証 - デフォルトテンプレートが返されることを確認
        self.assertIsNotNone(result, "テンプレート読み込みエラー時にデフォルトテンプレートが返されていません")
        self.assertIn("name", result, "デフォルトテンプレートに'name'キーがありません")
    
    def test_save_template_invalid_path(self):
        """無効なパスへのテンプレート保存をテスト"""
        # デフォルトテンプレートを生成
        template = self.data_handler.create_default_template()
        
        # 無効なパスに保存を試みる
        invalid_path = os.path.join(self.test_dir, "not_exist_dir", "template.json")
        result = self.data_handler.save_template(template, invalid_path)
        
        # 結果を検証
        self.assertFalse(result, "無効なパスへの保存エラーハンドリングに失敗しました")

if __name__ == "__main__":
    unittest.main() 