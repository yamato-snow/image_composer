#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def run_batch_process(csv_path, image_folder, output_folder, template_path):
    """バッチ処理を別プロセスとして実行"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "main.py")
    
    # コマンドを構築
    cmd = [
        sys.executable, 
        main_script,
        "--batch",
        "--csv", csv_path,
        "--images", image_folder,
        "--output", output_folder,
        "--template", template_path
    ]
    
    print(f"バッチ処理を実行中...")
    print(f"CSV: {csv_path}")
    print(f"画像フォルダ: {image_folder}")
    print(f"出力先: {output_folder}")
    print(f"テンプレート: {template_path}")
    
    # サブプロセスとして実行
    try:
        result = subprocess.run(
            cmd, 
            check=True, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            text=True
        )
        
        # 標準出力とエラー出力を表示
        print(result.stdout)
        
        if result.stderr:
            print(f"エラー出力:\n{result.stderr}")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"バッチ処理実行エラー: {e}")
        print(f"標準出力:\n{e.stdout}")
        print(f"エラー出力:\n{e.stderr}")
        return False

if __name__ == "__main__":
    # コマンドライン引数を確認
    if len(sys.argv) != 5:
        print("使用方法: python batch_runner.py <csv_path> <image_folder> <output_folder> <template_path>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    image_folder = sys.argv[2]
    output_folder = sys.argv[3]
    template_path = sys.argv[4]
    
    # バッチ処理実行
    success = run_batch_process(csv_path, image_folder, output_folder, template_path)
    
    # 終了コードを設定
    sys.exit(0 if success else 1) 