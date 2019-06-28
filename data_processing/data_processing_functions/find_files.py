import os


def find_files(mode, path, key):
    if mode == 0:
        return [path]
    elif mode == 1:
        files = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if key in filename:
                    files.append(os.path.join(dirpath, filename))
        return files
