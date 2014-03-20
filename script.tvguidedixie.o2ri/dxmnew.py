import zipfile
import shutil,os


def unzipAndMove(_in, _out, src):
    try:
        zin = zipfile.ZipFile(unicode(_in), 'r')
        zin.extractall(unicode(_out))
        if src:
            moveFiles(src, _out)
            shutil.rmtree(src)
    except Exception, e:
        print str(e)
        return False

    return True


def moveFiles(root_src_dir,root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)


