import json

# 元のjson.loads関数をバックアップ
original_loads = json.loads

# 安全なjson.loads関数の実装
def safe_loads(s, *args, **kwargs):
    try:
        if not s or s.strip() == "":
            print("空のJSONデータが検出されました。空のリストを返します。")
            return []
        return original_loads(s, *args, **kwargs)
    except json.JSONDecodeError as e:
        print(f"JSONデコードエラーをキャッチしました: {e}")
        # すべてのJSONエラーを捕捉し、空のリストを返す
        print("不正なJSONデータが検出されました。空のリストを返します。")
        return []

# jsonモジュールのloads関数をパッチ
def apply_patch():
    json.loads = safe_loads
    print("json.loadsをパッチしました。")
    return True 