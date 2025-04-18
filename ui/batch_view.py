import flet as ft
import os
import threading
import time
import subprocess
import sys
from template_manager import TemplateManager
from data_handler import DataHandler
from image_processor import ImageProcessor

def BatchView(page):
    """バッチ処理ビュー"""
    template_manager = TemplateManager()
    data_handler = DataHandler()
    image_processor = ImageProcessor()
    
    # 処理状態
    processing = False
    csv_path = ""
    image_folder = ""
    output_folder = ""
    selected_template_path = None
    
    # 各種フィールドを定義
    # CSVファイル選択フィールド
    csv_field = ft.TextField(
        label="商品情報CSV",
        read_only=True,
        expand=True
    )
    
    # 商品画像フォルダ選択フィールド
    image_folder_field = ft.TextField(
        label="商品画像フォルダ",
        read_only=True,
        expand=True
    )
    
    # 出力先フォルダ選択フィールド
    output_folder_field = ft.TextField(
        label="出力先フォルダ",
        read_only=True,
        expand=True
    )
    
    # テンプレート一覧
    template_list = ft.ListView(
        expand=1,
        spacing=10,
        padding=10,
        auto_scroll=True
    )
    
    # 進捗表示
    progress_bar = ft.ProgressBar(width=600, value=0)
    progress_text = ft.Text("待機中")
    
    # 処理ボタン
    process_button = ft.ElevatedButton(
        "処理開始",
        icon=ft.icons.PLAY_ARROW,
        on_click=lambda _: start_process()
    )
    
    # 処理ログ表示
    log_text = ft.TextField(
        label="処理ログ",
        multiline=True,
        read_only=True,
        min_lines=5,
        max_lines=5,
        expand=True
    )
    
    # ファイル選択ハンドラ関数
    def handle_csv_picked(e):
        if e.files and len(e.files) > 0:
            nonlocal csv_path
            csv_path = e.files[0].path
            csv_field.value = csv_path
            page.update()
    
    def handle_image_folder_picked(e):
        if e.path:
            nonlocal image_folder
            image_folder = e.path
            image_folder_field.value = image_folder
            page.update()
    
    def handle_output_folder_picked(e):
        if e.path:
            nonlocal output_folder
            output_folder = e.path
            output_folder_field.value = output_folder
            page.update()
    
    # ファイル選択用のPickerを作成
    csv_picker = ft.FilePicker(on_result=handle_csv_picked)
    image_folder_picker = ft.FilePicker(on_result=handle_image_folder_picked)
    output_folder_picker = ft.FilePicker(on_result=handle_output_folder_picked)
    
    # ファイル選択UIをページのオーバーレイに追加
    page.overlay.extend([csv_picker, image_folder_picker, output_folder_picker])
    page.update()  # オーバレイを更新
    
    # CSVファイル選択ボタン
    def pick_csv_file(_):
        csv_picker.pick_files(
            dialog_title="商品情報CSVを選択",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["csv"]
        )
    
    # 商品画像フォルダ選択ボタン
    def pick_image_folder(_):
        image_folder_picker.get_directory_path(
            dialog_title="商品画像フォルダを選択"
        )
    
    # 出力先フォルダ選択ボタン
    def pick_output_folder(_):
        output_folder_picker.get_directory_path(
            dialog_title="出力先フォルダを選択"
        )
    
    # テンプレート一覧を読み込み
    def load_template_list():
        """テンプレート一覧を読み込み"""
        template_list.controls.clear()
        templates = template_manager.get_template_list()
        
        for template_info in templates:
            template_item = ft.Container(
                content=ft.ListTile(
                    title=ft.Text(template_info["name"]),
                    subtitle=ft.Text(os.path.basename(template_info["path"]), size=10),
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    trailing=ft.Radio(value=template_info["path"]),
                    on_click=lambda _, path=template_info["path"]: select_template(path)
                ),
                border=ft.border.all(1, ft.colors.BLACK12),
                border_radius=5,
                padding=5
            )
            template_list.controls.append(template_item)
        
        page.update()
    
    # テンプレート選択
    def select_template(path):
        nonlocal selected_template_path
        
        # 選択状態を更新
        for item in template_list.controls:
            radio = item.content.trailing
            if radio.value == path:
                radio.value = path
                radio.selected = True
                selected_template_path = path
            else:
                radio.selected = False
        
        page.update()
    
    # 入力値検証
    def validate_inputs():
        """入力値を検証"""
        errors = []
        
        if not csv_path or not os.path.exists(csv_path):
            errors.append("有効なCSVファイルを選択してください")
        
        if not image_folder or not os.path.exists(image_folder):
            errors.append("有効な商品画像フォルダを選択してください")
        
        if not output_folder:
            errors.append("出力先フォルダを選択してください")
        
        if not selected_template_path:
            errors.append("テンプレートを選択してください")
        
        return errors
    
    # 処理開始
    def start_process():
        """処理を開始"""
        nonlocal processing
        
        # 処理中なら何もしない
        if processing:
            return
        
        # 入力値検証
        errors = validate_inputs()
        if errors:
            page.snack_bar = ft.SnackBar(ft.Text(errors[0]))
            page.snack_bar.open = True
            page.update()
            return
        
        # UI更新
        processing = True
        progress_bar.value = 0
        progress_text.value = "処理準備中..."
        process_button.disabled = True
        log_text.value = ""
        page.update()
        
        # バックグラウンドで処理実行
        threading.Thread(
            target=process_in_background,
            args=(csv_path, image_folder, output_folder, selected_template_path),
            daemon=True
        ).start()
    
    # バックグラウンド処理
    def process_in_background(csv_path, image_folder, output_folder, template_path):
        """バックグラウンドで処理実行"""
        nonlocal processing
        
        try:
            # UIの更新を待つ
            time.sleep(0.5)
            
            # スクリプトのパスを取得
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            batch_runner = os.path.join(script_dir, "batch_runner.py")
            
            # コマンドを構築
            cmd = [
                sys.executable,
                batch_runner,
                csv_path,
                image_folder,
                output_folder,
                template_path
            ]
            
            # 進捗表示を更新
            progress_text.value = "バッチ処理を開始します..."
            log_text.value += "バッチ処理を開始します...\n"
            page.update()
            
            # サブプロセスとして実行
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                bufsize=1,
                universal_newlines=True
            )
            
            # 標準出力をリアルタイムで読み取り
            total_lines = 0
            processed_items = 0
            total_items = 0
            
            # 標準出力の読み取り
            for line in process.stdout:
                log_text.value += line
                
                # 進捗情報を解析
                if "処理中..." in line and "/" in line:
                    try:
                        parts = line.split("処理中... ")[1].split("/")
                        current = int(parts[0].strip())
                        total = int(parts[1].split(" ")[0].strip())
                        processed_items = current
                        total_items = total
                        progress_bar.value = current / total
                        progress_text.value = f"処理中... {current}/{total}"
                    except:
                        pass
                
                # 処理完了情報
                if "バッチ処理完了" in line:
                    progress_bar.value = 1.0
                    progress_text.value = "処理完了"
                
                # 5行以上ある場合は古い行を削除
                total_lines += 1
                lines = log_text.value.split("\n")
                if len(lines) > 20:
                    log_text.value = "\n".join(lines[-20:])
                
                page.update()
            
            # エラー出力の読み取り
            error_output = process.stderr.read()
            if error_output:
                log_text.value += f"\nエラー出力:\n{error_output}"
                progress_text.value = "エラーが発生しました"
                page.update()
            
            # 処理完了
            process.wait()
            
            if process.returncode == 0:
                progress_bar.value = 1.0
                if processed_items > 0:
                    progress_text.value = f"完了: {processed_items}件処理"
                else:
                    progress_text.value = "処理完了"
                
                # 完了メッセージ
                page.snack_bar = ft.SnackBar(ft.Text("画像処理が完了しました"))
                page.snack_bar.open = True
            else:
                progress_text.value = f"エラーが発生しました (終了コード: {process.returncode})"
                page.snack_bar = ft.SnackBar(ft.Text("処理中にエラーが発生しました"))
                page.snack_bar.open = True
                
            page.update()
            
        except Exception as e:
            # エラー発生時のUI更新
            progress_bar.value = 0
            progress_text.value = f"エラー発生: {str(e)}"
            log_text.value += f"\nエラー発生: {str(e)}"
            page.update()
            
            # エラーメッセージ表示
            page.snack_bar = ft.SnackBar(ft.Text(f"処理中にエラーが発生しました: {str(e)}"))
            page.snack_bar.open = True
            page.update()
        
        finally:
            processing = False
            process_button.disabled = False
            page.update()
    
    # メインレイアウト
    main_layout = ft.Column(
        [
            # ファイル選択部分
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("ファイル設定", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            
                            # CSVファイル選択
                            ft.Row(
                                [
                                    csv_field,
                                    ft.ElevatedButton(
                                        "参照",
                                        icon=ft.icons.FOLDER_OPEN,
                                        on_click=pick_csv_file
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            
                            # 商品画像フォルダ選択
                            ft.Row(
                                [
                                    image_folder_field,
                                    ft.ElevatedButton(
                                        "参照",
                                        icon=ft.icons.FOLDER_OPEN,
                                        on_click=pick_image_folder
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            
                            # 出力先フォルダ選択
                            ft.Row(
                                [
                                    output_folder_field,
                                    ft.ElevatedButton(
                                        "参照",
                                        icon=ft.icons.FOLDER_OPEN,
                                        on_click=pick_output_folder
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ],
                        spacing=20
                    ),
                    padding=20
                )
            ),
            
            # テンプレート選択部分
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("テンプレート選択", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            template_list
                        ]
                    ),
                    padding=20,
                    height=200
                )
            ),
            
            # 進捗表示部分
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("処理状況", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            progress_bar,
                            progress_text,
                            log_text,
                            ft.Container(
                                content=process_button,
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(top=20)
                            )
                        ]
                    ),
                    padding=20
                )
            )
        ],
        spacing=20
    )
    
    # テンプレート一覧を初期ロード
    load_template_list()
    
    return ft.Container(
        content=main_layout,
        padding=20,
        expand=True
    )