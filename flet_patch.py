import json
import traceback
import flet
from flet import app

# オリジナルのon_eventメソッドをバックアップ
original_on_event = None

# パッチを適用する関数
def apply_patch():
    global original_on_event
    
    # flet.appモジュールからon_eventメソッドを取得
    import inspect
    import flet.app
    
    # 必要な関数を特定
    run_socket_server_func = None
    for name, func in inspect.getmembers(flet.app, inspect.isfunction):
        if name == "__run_socket_server":
            run_socket_server_func = func
            break
    
    if run_socket_server_func is None:
        print("警告: __run_socket_server関数が見つかりませんでした。パッチを適用できません。")
        return False
    
    # 関数のソースコードを確認
    source = inspect.getsource(run_socket_server_func)
    if "on_event" not in source:
        print("警告: on_event関数が見つかりませんでした。パッチを適用できません。")
        return False
    
    # on_eventメソッドをパッチ
    # on_eventはローカル関数のため、モンキーパッチが必要
    # 直接パッチを適用するのは難しいため、全体の関数を再定義する
    
    # 代わりに実用的な解決策として、JSONDecodeErrorをキャッチするラッパー関数を作成
    def safe_json_loads(data):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            print("JSONデコードエラーをキャッチしました。空のリストを返します。")
            return []
    
    # jsonモジュールのloads関数をモンキーパッチ
    original_loads = json.loads
    json.loads = safe_json_loads
    
    print("fletのJSONDecodeErrorに対するパッチを適用しました")
    return True 