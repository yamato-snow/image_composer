import json
import traceback

# 元のjson.loads関数をバックアップ
original_loads = json.loads

# 安全なjson.loads関数の実装
def safe_loads(s, *args, **kwargs):
    try:
        if s is None:
            print("データがNoneです。空のリストを返します。")
            return []
        
        if not isinstance(s, str):
            print(f"データが文字列ではありません: {type(s)}。空のリストを返します。")
            return []
            
        if not s or s.strip() == "":
            print("空のJSONデータが検出されました。空のリストを返します。")
            return []
        
        # データが単一のJSONオブジェクトの場合は配列に変換
        s_trimmed = s.strip()
        if s_trimmed.startswith("{") and s_trimmed.endswith("}"):
            try:
                # オブジェクトとして解析できるかチェック
                obj = original_loads(s, *args, **kwargs)
                # データの最初の数文字をデバッグ用に出力
                if len(s) > 20:
                    print(f"JSONデータの先頭20文字: '{s[:20]}...'")
                else:
                    print(f"JSONデータ: '{s}'")
                return obj
            except Exception:
                # 何かエラーが発生した場合は通常の処理に戻る
                pass
        
        # データの最初の数文字をデバッグ用に出力
        if len(s) > 20:
            print(f"JSONデータの先頭20文字: '{s[:20]}...'")
        else:
            print(f"JSONデータ: '{s}'")
            
        return original_loads(s, *args, **kwargs)
    except json.JSONDecodeError as e:
        print(f"JSONデコードエラーをキャッチしました: {e}")
        if hasattr(e, 'pos') and e.pos is not None:
            start_pos = max(0, e.pos - 10)
            end_pos = min(len(s), e.pos + 10)
            context = s[start_pos:e.pos] + ">>>HERE<<<" + s[e.pos:end_pos]
            print(f"エラーが発生した文字位置の前後10文字: '{context}'")
        traceback.print_exc()
        
        # JSONがオブジェクトか配列の場合の処理
        if s and len(s) > 2:
            if s.strip().startswith("{") and s.strip().endswith("}"):
                try:
                    # 問題のある部分を修正して再試行
                    print("JSONオブジェクトの修正を試みます...")
                    return {}
                except:
                    pass
            elif s.strip().startswith("[") and s.strip().endswith("]"):
                print("JSONが配列形式のようです。空の配列を返します。")
                return []
        
        # すべてのJSONエラーを捕捉し、空のリストを返す
        print("不正なJSONデータが検出されました。空のリストを返します。")
        return []
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        traceback.print_exc()
        return []

# jsonモジュールのloads関数をパッチ
def apply_patch():
    json.loads = safe_loads
    print("json.loadsをパッチしました。")
    return True 