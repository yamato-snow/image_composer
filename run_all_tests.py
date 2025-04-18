import unittest
import sys
import os
import json

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# パッチをテスト前に適用
print("JSONパッチを適用しています...")
try:
    from json_patch import apply_patch
    apply_patch()
except Exception as e:
    print(f"パッチの適用に失敗しました: {e}")
    
# 既存のテストをインポート
print("テストモジュールを読み込んでいます...")
try:
    from test_data_handler import TestDataHandler
    from test_template_manager import TestTemplateManager
    from test_batch_process import TestBatchProcess
    from test_json_patch import TestJSONPatch
    from test_template_view import TestTemplateView
except Exception as e:
    print(f"テストモジュールのインポートに失敗しました: {e}")
    
def create_test_suite():
    """すべてのテストを含むテストスイートを作成"""
    # テストスイートの作成
    suite = unittest.TestSuite()
    
    # 各テストクラスのすべてのテストを追加
    suite.addTest(unittest.makeSuite(TestDataHandler))
    suite.addTest(unittest.makeSuite(TestTemplateManager))
    suite.addTest(unittest.makeSuite(TestBatchProcess))
    suite.addTest(unittest.makeSuite(TestJSONPatch))
    suite.addTest(unittest.makeSuite(TestTemplateView))
    
    return suite
    
if __name__ == "__main__":
    # テストランナーの初期化
    runner = unittest.TextTestRunner(verbosity=2)
    
    # テストスイートの実行
    print("すべてのテストを実行します...")
    suite = create_test_suite()
    result = runner.run(suite)
    
    # 結果に基づく終了コードの設定
    sys.exit(not result.wasSuccessful()) 