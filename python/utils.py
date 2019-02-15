# -*- encoding: utf-8 -*-


def get_file_md5(file_path):
    """
    获取文件的md5值
    :param file_path: 文件路径
    :return:
    """
    import os
    import hashlib
    if os.path.isfile(file_path):
        md5obj = hashlib.md5()
        maxbuf = 8192
        f = open(file_path, 'rb')
        while True:
            buf = f.read(maxbuf)
            if not buf:
                break
            md5obj.update(buf)
        f.close()
        t_hash = md5obj.hexdigest()
        return str(t_hash).upper()
    return None


def copytree(src, dst, symlinks=False):
    """
    目录拷贝
    :param src: 待拷贝的源目录
    :param dst: 需要拷贝的目标目录
    :param symlinks:
    :return:
    """
    import os
    import shutil

    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)

    errors = []
    for name in names:
        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(src_name):
                linkto = os.readlink(src_name)
                os.symlink(linkto, dst_name)
            elif os.path.isdir(src_name):
                copytree(src_name, dst_name, symlinks)
            else:
                if os.path.isdir(dst_name):
                    os.rmdir(dst_name)
                elif os.path.isfile(dst_name):
                    os.remove(dst_name)
                shutil.copy2(src_name, dst_name)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((src_name, dst_name, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except OSError as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    pass


def post(url, params=None, data=None, headers=None):
    """
    获取post数据
    :param url: 请求的url
    :param params: 参数
    :param data: 请求数据
    :param headers: 请求头部
    :return:
    """
    import requests
    if headers is None:
        headers = {'User-Agent': "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"}

    response = requests.post(url, params=params, data=data, headers=headers)
    if response.status_code == 200:
        return response.content.decode("utf-8")
    else:
        return ''


def get_file_encoding(file_path, def_encoding='utf-8'):

    """
    获取文件编码方式
    :param file_path: 文件路径
    :param def_encoding: 默认编码方式
    :return:
    """

    import os

    if os.path.exists(file_path):
        with open(file_path, 'rb+') as f:
            import chardet
            encode = chardet.detect(f.read())
            # print(encode)
            enc = encode.get('encoding', def_encoding)
            if enc.lower().startswith('utf-16'):
                enc = def_encoding

            return enc

    return def_encoding
