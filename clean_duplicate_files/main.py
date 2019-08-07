import os
import argparse

# factor by which file sizes of duplicates are allowed to differ to be still considered duplicates
Q = 0.98
# number of mismatching characters allowed at the beginning of the file name
NO_MISMATCHING_CHARS_PREFIX = 5

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path of the top directory')
    parser.add_argument("-s", "--clean-subdirs", action='store_true', default=False,
                        help="Duplicates are removed recursively for each sub directory. " +
                             "(Default=False: duplicates are removed recursively from top directory)")
    parser.add_argument("-d", "--dry-run", action='store_true', default=False,
                        help="Dry run: no deletion, just listing the duplicates. Default: no dry run")
    args = parser.parse_args()
    path = args.path
    if not path or path == '.':
        path = os.getcwd()
    elif path == '..':
        path = os.path.dirname(os.getcwd())
    print(f"Looking for duplicates in {path}")
    if args.clean_subdirs:
        for dir_name in list_subdirectories(path):
            dir_path = os.path.join(path, dir_name)
            clean_duplicates_in_directory(dir_path, dict(), args.dry_run)
    else:
        clean_duplicates_in_directory(path, dict(), args.dry_run)


def clean_duplicates_in_directory(dir_path, cache, is_dry_run):
    print(f"Checking {dir_path}")
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            basename = os.path.basename(name)
            is_dupes_found = False
            os_stats = os.stat(os.path.join(root, name))
            for filename in cache.keys():
                name_length = min(len(filename), len(basename))
                match_length = name_length - NO_MISMATCHING_CHARS_PREFIX
                # be quite liberal what coincidence of filename concerns
                if len(longest_common_suffix(filename, basename)) >= match_length:
                    # compare file sizes
                    diff = cache[filename]["file_size"] / os_stats.st_size
                    is_dupes_found = (1.0 <= diff <= 1.0 / Q) or (1.0 >= diff >= Q)
                    if is_dupes_found:
                        delete_duplicate_confirmation(cache[filename]['path'], file_path, is_dry_run)
                        break
            if not is_dupes_found:
                stats = dict()
                stats["path"] = file_path
                stats["file_size"] = os_stats.st_size
                cache[basename] = stats


def delete_duplicate_confirmation(first_path, duplicate_path, is_dry_run):
    print("")
    print("Found duplicate.")
    print(f"{first_path}")
    print(f"{duplicate_path}")
    if not is_dry_run:
        confirm = input("For deleting second file type 'y/yes/second', for deleting first file type 'first'. ")
        if confirm in ['y', 'yes', 'second']:
            os.remove(duplicate_path)
        if confirm in ['first']:
            os.remove(first_path)


def list_subdirectories(top_dir):
    """
    returns sub directories to a given path
    :param top_dir: path to parent directory
    :return: list of directory paths
    """
    return [sub for sub in os.listdir(top_dir) if os.path.isdir(os.path.join(top_dir, sub))]


def longest_common_prefix(seq1, seq2):
    """
    taken from https://www.quora.com/What-is-the-easiest-way-to-find-the-longest-common-prefix-or-suffix-of-two-sequences-in-Python
    :param seq1: first string 
    :param seq2: second string
    :return: the prefix
    """
    start = 0
    while start < min(len(seq1), len(seq2)):
        if seq1[start] != seq2[start]:
            break
        start += 1
    return seq1[:start]


def longest_common_suffix(seq1, seq2):
    # apply revers string operation
    return longest_common_prefix(seq1[::-1], seq2[::-1])[::-1]
