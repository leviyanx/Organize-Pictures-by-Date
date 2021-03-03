# -*- encoding: utf-8 -*-

'''
把当前目录下的图片文件按拍摄日期进行重命名
如果没有拍摄日期，按修改日期重命名

如果遇到同一时刻的两张图，不覆盖，给同时刻的后面的图片的名字里加上时间戳，
然后人工处理。
'''

import os
import datetime
import shutil
import exifread
import time


def get_file_modification_date(file_name):
    '''
    获得文件修改时间
    '''
    # 获得文件创建时间戳
    file_modification_timestamp = os.path.getmtime(file_name)
    # 转换为创建时间
    file_modification_time = datetime.datetime.fromtimestamp(file_modification_timestamp)
    # 转换为创建日期
    file_modification_date = file_modification_time.strftime('%Y-%m-%d %H.%M.%S')
    return file_modification_date


def get_file_date(file_name):
    '''
    获得文件拍摄时间，如果没有拍摄时间，用修改时间代替
    '''
    try:
        with open(file_name, 'rb') as file:
            original_data = exifread.process_file(file)
    except:
        return "000"

    try:
        file_origin_date = original_data['EXIF DateTimeOriginal']
        file_date = str(file_origin_date)[:10].replace(':', '-') # 文件日期
        file_time = str(file_origin_date)[11:19].replace(':', '.') # 文件时间
        final_file_datetime = file_date + " " + file_time # 文件日期+时间

        return str(final_file_datetime)
    except:
        return get_file_modification_date(file_name)


def get_current_dir_files():
    '''
    获得当前目录的所有文件，排除.py文件
    '''
    # 获得当前目录的所有文件和文件夹
    files_and_dirs = os.listdir()
    # 过滤文件夹
    files = [file for file in files_and_dirs if (os.path.isfile(file) and file[-3:] != '.py')]
    return files


def create_dir(dir_name):
    # 文件夹不存在是创建文件夹
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)


if __name__ == '__main__':
    files = get_current_dir_files()
    print('共%d个文件' % len(files))

    for index, file in enumerate(files):
        file_date = get_file_date(file)

        # 跳过异常文件
        if file_date == "000":
            continue

        # 源文件名和目标文件名
        source_file_name = file
        file_type = os.path.splitext(file)[-1]
        target_file_name = file_date + file_type

        # 跳过命名正确的文件
        if source_file_name == target_file_name:
            continue

        try:
            os.rename(source_file_name, target_file_name)
        except:
            # 遇到同时刻的文件，名字里加上现在的时间戳
            target_file_name = file_date + "(" + str(time.time()) + ")" + file_type
            os.rename(source_file_name, target_file_name)

        print('第%d个' % (index + 1))
    print('完成!!!')
