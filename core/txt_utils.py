def clean_up_txt():
    try:
        with open('outputs/emergency_result.json', 'w', encoding='utf-8') as file:
            file.write('')
        with open('outputs/excel.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return True
    except:
        return False


def logs_txt(mode: int, text: str = '', serial_number: int | str = ''):
    # excel result
    if mode == 1:
        with open('outputs/excel.txt', 'a', encoding='utf-8') as file:
            file.write(f'{serial_number}|{text},\n')

    # emergency result
    if mode == 2:
        with open('outputs/emergency_result.json', 'a', encoding='utf-8') as file:
            file.write(
                f'{text},\n')
