import flet as ft
import os
import sys
import argparse
import traceback

# スクリプトの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 相対パスを絶対パスに変換する関数
def abs_path(rel_path):
    return os.path.join(script_dir, rel_path)

from ui.main_view import MainView
from image_processor import ImageProcessor
from template_manager import TemplateManager
from data_handler import DataHandler

# グローバルな例外ハンドラ
def global_exception_handler(exctype, value, tb):
    """グローバルな例外をキャッチして処理"""
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    print(f"未処理の例外が発生しました:\n{error_msg}")
    
    # 元の例外ハンドラにも流す
    sys.__excepthook__(exctype, value, tb)

# グローバル例外ハンドラを設定
sys.excepthook = global_exception_handler

def batch_process(csv_path, image_folder, output_folder, template_path):
    """バッチ処理を実行する関数"""
    template_manager = TemplateManager()
    data_handler = DataHandler()
    image_processor = ImageProcessor()
    
    try:
        # CSVデータを読み込み
        csv_data = data_handler.load_csv(csv_path)
        if csv_data is None:
            print("CSVファイルの読み込みに失敗しました")
            return False
        
        # テンプレートを読み込み
        template = template_manager.data_handler.load_template(template_path)
        if template is None:
            print(f"テンプレートの読み込みに失敗しました: {template_path}")
            return False
        
        # テンプレートの色情報をタプルに変換
        for text_elem in template.get("text_elements", []):
            if "color" in text_elem and isinstance(text_elem["color"], list):
                text_elem["color"] = tuple(text_elem["color"])
        
        # 進捗表示コールバック
        def progress_callback(current, total):
            print(f"処理中... {current}/{total} 完了")
        
        # 画像処理実行
        processed, errors = image_processor.batch_process(
            csv_data, 
            image_folder, 
            template, 
            output_folder, 
            progress_callback=progress_callback
        )
        
        print(f"バッチ処理完了: 処理件数 {processed}件, エラー {errors}件")
        return True
    except Exception as e:
        print(f"バッチ処理でエラーが発生しました: {str(e)}")
        traceback.print_exc()
        return False

def run_flet_app(assets_dir):
    """Fletアプリケーションを実行する関数"""
    try:
        # view関数に例外ハンドリングを追加したラッパー
        def wrapped_main_view(page):
            try:
                MainView(page)
            except Exception as e:
                # エラー表示画面
                page.views.clear()
                page.add(
                    ft.Column([
                        ft.Text("エラーが発生しました", size=20, color=ft.colors.RED),
                        ft.Text(str(e)),
                        ft.ElevatedButton("再試行", on_click=lambda _: page.window_close()),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20)
                )
                page.update()
                # エラーログ出力
                print(f"アプリケーションでエラーが発生しました: {str(e)}")
                traceback.print_exc()
        
        # Fletアプリを実行
        ft.app(target=wrapped_main_view, assets_dir=assets_dir)
        
    except Exception as e:
        print(f"Fletアプリケーションの起動中にエラーが発生しました: {str(e)}")
        traceback.print_exc()
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='画像合成自動化ツール')
    parser.add_argument('--batch', action='store_true', help='バッチモードで実行')
    parser.add_argument('--csv', help='商品情報CSVファイルパス')
    parser.add_argument('--images', help='商品画像フォルダパス')
    parser.add_argument('--output', help='出力先フォルダパス')
    parser.add_argument('--template', help='テンプレートファイルパス')
    
    args = parser.parse_args()
    
    # テンプレートディレクトリが存在しない場合は作成
    templates_dir = abs_path("templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir, exist_ok=True)
    
    # アセットディレクトリが存在しない場合は作成
    assets_dir = abs_path("assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir, exist_ok=True)
    
    # バッチモードの場合
    if args.batch:
        if not all([args.csv, args.images, args.output, args.template]):
            print("バッチモードでは以下のオプションが必要です:")
            print("--csv: 商品情報CSVファイルパス")
            print("--images: 商品画像フォルダパス")
            print("--output: 出力先フォルダパス")
            print("--template: テンプレートファイルパス")
            return
        
        # 絶対パスに変換
        csv_path = os.path.abspath(args.csv)
        image_folder = os.path.abspath(args.images)
        output_folder = os.path.abspath(args.output)
        template_path = os.path.abspath(args.template)
        
        # バッチ処理実行
        success = batch_process(csv_path, image_folder, output_folder, template_path)
        # 終了コードを設定
        sys.exit(0 if success else 1)
    else:
        # Fletアプリケーションを起動
        run_flet_app(assets_dir)

if __name__ == "__main__":
    main()
