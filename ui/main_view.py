import flet as ft

from ui.template_view import TemplateView
from ui.batch_view import BatchView

def MainView(page):
    """アプリケーションのメインビュー"""
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            # メインビュー
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("画像合成自動化ツール"),
                            center_title=True,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("画像レイアウト自動化ツール", size=24, weight=ft.FontWeight.BOLD),
                                    ft.Text("複数の商品素材と所定のテキスト、イラスト、背景などを自動的に合成します。", size=16),
                                    ft.Container(height=30),
                                    
                                    ft.Container(
                                        content=ft.ElevatedButton(
                                            text="テンプレート管理",
                                            icon=ft.icons.PALETTE,
                                            on_click=lambda _: page.go("/template"),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10), 
                                                padding=ft.padding.all(20)
                                            ),
                                            width=250
                                        ),
                                        alignment=ft.alignment.center
                                    ),
                                    
                                    ft.Container(height=20),
                                    
                                    ft.Container(
                                        content=ft.ElevatedButton(
                                            text="バッチ処理実行",
                                            icon=ft.icons.PLAY_ARROW,
                                            on_click=lambda _: page.go("/batch"),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10), 
                                                padding=ft.padding.all(20)
                                            ),
                                            width=250
                                        ),
                                        alignment=ft.alignment.center
                                    ),
                                    
                                    ft.Container(height=30),
                                    
                                    ft.Container(
                                        content=ft.Row(
                                            [ft.Text("© 2025 画像合成自動化ツール", size=12, color=ft.colors.GREY)],
                                            alignment=ft.MainAxisAlignment.END
                                        ),
                                        alignment=ft.alignment.bottom_right,
                                        margin=ft.margin.only(right=20, bottom=20)
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                            padding=ft.padding.all(20)
                        )
                    ]
                )
            )
        
        elif page.route == "/template":
            # テンプレート管理ビュー
            page.views.append(
                ft.View(
                    route="/template",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("テンプレート管理"),
                            center_title=True,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            actions=[
                                ft.IconButton(icon=ft.icons.HOME, on_click=lambda _: page.go("/"))
                            ]
                        ),
                        TemplateView(page)
                    ]
                )
            )
        
        elif page.route == "/batch":
            # バッチ処理ビュー
            page.views.append(
                ft.View(
                    route="/batch",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("バッチ処理実行"),
                            center_title=True,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            actions=[
                                ft.IconButton(icon=ft.icons.HOME, on_click=lambda _: page.go("/"))
                            ]
                        ),
                        BatchView(page)
                    ]
                )
            )
        
        page.update()
    
    # ルート変更ハンドラを設定
    page.on_route_change = route_change
    
    # ダークモード対応
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # ナビゲーションの初期化
    page.go("/")
