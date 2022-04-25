#!/usr/bin/env python3

import argparse
from functools import partial
import os
import re
import shutil


def parse_command_line():
    parser = argparse.ArgumentParser(description='Copy model, adapt paths')
    parser.add_argument('--from-ini', dest='from_ini', required=True)
    parser.add_argument('--to-dir', dest='to_dir', required=True)
    parser.add_argument('--base-marker', dest='base_marker', required=True)
    parser.add_argument('--new-path', dest='new_path', required=True)
    return parser.parse_args()


re_path = re.compile(' path=([^ ]+)')


def copy_ini(h_in, h_out, path_to_relative_func, path_in_ini):
    files = []
    for li in h_in:
        m = re_path.search(li)
        if m:
            orig_path = m.group(1)
            files.append(get_model_path(orig_path))
            rel_path = path_to_relative_func(orig_path)
            dist_path = os.path.join(path_in_ini, os.path.basename(rel_path))
            new_path = f' path={dist_path}'
            li = re_path.sub(new_path, li)
        h_out.write(li)
    return files


def get_model_path(orig_path):
    if 'phrase-table' in orig_path:
        return f'{orig_path}.minphr'
    if 'reordering-table' in orig_path:
        return f'{orig_path}.minlexr'
    return orig_path


def get_relative_path(base_marker, file_name):
    pos = file_name.rfind(base_marker)
    assert pos != -1, \
        'The marker not found in the path: marker: ' \
        f'${base_marker}, path: ${file_name}'
    new_file_name = file_name[pos + len(base_marker):]
    while new_file_name[0] == '/':
        new_file_name = new_file_name[1:]
    return new_file_name


def copy_files(base_marker, moses_ini, out_dir, files):
    moses_rel = get_relative_path(base_marker, moses_ini)
    in_base = moses_ini[:-len(moses_rel)]
    print('in_base, moses_rel, marker', in_base, moses_rel, base_marker)
    for fname in files:
        in_file = os.path.join(in_base, get_relative_path(base_marker, fname))
        out_file = os.path.join(out_dir, os.path.basename(in_file))
        shutil.copy(in_file, out_file)


def main():
    args = parse_command_line()
    out_ini = os.path.join(args.to_dir, os.path.basename(args.from_ini))
    os.makedirs(args.to_dir, exist_ok=True)
    with open(args.from_ini) as h_in, open(out_ini, 'w') as h_out:
        func_rel = partial(get_relative_path, args.base_marker)
        files = copy_ini(h_in, h_out, func_rel, args.new_path)
    copy_files(args.base_marker, args.from_ini, args.to_dir, files)


if __name__ == '__main__':
    main()
