# -*- encoding: utf-8 -*-

'''
把当前目录下的图片文件按拍摄日期进行分类
如果没有拍摄日期，按修改日期分类
'''

import os
import datetime
import shutil
import exifread


def get_file_modification_date(file_name):
    '''
    获得文件修改时间
    '''
    # 获得文件创建时间戳
    file_modification_timestamp = os.path.getmtime(file_name)
    # 转换为创建时间
    file_modification_time = datetime.datetime.fromtimestamp(file_modification_timestamp)
    # 转换为创建日期
    file_modification_date = file_modification_time.strftime('%Y-%m')
    return file_modification_date

def get_file_date(file_name):
    '''
    获得文件拍摄时间，如果没有拍摄时间，用修改时间代替
    '''
    try:
        with open(file_name, 'rb') as file:
            original_data = exifread.process_file(file)
    except:
        return "000" # error code

    try:
        file_date = original_data['EXIF DateTimeOriginal']
        file_date = str(file_date)[:7].replace(':', '-')
        
        print(file_date) # test shot information

        return file_date
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

        # error condition
        if file_date == "000":
            continue

        create_dir(file_date)
        shutil.move(file, os.path.join(file_date, file))

        print('第%d个' % (index + 1))
    print('移动完成!!!')
