# from functools import reduce
# import keyboard
# import mouse
# import time
# import desktopmagic.screengrab_win32 as desktop
#
#
# def luhn(code):
#     # Предварительно рассчитанные результаты умножения на 2 с вычетом 9 для больших цифр
#     # Номер индекса равен числу, над которым проводится операция
#     LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
#     code = reduce(str.__add__, filter(str.isdigit, code))
#     evens = sum(int(i) for i in code[-1::-2])
#     odds = sum(LOOKUP[int(i)] for i in code[-2::-2])
#     return (evens + odds) % 10 == 0
#
#
# def type_the_code(num):
#     for i in str(num):
#         keyboard.send(min(keyboard.key_to_scan_codes(i)))
#
#
# def is_valid():
#     im = desktop.getRectAsImage((2151, 627, 2460, 647)).convert("LA")
#     white = black = 0
#     for p in im.getdata():
#         white += p[0]
#         black += p[1]
#     return white / black > 0.05
#
#
# def try_code(code, delay=0.5):
#     keyboard.send('ctrl+a')
#     type_the_code(code)
#     time.sleep(delay)
#     if is_valid():
#         print(code.upper())
#
#
# def click(x, y, return_mouse=True):
#     current_mouse_loc = mouse.get_position()
#     mouse.move(x, y)
#     mouse.click()
#     if return_mouse:
#         mouse.move(*current_mouse_loc)
#
#
# def set_mouse():
#     click(2296, 568)
#     mouse.move(35, 826)
#
#
# def refresh():
#     click(3051, 271)  # close window
#     click(2594, 719)  # choose the date
#     click(2895, 584, return_mouse=False)  # choose the ticket
#     mouse.wheel(-3)  # scroll to buy button
#     click(2895, 584)  # press buy button
#     set_mouse()
#
#
# word_list = []
# # word_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
# # word_list = ['black', 'actor']
# # word_list = ['insta']
# word_list = ['bar', 'kitchen', 'moshkov', 'stuff', 'test', 'discount', 'code', 'promo', 'promocode']
# # word_list = ['']
# # word_list = ['']
# # word_list = ['']
#
# for word in word_list:
#     try_code(word)
#     for number in range(10):
#         try_code('{}{}'.format(word, number))
#     refresh()

import requests
import string


def try_code(code):
    cookies = {"SESSI0a73a1d963effe19622915414914bdca": "umdk93sr59a4rojra1n99ssgr6"}
    request_data = {
        "cd_nid": None,
        "ldt_id": "2",
        "pay_order_by_bonuses": False,
        "promocode": code,
        "pt_id": "sberbank_card",
        "remove_ticket": None
    }
    response_data = requests.post("https://w.intickets.ru/ajax/ordering-get-data", json=request_data,
                                  cookies=cookies)
    print(response_data.text)
    response_data = response_data.json()
    if response_data['cost']['total_discount'] > 0:
        print("{} - {}%".format(request_data['promocode'],
                                int((response_data['cost']['total_discount'] / response_data['cost'][
                                    'total_orig']) * 100)))


separator = "###"
codes = string.ascii_uppercase

code_list = []
for code in codes:
    code_list.append(code)
    code_list.extend("{}{:02}".format(code, i) for i in range(10))
    code_list.extend("{}{}".format(code, i) for i in range(10))
    code_list.extend("{}{}".format(code, i) for i in range(10, 31))
    code_list.append(separator)

i = 0
for code in code_list:
    if code == separator:
        i += 1
        print("{} / 26".format(i))
    else:
        try_code(code)
