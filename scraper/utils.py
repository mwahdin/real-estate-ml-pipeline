import pandas as pd
import re

def persian_to_number(text):
    if text is None:
        return None

    text = str(text).strip()

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    text = text.replace("٫", ".").replace(",", "")

    if "میلیارد" in text:
        return float(text.replace("میلیارد", "").strip()) * 1_000_000_000

    if "میلیون" in text:
        return float(text.replace("میلیون", "").strip()) * 1_000_000

    # استخراج اولین عدد از متن
    match = re.search(r"\d+(\.\d+)?", text)

    if match:
        return float(match.group())

    return None




def extract_number(text):

    if pd.isna(text):
        return None

    text = str(text)

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    numbers = re.findall(r"\d+", text)

    if not numbers:
        return None

    return int(numbers[0])




def parse_floor(text):
    if text is None:
        return None, None

    text = str(text).strip()

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    # همکف
    if text == "همکف":
        return 0, None

    # زیرهمکف
    if text == "زیرهمکف":
        return -1, None

    # همکف از ۴
    if text.startswith("همکف از"):
        total = int(re.findall(r"\d+", text)[0])
        return 0, total

    # زیرهمکف از ۴
    if text.startswith("زیرهمکف از"):
        total = int(re.findall(r"\d+", text)[0])
        return -1, total

    # ۴ از ۶
    if "از" in text:
        nums = re.findall(r"\d+", text)

        if len(nums) == 2:
            return int(nums[0]), int(nums[1])

    # فقط ۳
    nums = re.findall(r"\d+", text)

    if len(nums) == 1:
        return int(nums[0]), None

    return None, None