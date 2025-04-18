import flet as ft
import os
import json
from template_manager import TemplateManager

def TemplateView(page):
    """テンプレート管理ビュー"""
    template_manager = TemplateManager()
    
    # 現在選択中のテンプレート情報
    current_template = None
    current_template_path = None
    
    # ロード中表示用プログレスバー
    loading = ft.ProgressBar(width=100, visible=False)
    
    # テンプレート一覧
    template_list = ft.ListView(
        expand=1,
        spacing=10,
        padding=10,
        auto_scroll=True
    )
    
    # 右側のフォーム
    template_name = ft.TextField(
        label="テンプレート名",
        width=300
    )
    
    bg_path = ft.TextField(
        label="背景画像パス",
        width=400,
        expand=True
    )
    
    product_pos_x = ft.TextField(
        label="X位置",
        width=100,
        value="250",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    product_pos_y = ft.TextField(
        label="Y位置",
        width=100,
        value="150",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    product_size_w = ft.TextField(
        label="幅",
        width=100,
        value="300",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    product_size_h = ft.TextField(
        label="高さ",
        width=100,
        value="300",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # テキスト要素リスト
    text_elements_list = ft.ListView(
        height=200,
        spacing=10,
        padding=10,
        auto_scroll=True
    )
    
    # 装飾要素リスト
    image_elements_list = ft.ListView(
        height=200,
        spacing=10,
        padding=10,
        auto_scroll=True
    )
    
    # テンプレート編集部分
    template_form = ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [template_name],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=ft.padding.only(bottom=10)
            ),
            
            ft.Text("背景設定", size=16, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    bg_path,
                    ft.ElevatedButton(
                        "参照",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda _: pick_background_file()
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            
            ft.Divider(),
            
            ft.Text("商品画像設定", size=16, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.Text("位置:"),
                    product_pos_x,
                    product_pos_y
                ]
            ),
            ft.Row(
                [
                    ft.Text("サイズ:"),
                    product_size_w,
                    product_size_h
                ]
            ),
            
            ft.Divider(),
            
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("テキスト要素", size=16, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton(
                                    "追加",
                                    icon=ft.Icons.ADD,
                                    on_click=lambda _: add_text_element()
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        text_elements_list,
                        ft.Row(
                            [
                                ft.OutlinedButton(
                                    "編集",
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda _: edit_text_element()
                                ),
                                ft.OutlinedButton(
                                    "削除",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda _: remove_text_element()
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ]
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("装飾要素", size=16, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton(
                                    "追加",
                                    icon=ft.Icons.ADD,
                                    on_click=lambda _: add_image_element()
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        image_elements_list,
                        ft.Row(
                            [
                                ft.OutlinedButton(
                                    "編集",
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda _: edit_image_element()
                                ),
                                ft.OutlinedButton(
                                    "削除",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda _: remove_image_element()
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ]
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            ft.Container(
                content=ft.Row(
                    [
                        ft.ElevatedButton(
                            "保存",
                            icon=ft.Icons.SAVE,
                            on_click=lambda _: save_template()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    def load_template_list():
        """テンプレート一覧を読み込み"""
        template_list.controls.clear()
        templates = template_manager.get_template_list()
        
        for template_info in templates:
            template_item = ft.Container(
                content=ft.ListTile(
                    title=ft.Text(template_info["name"]),
                    subtitle=ft.Text(os.path.basename(template_info["path"]), size=10),
                    leading=ft.Icon(ft.Icons.DESCRIPTION),
                    on_click=lambda _, info=template_info: select_template(info)
                ),
                border=ft.border.all(1, ft.Colors.BLACK12),
                border_radius=5,
                padding=5
            )
            template_list.controls.append(template_item)
        
        page.update()
    
    def select_template(template_info):
        """テンプレートを選択"""
        nonlocal current_template, current_template_path
        
        # ローディング表示
        loading.visible = True
        page.update()
        
        template = template_manager.data_handler.load_template(template_info["path"])
        current_template = template
        current_template_path = template_info["path"]
        
        # UIに値を設定
        template_name.value = template.get("name", "")
        bg_path.value = template.get("background", "")
        
        # 商品画像位置とサイズ
        product_pos = template.get("product_position", (250, 150))
        product_pos_x.value = str(product_pos[0])
        product_pos_y.value = str(product_pos[1])
        
        product_size = template.get("product_size", (300, 300))
        product_size_w.value = str(product_size[0])
        product_size_h.value = str(product_size[1])
        
        # テキスト要素を更新
        update_text_elements_list()
        
        # 装飾要素を更新
        update_image_elements_list()
        
        # ローディング非表示
        loading.visible = False
        page.update()
    
    def update_text_elements_list():
        """テキスト要素リストを更新"""
        text_elements_list.controls.clear()
        
        if not current_template:
            page.update()
            return
        
        for i, element in enumerate(current_template.get("text_elements", [])):
            text = element.get("text", "")
            position = element.get("position", (0, 0))
            font_size = element.get("font_size", 24)
            
            text_elements_list.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(text),
                        subtitle=ft.Text(f"位置: {position}, サイズ: {font_size}pt", size=10),
                        leading=ft.Icon(ft.Icons.TEXT_FIELDS),
                        selected=False,
                        data=i  # インデックスを保存
                    ),
                    border=ft.border.all(1, ft.Colors.BLACK12),
                    border_radius=5
                )
            )
        
        page.update()
    
    def update_image_elements_list():
        """装飾要素リストを更新"""
        image_elements_list.controls.clear()
        
        if not current_template:
            page.update()
            return
        
        for i, element in enumerate(current_template.get("image_elements", [])):
            path = element.get("path", "")
            position = element.get("position", (0, 0))
            size = element.get("size", (100, 100))
            
            basename = os.path.basename(path) if path else "装飾要素"
            
            image_elements_list.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(basename),
                        subtitle=ft.Text(f"位置: {position}, サイズ: {size}", size=10),
                        leading=ft.Icon(ft.Icons.IMAGE),
                        selected=False,
                        data=i  # インデックスを保存
                    ),
                    border=ft.border.all(1, ft.Colors.BLACK12),
                    border_radius=5
                )
            )
        
        page.update()
    
    def pick_background_file():
        """背景画像ファイルを選択"""
        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                bg_path.value = e.files[0].path
                page.update()
        
        file_picker = ft.FilePicker(on_result=pick_file_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(
            dialog_title="背景画像を選択",
            file_type=ft.FilePickerFileType.IMAGE,
            allowed_extensions=["png", "jpg", "jpeg"]
        )
    
    def create_new_template():
        """新規テンプレートを作成"""
        def save_new_template(e):
            if not name_field.value:
                name_field.error_text = "テンプレート名を入力してください"
                dlg.update()
                return
            
            template = template_manager.data_handler.create_default_template()
            template["name"] = name_field.value
            
            success = template_manager.create_template(template, name_field.value)
            if success:
                page.snack_bar = ft.SnackBar(ft.Text("新規テンプレートを作成しました"))
                page.snack_bar.open = True
                page.update()
                load_template_list()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("テンプレート作成に失敗しました"))
                page.snack_bar.open = True
                page.update()
            
            dlg.open = False
            page.update()
        
        name_field = ft.TextField(label="テンプレート名")
        dlg = ft.AlertDialog(
            title=ft.Text("新規テンプレート"),
            content=ft.Column([name_field], width=300, height=80, tight=True),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: setattr(dlg, "open", False)),
                ft.TextButton("作成", on_click=save_new_template)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def delete_template():
        """選択されたテンプレートを削除"""
        if not current_template:
            page.snack_bar = ft.SnackBar(ft.Text("テンプレートを選択してください"))
            page.snack_bar.open = True
            page.update()
            return
        
        # ここでエラーが起きていた部分を修正
        template_path = current_template_path  # ローカル変数として保存
        template_name_str = current_template.get('name', '')
        
        def confirm_delete(e):
            nonlocal current_template, current_template_path
            success = template_manager.delete_template(template_path)
            if success:
                page.snack_bar = ft.SnackBar(ft.Text("テンプレートを削除しました"))
                page.snack_bar.open = True
                current_template = None
                current_template_path = None
                load_template_list()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("テンプレート削除に失敗しました"))
                page.snack_bar.open = True
            
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("確認"),
            content=ft.Text(f"テンプレート '{template_name_str}' を削除しますか？"),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: setattr(dlg, "open", False)),
                ft.TextButton("削除", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def save_template():
        """現在のテンプレートを保存"""
        if not current_template:
            page.snack_bar = ft.SnackBar(ft.Text("テンプレートが選択されていません"))
            page.snack_bar.open = True
            page.update()
            return
        
        # テンプレート情報を更新
        current_template["name"] = template_name.value
        current_template["background"] = bg_path.value
        
        # 商品画像位置とサイズを更新
        current_template["product_position"] = (int(product_pos_x.value or 0), int(product_pos_y.value or 0))
        current_template["product_size"] = (int(product_size_w.value or 0), int(product_size_h.value or 0))
        
        # テンプレートを保存
        success = template_manager.update_template(current_template, current_template_path)
        
        if success:
            page.snack_bar = ft.SnackBar(ft.Text("テンプレートを保存しました"))
            page.snack_bar.open = True
            load_template_list()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("テンプレート保存に失敗しました"))
            page.snack_bar.open = True
    
    def add_text_element():
        """テキスト要素を追加"""
        if not current_template:
            page.snack_bar = ft.SnackBar(ft.Text("テンプレートを選択してください"))
            page.snack_bar.open = True
            page.update()
            return
        
        def save_text_element(e):
            if not text_field.value:
                text_field.error_text = "テキストを入力してください"
                dlg.update()
                return
            
            new_element = {
                "text": text_field.value,
                "position": (int(pos_x.value or 0), int(pos_y.value or 0)),
                "font": font_field.value or "arial.ttf",
                "font_size": int(font_size.value or 24),
                "color": (0, 0, 0)  # 簡易実装のため固定
            }
            
            if "text_elements" not in current_template:
                current_template["text_elements"] = []
            
            current_template["text_elements"].append(new_element)
            update_text_elements_list()
            
            dlg.open = False
            page.update()
        
        text_field = ft.TextField(label="テキスト", hint_text="${name}のように変数を使用できます")
        pos_x = ft.TextField(label="X位置", value="250", keyboard_type=ft.KeyboardType.NUMBER)
        pos_y = ft.TextField(label="Y位置", value="500", keyboard_type=ft.KeyboardType.NUMBER)
        font_field = ft.TextField(label="フォント", value="arial.ttf")
        font_size = ft.TextField(label="フォントサイズ", value="24", keyboard_type=ft.KeyboardType.NUMBER)
        
        dlg = ft.AlertDialog(
            title=ft.Text("テキスト要素追加"),
            content=ft.Column(
                [
                    text_field,
                    ft.Row([pos_x, pos_y]),
                    font_field,
                    font_size
                ],
                width=400,
                height=250,
                spacing=10
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: setattr(dlg, "open", False)),
                ft.TextButton("追加", on_click=save_text_element)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def edit_text_element():
        """テキスト要素を編集"""
        # 実装省略（時間の都合上）
        page.snack_bar = ft.SnackBar(ft.Text("この機能はまだ実装されていません"))
        page.snack_bar.open = True
        page.update()
    
    def remove_text_element():
        """テキスト要素を削除"""
        # 実装省略（時間の都合上）
        page.snack_bar = ft.SnackBar(ft.Text("この機能はまだ実装されていません"))
        page.snack_bar.open = True
        page.update()
    
    def add_image_element():
        """装飾要素を追加"""
        if not current_template:
            page.snack_bar = ft.SnackBar(ft.Text("テンプレートを選択してください"))
            page.snack_bar.open = True
            page.update()
            return
            
        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                file_path = e.files[0].path
                
                new_element = {
                    "path": file_path,
                    "position": (400, 400),
                    "size": (100, 100)
                }
                
                if "image_elements" not in current_template:
                    current_template["image_elements"] = []
                
                current_template["image_elements"].append(new_element)
                update_image_elements_list()
        
        file_picker = ft.FilePicker(on_result=pick_file_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(
            dialog_title="装飾画像を選択",
            file_type=ft.FilePickerFileType.IMAGE,
            allowed_extensions=["png", "jpg", "jpeg"]
        )
    
    def edit_image_element():
        """装飾要素を編集"""
        # 実装省略（時間の都合上）
        page.snack_bar = ft.SnackBar(ft.Text("この機能はまだ実装されていません"))
        page.snack_bar.open = True
        page.update()
    
    def remove_image_element():
        """装飾要素を削除"""
        # 実装省略（時間の都合上）
        page.snack_bar = ft.SnackBar(ft.Text("この機能はまだ実装されていません"))
        page.snack_bar.open = True
        page.update()
    
    # ボタンバー
    button_bar = ft.Row(
        [
            ft.ElevatedButton(
                "新規テンプレート",
                icon=ft.Icons.ADD,
                on_click=lambda _: create_new_template()
            ),
            ft.ElevatedButton(
                "テンプレート削除",
                icon=ft.Icons.DELETE,
                on_click=lambda _: delete_template()
            ),
            loading
        ],
        alignment=ft.MainAxisAlignment.END
    )
    
    # メインレイアウト
    main_layout = ft.Row(
        [
            # 左側：テンプレート一覧
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("テンプレート一覧", size=16, weight=ft.FontWeight.BOLD),
                                    button_bar
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Divider(),
                            template_list
                        ]
                    ),
                    padding=10,
                    width=300,
                    height=650
                )
            ),
            
            # 右側：テンプレート編集
            ft.Card(
                content=ft.Container(
                    content=template_form,
                    padding=10,
                    width=600,
                    height=650
                ),
                expand=True
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )
    
    # テンプレート一覧を初期ロード
    load_template_list()
    
    return ft.Container(
        content=main_layout,
        padding=20,
        expand=True
    )
