import os


def find_files(mode, path, find_name):
    if mode == 0:
        return {os.path.split(path)[-1]: path}
    elif mode == 1:
        files = dict()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename == find_name:
                    files[os.path.split(dirpath)[-1]] = os.path.join(dirpath, filename)
        return files
