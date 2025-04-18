import flet as ft
import os
import sys

# スクリプトの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 相対パスを絶対パスに変換する関数
def abs_path(rel_path):
    return os.path.join(script_dir, rel_path)

from ui.main_view import MainView

def main():
    # テンプレートディレクトリが存在しない場合は作成
    templates_dir = abs_path("templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir, exist_ok=True)
    
    # アセットディレクトリが存在しない場合は作成
    assets_dir = abs_path("assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir, exist_ok=True)
    
    # Fletアプリケーションを起動
    ft.app(target=MainView, assets_dir=assets_dir)

if __name__ == "__main__":
    main()
