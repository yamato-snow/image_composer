import unittest
import json
import sys
import os

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# パッチ適用前にオリジナルのjson.loads関数を保存
original_loads = json.loads

class TestJSONPatch(unittest.TestCase):
    
    def setUp(self):
        """各テスト前の準備"""
        # パッチを適用
        from json_patch import apply_patch
        apply_patch()
    
    def tearDown(self):
        """各テスト後の後始末"""
        # 元のjson.loads関数を復元
        json.loads = original_loads
    
    def test_valid_json(self):
        """有効なJSONデータがロードできるか"""
        valid_json = '{"name": "テスト", "value": 123}'
        result = json.loads(valid_json)
        self.assertEqual(result["name"], "テスト")
        self.assertEqual(result["value"], 123)
    
    def test_empty_json(self):
        """空のJSONデータを処理できるか"""
        # 空文字列
        result = json.loads("")
        self.assertEqual(result, [])
        
        # 空白のみ
        result = json.loads("   ")
        self.assertEqual(result, [])
    
    def test_invalid_json(self):
        """不正なJSONデータを処理できるか"""
        # JSONパースエラーが発生するデータ
        result = json.loads("{invalid")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main() 