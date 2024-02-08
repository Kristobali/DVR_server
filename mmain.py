import json
import time
import psutil
from platform import uname
import os

def get_files(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def get_formatted_size(size):
    if size < 1024 * 1024:  # Меньше 1 МБ
        return f"{size / 1024:.2f} KB"
    elif 1024 * 1024 <= size < 1024 * 1024 * 1024:  # От 1 МБ до 1 ГБ
        return f"{size / (1024 * 1024):.2f} MB"
    else:  # Больше или равно 1 ГБ
        return f"{size / (1024 * 1024 * 1024):.2f} GB"

def get_largest_file_size(files):
    max_size = 0
    for file in files:
        file_size = os.path.getsize(file)
        if file_size > max_size:
            max_size = file_size
    return max_size

def divide_into_segments(max_size):
    segment_size = max_size / 5
    segments = [(segment_size * i, segment_size * (i + 1)) for i in range(5)]
    return segments

def group_files_by_segment(files, segments):
    grouped_files = {segment: [] for segment in segments}
    for file in files:
        file_size = os.path.getsize(file)
        for segment in segments:
            if segment[0] <= file_size <= segment[1]:  # Включаем файлы с размером, совпадающим с верхней границей сегмента
                grouped_files[segment].append((file, file_size))
                break
    return grouped_files


if __name__ == "__main__":
    directory = input("Введите путь к папке: ")
    files = get_files(directory)
    max_size = get_largest_file_size(files)
    segments = divide_into_segments(max_size)
    grouped_files = group_files_by_segment(files, segments)

    print("Файлы по сегментам:")
    for segment, files in grouped_files.items():
        print(f"Сегмент {segments.index(segment) + 1}:")
        segment_start, segment_end = segment
        print(f"Диапазон размера: от {get_formatted_size(segment_start)} до {get_formatted_size(segment_end)}")
        for file, size in files:
            print(f"  Файл: {file}, Размер: {get_formatted_size(size)}")
        print()

    print("Отдельные файлы:")
    for file in files:
        size = os.path.getsize(file)
        print(f"Файл: {file}, Размер: {get_formatted_size(size)}")


#--------------------------------------------------------------------
        
# def correct_size(bts, ending='iB'):
#     size = 1024
#     for item in ["", "K", "M", "G", "T", "P"]:
#         if bts < size:
#             return f"{bts:.2f}{item}{ending}"
#         bts /= size


# def creating_file():
#     collect_info_dict = dict()
#     if 'info' not in collect_info_dict:
#         collect_info_dict['info'] = dict()
#         collect_info_dict['info']['system_info'] = dict()
#         collect_info_dict['info']['system_info'] = {'system': {'comp_name': uname().node,
#                                                                'os_name': f"{uname().system} {uname().release}",
#                                                                'version': uname().version,
#                                                                'machine': uname().machine},
#                                                     'processor': {'name': uname().processor,
#                                                                   'phisycal_core': psutil.cpu_count(logical=False),
#                                                                   'all_core': psutil.cpu_count(logical=True),
#                                                                   'freq_max': f"{psutil.cpu_freq().max:.2f}Мгц"},
#                                                     'ram': {'volume': correct_size(psutil.virtual_memory().total),
#                                                             'aviable': correct_size(psutil.virtual_memory().available),
#                                                             'used': correct_size(psutil.virtual_memory().used)}}

#     for partition in psutil.disk_partitions():
#         try:
#             partition_usage = psutil.disk_usage(partition.mountpoint)
#         except PermissionError:
#             continue
#         if 'disk_info' not in collect_info_dict['info']:
#             collect_info_dict['info']['disk_info'] = dict()
#         if f"'device': {partition.device}" not in collect_info_dict['info']['disk_info']:
#             collect_info_dict['info']['disk_info'][partition.device] = dict()
#             collect_info_dict['info']['disk_info'][partition.device] = {'file_system': partition.fstype,
#                                                                         'size_total': correct_size(
#                                                                             partition_usage.total),
#                                                                         'size_used': correct_size(
#                                                                             partition_usage.used),
#                                                                         'size_free': correct_size(
#                                                                             partition_usage.free),
#                                                                         'percent':
#                                                                             f'{partition_usage.percent}'}

#     for interface_name, interface_address in psutil.net_if_addrs().items():
#         if interface_name == 'Loopback Pseudo-Interface 1':
#             continue
#         else:
#             if 'net_info' not in collect_info_dict['info']:
#                 collect_info_dict['info']['net_info'] = dict()
#             if interface_name not in collect_info_dict['info']['net_info']:
#                 collect_info_dict['info']['net_info'][interface_name] = dict()
#                 collect_info_dict['info']['net_info'][interface_name] = {
#                     'mac': interface_address[0].address.replace("-", ":"),
#                     'ipv4': interface_address[1].address,
#                     'ipv6': interface_address[2].address}

#     return collect_info_dict


# def print_info(dict_info):
#     for item in dict_info['info']:
#         if item == "system_info":
#             for elem in dict_info['info'][item]:
#                 if elem == 'system':
#                     print(f"[+] Информация о системе\n"
#                           f"\t- Имя компьютера: {dict_info['info'][item][elem]['comp_name']}\n"
#                           f"\t- Опереционная система: {dict_info['info'][item][elem]['os_name']}\n"
#                           f"\t- Сборка: {dict_info['info'][item][elem]['version']}\n"
#                           f"\t- Архитектура: {dict_info['info'][item][elem]['machine']}\n")
#                 if elem == 'processor':
#                     print(f"[+] Информация о процессоре\n"
#                           f"\t- Семейство: {dict_info['info'][item][elem]['name']}\n"
#                           f"\t- Физические ядра: {dict_info['info'][item][elem]['phisycal_core']}\n"
#                           f"\t- Всего ядер: {dict_info['info'][item][elem]['all_core']}\n"
#                           f"\t- Максимальная частота: {dict_info['info'][item][elem]['freq_max']}\n")
#                 if elem == 'ram':
#                     print(f"[+] Оперативная память\n"
#                           f"\t- Объем: {dict_info['info'][item][elem]['volume']}\n"
#                           f"\t- Доступно: {dict_info['info'][item][elem]['aviable']}\n"
#                           f"\t- Используется: {dict_info['info'][item][elem]['used']}\n")
#         if item == "disk_info":
#             for elem in dict_info['info'][item]:
#                 print(f"[+] Информация о дисках\n"
#                       f"\t- Имя диска: {elem}\n"
#                       f"\t- Файловая система: {dict_info['info'][item][elem]['file_system']}\n"
#                       f"\t- Объем диска: {dict_info['info'][item][elem]['size_total']}\n"
#                       f"\t- Занято: {dict_info['info'][item][elem]['size_used']}\n"
#                       f"\t- Свободно: {dict_info['info'][item][elem]['size_free']}\n"
#                       f"\t- Заполненность: {dict_info['info'][item][elem]['percent']}%\n")
#         if item == "net_info":
#             for elem in dict_info['info'][item]:
#                 print(f"[+] Информация о сети\n"
#                       f"\t- Имя интерфейса: {elem}\n"
#                       f"\t- MAC-адрес: {dict_info['info'][item][elem]['mac']}\n"
#                       f"\t- IPv4: {dict_info['info'][item][elem]['ipv4']}\n"
#                       f"\t- IPv6: {dict_info['info'][item][elem]['ipv6']}\n")


# def main():
#     if uname().system == "Windows":
#         dict_info = creating_file()
#         with open(f'info_{uname().node}.json', 'w', encoding='utf-8') as file:
#             json.dump(dict_info, file, indent=4, ensure_ascii=False)
#         print_info(dict_info)
#     elif uname().system == "Linux":
#         dict_info = creating_file()
#         with open(f'info_{uname().node}.json', 'w', encoding='utf-8') as file:
#             json.dump(dict_info, file, indent=4, ensure_ascii=False)
#         print_info(dict_info)

#--------------------------------------------------------------------
        
# while True:
#     cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
#     for i, percentage in enumerate(cpu_percents):
#         print(f"Использование ядра процессора {i+1}: {percentage:.2f}%")
#     time.sleep(10)

# if __name__ == "__main__":
#     main()
