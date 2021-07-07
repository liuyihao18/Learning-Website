import torchvision

from Learning.constants import *

if __name__ == '__main__':
    # 创建相应文件夹
    try:
        os.mkdir(extra_args['data_path'])
        print("Create directory:", extra_args['data_path'])
    except FileExistsError:
        pass
    # 数据集准备
    torchvision.datasets.MNIST(root=extra_args['data_path'],
                               download=True)
    try:
        os.mkdir(extra_args['save_path'])
        print("Create directory:", extra_args['save_path'])
    except FileExistsError:
        pass
    for sub_save_path in sub_save_paths:
        try:
            os.mkdir(extra_args['save_path'] + os.sep + sub_save_path)
            print("Create directory:", extra_args['save_path'] + os.sep + sub_save_path)
        except FileExistsError:
            pass
