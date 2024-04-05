from paddleocr import PaddleOCR
import os

image_path = 'images_to_recognize/Ingredients_pl_en.jpg'
language = 'Polish'

if os.path.exists(image_path):
    if language == 'English':
        lang_rec = 'en'
    elif language == 'Polish':
        lang_rec = 'pl'
    ocr = PaddleOCR(use_angle_cls=True, lang=lang_rec)
    try:
        result = ocr.ocr(image_path, cls=True)
        recognized_text = ""
        for line in result:
            for item in line:
                item_text = item[-1][0]
                recognized_text += item_text + " "
        print(recognized_text)
        polish_language_additives_beginnings = ('Składniki:', 'Sktadniki:')
        for beginning in polish_language_additives_beginnings:
            if beginning in recognized_text:
                recognized_text_from_ingredients = recognized_text.split(beginning)[1]
                print(recognized_text_from_ingredients)
        last_additive = input('Please enter the last food additive:') + '.'
        if last_additive in recognized_text_from_ingredients:
            recognized_text_additives = recognized_text_from_ingredients.split(last_additive)[0] + last_additive[:-1]
            print(recognized_text_additives)
    except Exception as e:
        print(f"Failed to read text from {image_path}. Reason {str(e)}")
else:
    print(f"{image_path} does not exist.")


