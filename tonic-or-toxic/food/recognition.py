from paddleocr import PaddleOCR
import os
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()
image_path = filedialog.askopenfilename()

language = 'English'
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
        polish_additives_beginnings = ('Składniki:', 'Sktadniki:')
        english_additives_beginnings = ("Ingredients:",)
        if language == 'Polish':
            additives_beginnings = polish_additives_beginnings
        else:
            additives_beginnings = english_additives_beginnings
        for beginning in additives_beginnings:
            if beginning in recognized_text:
                recognized_text_from_ingredients = recognized_text.split(beginning)[1]
                print(recognized_text_from_ingredients)
            else:
                print('We have some problems!')
        last_additive = input('Please enter the last food additive:')
        if last_additive in recognized_text_from_ingredients:
            recognized_text_additives = recognized_text_from_ingredients.split(last_additive)[0] + last_additive
            print(recognized_text_additives)
        else:
            print('We have another problem!')
        recognized_text_additives_corrected = recognized_text_additives.replace("*", "").replace("emulsifier:", "")
        print(recognized_text_additives_corrected)
        recognized_text_list = recognized_text_additives_corrected.split(",")
        print(recognized_text_list)
    except Exception as e:
        print(f"Failed to read text from {image_path}. Reason {str(e)}")
else:
    print(f"{image_path} does not exist.")


