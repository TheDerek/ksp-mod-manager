
import fnmatch
import os
import shutil
import urllib
import zipfile
import stat


TEMP_DICT = "temp"
UNZIPPED_TEMP = "temp/unzipped"


def install_from_url(url, install_location):
    shutil.rmtree(UNZIPPED_TEMP)
    shutil.rmtree(TEMP_DICT)

    os.mkdir(TEMP_DICT)
    os.mkdir(UNZIPPED_TEMP)

    file_name = TEMP_DICT + "/mod.zip"
    download_file(url, file_name)
    unzip(file_name, UNZIPPED_TEMP)

    copytree(UNZIPPED_TEMP, install_location)
    os.remove(file_name)


def delete_super_folders(dict, super_folder_name):
    matches = []
    for root, dirnames, filenames in os.walk(dict):
        for filename in fnmatch.filter(filenames, super_folder_name):
            matches.append(os.path.join(root, filename))

    if len(matches) is 0:
        return

    #Get first GameData Folder
    super_folder = matches[0]
    shutil.copytree(super_folder, dict)
    shutil.rmtree(super_folder)


def copytree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def download_file(url, file_name=None):
    #url = "http://download.thinkbroadband.com/10MB.zip"
    if file_name is None:
        file_name = url.split('/')[-1]

    urllib.urlretrieve(url, file_name)


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)