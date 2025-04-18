from PIL import Image, ImageDraw, ImageFont
import os
import json

class ImageProcessor:
    def __init__(self):
        self.fonts_cache = {}
        
    def get_font(self, font_name, font_size):
        """フォントをキャッシュから取得またはロード"""
        key = f"{font_name}_{font_size}"
        if key not in self.fonts_cache:
            try:
                self.fonts_cache[key] = ImageFont.truetype(font_name, font_size)
            except:
                # デフォルトフォントにフォールバック
                self.fonts_cache[key] = ImageFont.load_default()
        return self.fonts_cache[key]
    
    def apply_template(self, product_image_path, product_data, template):
        """テンプレートを適用して画像を合成"""
        # 背景画像を読み込む
        if template.get('background'):
            base_img = Image.open(template['background']).convert('RGBA')
        else:
            # デフォルト背景（白）を作成
            base_img = Image.new('RGBA', (800, 800), (255, 255, 255, 255))
        
        # 商品画像を読み込む
        try:
            prod_img = Image.open(product_image_path).convert('RGBA')
            
            # 商品画像のリサイズ（テンプレートに指定されたサイズ）
            if 'product_size' in template:
                width, height = template['product_size']
                prod_img = prod_img.resize((width, height), Image.LANCZOS)
            
            # 商品画像の配置
            product_pos = template.get('product_position', (0, 0))
            base_img.paste(prod_img, product_pos, prod_img)
        except Exception as e:
            print(f"商品画像の処理エラー: {e}")
        
        # テキスト追加
        draw = ImageDraw.Draw(base_img)
        for text_element in template.get('text_elements', []):
            text = text_element['text']
            
            # テキスト内の変数を商品データで置換
            for key, value in product_data.items():
                text = text.replace(f"${{{key}}}", str(value))
            
            position = text_element.get('position', (0, 0))
            font_name = text_element.get('font', 'arial.ttf')
            font_size = text_element.get('font_size', 24)
            color = text_element.get('color', (0, 0, 0))
            
            # 色情報がリスト形式の場合はタプルに変換
            if isinstance(color, list):
                color = tuple(color)
            
            font = self.get_font(font_name, font_size)
            draw.text(position, text, font=font, fill=color)
        
        # イラスト/装飾要素の追加
        for image_element in template.get('image_elements', []):
            try:
                element_img = Image.open(image_element['path']).convert('RGBA')
                
                # サイズ調整
                if 'size' in image_element:
                    width, height = image_element['size']
                    element_img = element_img.resize((width, height), Image.LANCZOS)
                
                position = image_element.get('position', (0, 0))
                base_img.paste(element_img, position, element_img)
            except Exception as e:
                print(f"装飾要素の処理エラー: {e}")
        
        return base_img
    
    def batch_process(self, csv_data, image_folder, template, output_folder, progress_callback=None):
        """CSVデータを使って一括処理"""
        os.makedirs(output_folder, exist_ok=True)
        
        # テンプレートの座標・サイズデータがリスト形式の場合はタプルに変換
        if isinstance(template.get('product_position'), list):
            template['product_position'] = tuple(template['product_position'])
        
        if isinstance(template.get('product_size'), list):
            template['product_size'] = tuple(template['product_size'])
        
        # テキスト要素の色情報とポジションをタプルに変換
        for text_elem in template.get('text_elements', []):
            if isinstance(text_elem.get('color'), list):
                text_elem['color'] = tuple(text_elem['color'])
            if isinstance(text_elem.get('position'), list):
                text_elem['position'] = tuple(text_elem['position'])
        
        # 装飾画像要素のポジションとサイズをタプルに変換
        for image_elem in template.get('image_elements', []):
            if isinstance(image_elem.get('position'), list):
                image_elem['position'] = tuple(image_elem['position'])
            if isinstance(image_elem.get('size'), list):
                image_elem['size'] = tuple(image_elem['size'])
        
        total = len(csv_data)
        processed = 0
        errors = 0
        
        for index, row in csv_data.iterrows():
            product_data = row.to_dict()
            
            # 商品画像パスの構築
            image_file = product_data.get('image_file', '')
            if not image_file:
                errors += 1
                continue
                
            product_image_path = os.path.join(image_folder, image_file)
            
            # 画像が存在するか確認
            if not os.path.exists(product_image_path):
                print(f"画像ファイルが見つかりません: {product_image_path}")
                errors += 1
                continue
            
            try:
                # テンプレート適用
                result_image = self.apply_template(product_image_path, product_data, template)
                
                # 出力ファイル名を生成
                output_filename = f"{product_data.get('id', index)}.png"
                output_path = os.path.join(output_folder, output_filename)
                
                # 画像を保存
                result_image.save(output_path)
                
                processed += 1
                
                # 進捗コールバック
                if progress_callback:
                    progress_callback(processed, total)
                    
            except Exception as e:
                print(f"処理エラー（ID: {product_data.get('id', index)}）: {e}")
                errors += 1
        
        return processed, errors
