import re
# from text.japanese import japanese_to_romaji_with_accent, japanese_to_ipa, japanese_to_ipa2, japanese_to_ipa3
from text.korean import latin_to_hangul, number_to_hangul, divide_hangul, korean_to_lazy_ipa, korean_to_ipa
# from text.mandarin import number_to_chinese, chinese_to_bopomofo, latin_to_bopomofo, chinese_to_romaji, chinese_to_lazy_ipa, chinese_to_ipa, chinese_to_ipa2
# from text.sanskrit import devanagari_to_ipa
# from text.english import english_to_lazy_ipa, english_to_ipa2, english_to_lazy_ipa2
# from text.thai import num_to_thai, latin_to_thai
# from text.shanghainese import shanghainese_to_ipa
# from text.cantonese import cantonese_to_ipa
# from text.ngu_dialect import ngu_dialect_to_ipa


# def japanese_cleaners(text):
#     text = japanese_to_romaji_with_accent(text)
#     text = re.sub(r'([A-Za-z])$', r'\1.', text)
#     return text


# def japanese_cleaners2(text):
#     return japanese_cleaners(text).replace('ts', 'ʦ').replace('...', '…')


def korean_cleaners(text):
    '''Pipeline for Korean text'''
    text = latin_to_hangul(text)
    text = number_to_hangul(text)
    text = divide_hangul(text)
    text = re.sub(r'([\u3131-\u3163])$', r'\1.', text)
    return text