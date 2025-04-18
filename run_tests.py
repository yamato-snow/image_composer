#!/usr/bin/env python3
import unittest
import sys
import os

if __name__ == "__main__":
    print("画像合成自動化ツールのテストを実行します...")
    
    # テスト対象のモジュールをインポート
    import test_data_handler
    import test_template_manager
    import test_batch_process
    
    # テストローダーを作成
    loader = unittest.TestLoader()
    
    # テストスイートを作成
    test_suite = unittest.TestSuite()
    
    # 各テストケースをテストスイートに追加
    test_suite.addTests(loader.loadTestsFromTestCase(test_data_handler.TestDataHandler))
    test_suite.addTests(loader.loadTestsFromTestCase(test_template_manager.TestTemplateManager))
    test_suite.addTests(loader.loadTestsFromTestCase(test_batch_process.TestBatchProcess))
    
    # テストを実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 結果に基づいて終了コードを設定
    sys.exit(0 if result.wasSuccessful() else 1) 