import sys

print(sys.path)

# from PIL import Image, ImageDraw, ImageFont

# def generate_image_from_text(text, image_size=(400, 200), font_size=20, font_path=None, background_color="white", text_color="black"):
#     # 画像の生成
#     image = Image.new("RGB", image_size, background_color)
#     draw = ImageDraw.Draw(image)

#     # フォントの指定
#     if font_path is None:
#         font = ImageFont.load_default()
#     else:
#         font = ImageFont.truetype(font_path, font_size)

#     # テキストの描画
#     text_width, text_height = draw.textsize(text, font=font)
#     text_x = (image_size[0] - text_width) / 2
#     text_y = (image_size[1] - text_height) / 2
#     draw.text((text_x, text_y), text, fill=text_color, font=font)

#     return image

# # テキスト
# input_text = "こんにちは、世界!"

# # 画像の生成
# image = generate_image_from_text(input_text)

# # 画像の保存
# image.save("text_image.png")

# # 画像の表示
# image.show()
