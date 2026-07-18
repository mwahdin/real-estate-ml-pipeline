def persian_to_number(text):
    if not text:
        return None

    # تبدیل اعداد فارسی به انگلیسی
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    text = text.replace("٫", ".").replace(",", "")

    # تبدیل میلیارد و میلیون
    if "میلیارد" in text:
        return float(text.replace("میلیارد", "").strip()) * 1_000_000_000
    elif "میلیون" in text:
        return float(text.replace("میلیون", "").strip()) * 1_000_000

    return float(text)


def extract_number(text):
    if not text:
        return None

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)

    digits = "".join(filter(str.isdigit, text))

    return int(digits) if digits else None
