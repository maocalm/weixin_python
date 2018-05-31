import subprocess
import os
import shutil

import tinify as tinify
from PIL import Image
import sys

# 自定义pngquant.exe路径，这里是当前取当前目录下
PNGQUANT_PATH = os.path.join(os.getcwd(), 'pngquant.exe')

# 自定义多个tinify_keys存放到列表，使用前请替换
tinify_keys = ["vqZIaeRi9hUBxzGcSNVOf5hCfs5WJHGO", "AJ4Z720EjZZQJpDnt2K7rhaQINSqpA4i",
               "Ien9JtUYxlofltsbDQCSX6cTAajCxyy2", "pPGFXhJ7ugVXdVQbbJDzV2T98StuuBFF"]


# tinify_keys = ["pPGFXhJ7ugVXdVQbbJDzV2T98StuuBFF", "Ien9JtUYxlofltsbDQCSX6cTAajCxyy2", "Ien9JtUYxlofltsbDQCSX6cTAajCxyy2" ,"pPGFXhJ7ugVXdVQbbJDzV2T98StuuBFF"]


def CompressByPillow(fromFile, out_dir):
    print("do CompressByPillow..")
    try:
        for root, dir, files in os.walk(fromFile):
            print("****************************************************************************************")
            print("root dir:" + root)
            print("dir:" + str(dir))
            for file in files:
                current_file = os.path.join(root, file)
                dirName = os.path.basename(root)
                # 如果没有指定输出路径，则默认覆盖当前文件
                if not out_dir:
                    out_dir = fromFile
                targetDir = os.path.join(out_dir, dirName)
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                # 如果是.9图片或者非图片文件不做处理,直接做拷贝
                if not file.endswith(".9.png") and (file.endswith(".png") or file.endswith(".jpg")):
                    print(
                        "--------------------------------------------------------------------------------------------")
                    print("currrent file:" + current_file)
                    im = Image.open(current_file)
                    origin_size = os.path.getsize(current_file)

                    if file.endswith(".png"):
                        im = im.convert('P')
                    im.save(os.path.join(targetDir, file), optimize=True)

                    target_file = os.path.join(targetDir, file)
                    compress_size = os.path.getsize(target_file)
                    print('%.2f' % ((origin_size - compress_size) / origin_size))
                else:
                    if not out_dir or out_dir == fromFile:
                        continue
                    shutil.copy(current_file, os.path.join(targetDir, file))

    except Exception as e:
        print(e.message)


def CompressByPillow(fromFile, out_dir):
    print("do CompressByPillow..")
    try:
        for root, dir, files in os.walk(fromFile):
            print("****************************************************************************************")
            print("root dir:" + root)
            print("dir:" + str(dir))
            for file in files:
                current_file = os.path.join(root, file)
                dirName = os.path.basename(root)
                # 如果没有指定输出路径，则默认覆盖当前文件
                if not out_dir:
                    out_dir = fromFile
                targetDir = os.path.join(out_dir, dirName)
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                # 如果是.9图片或者非图片文件不做处理,直接做拷贝
                if not file.endswith(".9.png") and (file.endswith(".png") or file.endswith(".jpg")):
                    print(
                        "--------------------------------------------------------------------------------------------")
                    print("currrent file:" + current_file)
                    origin_size = os.path.getsize(current_file)
                    target_file = os.path.join(targetDir, file)

                    cmd_command = '"{0}" 256 -s1 --force --quality=50-50 "{1}" -o "{2}"'.format(PNGQUANT_PATH,
                                                                                                current_file,
                                                                                                target_file)
                    print("cmd_command:" + cmd_command)
                    # 执行命令
                    p = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    retval = p.wait()

                    compress_size = os.path.getsize(target_file)
                    print('%.2f' % ((origin_size - compress_size) / origin_size))
                else:
                    if not out_dir or out_dir == fromFile:
                        continue
                    shutil.copy(current_file, os.path.join(targetDir, file))

    except Exception as e:
        print(e.message)


def CompressByTinypng(fromFile, out_dir):
    print("do CompressByTinypng..")
    try:
        for root, dir, files in os.walk(fromFile):
            print("****************************************************************************************")
            print("root dir:" + root)
            print("dir:" + str(dir))
            for file in files:
                current_file = os.path.join(root, file)
                dirName = os.path.basename(root)
                # 如果没有指定输出路径，则默认覆盖当前文件
                if not out_dir:
                    out_dir = fromFile
                targetDir = os.path.join(out_dir, dirName)
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                # 如果是.9图片或者非图片文件不做处理,直接做拷贝
                if not file.endswith(".9.png") and (file.endswith(".png") or file.endswith(".jpg")):
                    print(
                        "--------------------------------------------------------------------------------------------")
                    for key in tinify_keys:
                        # 验证当前API key是否可以用，不可以用就切换下一个账号
                        tinify.key = key
                        try:
                            valid = tinify.validate()
                            if valid:
                                print("currrent file:" + current_file)
                                origin_size = os.path.getsize(current_file)
                                source = tinify.from_file(current_file)
                                target_file = os.path.join(targetDir, file)
                                source.to_file(target_file)
                                compress_size = os.path.getsize(target_file)
                                print('%.2f' % ((origin_size - compress_size) / origin_size))
                                break
                            else:
                                continue
                        except Exception as e:
                            # Something else went wrong, unrelated to the Tinify API.
                            print("error while compressing png image:" + e.message)
                            continue
                else:
                    if not out_dir or out_dir == fromFile:
                        continue
                    shutil.copy(current_file, os.path.join(targetDir, file))

    except Exception as e:
        print(e.message)


CompressByTinypng('C:/Users/hanwenmao/Desktop/PNG/100-999_kb_png', 'C:/Users/hanwenmao/Desktop/PNG/100-999_kb_my')
# CompressByPillow('imgting/wmb010.png', 'imgting/a.png')
