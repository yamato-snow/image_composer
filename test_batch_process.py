#!/usr/bin/env python3
import unittest
import os
import shutil
import tempfile
import pandas as pd
from image_processor import ImageProcessor
from template_manager import TemplateManager
from data_handler import DataHandler

class TestBatchProcess(unittest.TestCase):
    """バッチ処理の単体テスト"""
    
    def setUp(self):
        """テスト用ディレクトリとファイルを準備"""
        # 一時ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()
        
        # テンプレートマネージャと各種ハンドラを初期化
        self.template_manager = TemplateManager()
        self.data_handler = DataHandler()
        self.image_processor = ImageProcessor()
        
        # テスト用CSVデータを作成
        self.csv_path = os.path.join(self.test_dir, "test_data.csv")
        self.create_test_csv()
        
        # テスト用画像フォルダを作成
        self.image_folder = os.path.join(self.test_dir, "images")
        os.makedirs(self.image_folder, exist_ok=True)
        self.create_test_images()
        
        # 出力先フォルダを作成
        self.output_folder = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_folder, exist_ok=True)
        
        # テスト用テンプレートを作成
        self.template_path = os.path.join(self.test_dir, "test_template.json")
        self.create_test_template()
    
    def tearDown(self):
        """テスト終了後のクリーンアップ"""
        # テスト用ディレクトリを削除
        shutil.rmtree(self.test_dir)
    
    def create_test_csv(self):
        """テスト用CSVデータを作成"""
        data = {
            'id': [1, 2, 3],
            'name': ['テスト商品1', 'テスト商品2', 'テスト商品3'],
            'price': [1000, 2000, 3000],
            'image_file': ['test1.png', 'test2.png', 'test3.png']
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False)
    
    def create_test_images(self):
        """テスト用画像を作成"""
        from PIL import Image
        
        # テスト用のダミー画像を作成
        for i in range(1, 4):
            image_path = os.path.join(self.image_folder, f"test{i}.png")
            # 100x100の白い画像を作成
            image = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
            image.save(image_path)
    
    def create_test_template(self):
        """テスト用テンプレートを作成"""
        # デフォルトテンプレートを元に作成する
        template = {
            "name": "テスト用テンプレート",
            "background": "",
            "product_position": [50, 50],
            "product_size": [80, 80],
            "text_elements": [
                {
                    "text": "${name}",
                    "position": [10, 10],
                    "font": "arial.ttf",
                    "font_size": 12,
                    "color": [0, 0, 0]  # タプルではなくリストで指定
                },
                {
                    "text": "¥${price}",
                    "position": [10, 30],
                    "font": "arial.ttf",
                    "font_size": 14,
                    "color": [255, 0, 0]  # タプルではなくリストで指定
                }
            ],
            "image_elements": []
        }
        self.data_handler.save_template(template, self.template_path)
    
    def test_batch_process(self):
        """バッチ処理の基本的な動作をテスト"""
        # CSVデータを読み込み
        csv_data = self.data_handler.load_csv(self.csv_path)
        self.assertIsNotNone(csv_data, "CSVの読み込みに失敗しました")
        
        # テンプレートを読み込み
        template = self.data_handler.load_template(self.template_path)
        self.assertIsNotNone(template, "テンプレートの読み込みに失敗しました")
        
        # テンプレートの色情報をタプルに変換
        for text_elem in template["text_elements"]:
            if "color" in text_elem and isinstance(text_elem["color"], list):
                text_elem["color"] = tuple(text_elem["color"])
        
        # 進捗コールバック関数
        progress_log = []
        def progress_callback(current, total):
            progress_log.append((current, total))
        
        # バッチ処理を実行
        processed, errors = self.image_processor.batch_process(
            csv_data,
            self.image_folder,
            template,
            self.output_folder,
            progress_callback=progress_callback
        )
        
        # テスト結果を確認
        self.assertEqual(processed, 3, "処理件数が想定と異なります")
        self.assertEqual(errors, 0, "エラー件数が想定と異なります")
        
        # 進捗コールバックが呼ばれたことを確認
        self.assertEqual(len(progress_log), 3, "進捗コールバックの呼び出し回数が想定と異なります")
        
        # 出力ファイルが存在することを確認
        for i in range(1, 4):
            output_path = os.path.join(self.output_folder, f"{i}.png")
            self.assertTrue(os.path.exists(output_path), f"出力ファイル {output_path} が存在しません")
    
    def test_batch_process_missing_image(self):
        """存在しない画像ファイルがある場合のテスト"""
        # 不正なCSVデータを作成
        data = {
            'id': [1, 2, 3],
            'name': ['テスト商品1', 'テスト商品2', 'テスト商品3'],
            'price': [1000, 2000, 3000],
            'image_file': ['test1.png', 'not_exist.png', 'test3.png']
        }
        invalid_csv_path = os.path.join(self.test_dir, "invalid_data.csv")
        pd.DataFrame(data).to_csv(invalid_csv_path, index=False)
        
        # CSVデータを読み込み
        csv_data = self.data_handler.load_csv(invalid_csv_path)
        
        # テンプレートを読み込み
        template = self.data_handler.load_template(self.template_path)
        
        # テンプレートの色情報をタプルに変換
        for text_elem in template["text_elements"]:
            if "color" in text_elem and isinstance(text_elem["color"], list):
                text_elem["color"] = tuple(text_elem["color"])
        
        # バッチ処理を実行
        processed, errors = self.image_processor.batch_process(
            csv_data,
            self.image_folder,
            template,
            self.output_folder
        )
        
        # テスト結果を確認
        self.assertEqual(processed, 2, "処理件数が想定と異なります")
        self.assertEqual(errors, 1, "エラー件数が想定と異なります")
        
        # 成功した出力ファイルが存在することを確認
        self.assertTrue(os.path.exists(os.path.join(self.output_folder, "1.png")))
        self.assertFalse(os.path.exists(os.path.join(self.output_folder, "2.png")))
        self.assertTrue(os.path.exists(os.path.join(self.output_folder, "3.png")))

if __name__ == "__main__":
    unittest.main() 