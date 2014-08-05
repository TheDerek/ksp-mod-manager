
import fnmatch
import os
import shutil
import urllib
import urllib2
import zipfile
import stat
import math
from src.download import Downloader


TEMP_DICT = "temp"
UNZIPPED_TEMP = "temp/unzipped"


def install_from_url(url, install_location):
    if not os.path.isdir(install_location):
        raise DictError("Specified path is not a valid directory")

    if not os.access(install_location, os.W_OK):
        raise DictError("User not allowed to write to specified directory")

    shutil.rmtree(UNZIPPED_TEMP)
    shutil.rmtree(TEMP_DICT)

    os.mkdir(TEMP_DICT)
    os.mkdir(UNZIPPED_TEMP)

    #file_name = TEMP_DICT + "/mod.zip"
    #file_name = download_file(url)
    #file_name = Downloader(url, "")

    downloader = Downloader(url, TEMP_DICT)
    downloader.show()
    downloader.exec_()

    file_name = str(downloader.file_name)

    unzip2(file_name, UNZIPPED_TEMP)
    up_one = False

    for path, dirs, files in os.walk(UNZIPPED_TEMP):
        for f in reversed(dirs):
            print("In folder: " + f)
            if f == "GameData":
                up_one = True
                tree = path + "/" + f
                print("GameData Detected, copying to GameData folder and deleting: " + tree)
                copy_and_delete_tree(tree, install_location)

    if up_one:
        print("Upped one\n")
        copytree(UNZIPPED_TEMP, install_location + "/..")
    else:
        copytree(UNZIPPED_TEMP, install_location)

    os.remove(file_name)

    print("Finished\n")


class DictError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def delete_super_folders(dict, super_folder_name):
    matches = []
    for root, dirnames, filenames in os.walk(dict):
        for filename in fnmatch.filter(filenames, super_folder_name):
            matches.append(os.path.join(root, filename))

    if len(matches) is 0:
        return

    print("Super folder detected, deleting.")

    #Get first GameData Folder
    super_folder = matches[0]
    shutil.copytree(super_folder, dict)
    shutil.rmtree(super_folder)


def copy_and_delete_tree(src, dst, symlinks = False, ignore = None):
    copytree(src, dst, symlinks, ignore)
    shutil.rmtree(src)


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


def download_file(url):
    """Helper to download large files
        the only arg is a url
       this file will go to a temp directory
       the file will also be downloaded
       in chunks and print out how much remains
    """

    baseFile = os.path.basename(url)

    #move the file to a more uniq path
    os.umask(0002)
    temp_path = "/tmp/"
    try:
        file = os.path.join(temp_path, baseFile)
        #file = file_name

        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                print math.floor( (downloaded / total_size) * 100)
                if not chunk: break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False

    return file


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(str(source_filename)) as zf:
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


def unzip2(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)