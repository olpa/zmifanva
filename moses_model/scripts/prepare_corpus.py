#!/usr/bin/env python3

import argparse
import collections
import glob
import itertools
import os
import random
import xml.etree.ElementTree as ET

from convert_solr_xml_to_bitext import iterate_bitext


def parse_command_line():
    parser = argparse.ArgumentParser(
            description='Create train/dev/test corpus for moses')
    parser.add_argument(
            '--solr-dir', dest='solr_dir', required=True)
    parser.add_argument(
            '--seed', dest='seed', type=int, default=42,
            help='random seed for split')
    parser.add_argument('paths', metavar='base:percentage', nargs='+')
    args = parser.parse_args()
    args.paths = reinterpret_split(args.paths)
    return args


def reinterpret_split(paths):
    def path_to_path_and_percentage(path):
        assert ':' in path, f"Path should contain ':', but does not: {path}"
        new_path, s_perc = path.split(':')
        try:
            perc = float(s_perc)
        except ValueError:
            assert False, f"Should have a number after ':': {path}"
        return (new_path, perc)
    split = list(map(path_to_path_and_percentage, paths))
    total = sum(map(lambda ls: ls[1], split))
    assert int(total) == 100, f"Splits should sum to 100%, got: {total}"
    return split


# for the split 80:20 and the length 1000 return:
# [(0, 799), (799, 999)]
def split_to_indexes(splits, length):
    cum = itertools.accumulate(splits)
    borders = list(map(lambda perc: int(perc * length / 100), cum))
    return list(zip(itertools.chain([0], borders), borders))


Bitext = collections.namedtuple('Bitext', ['en', 'jb'])


def load_bitext_from_dir(base_dir):
    solr_files = glob.glob(os.path.join(base_dir, '*.xml'))
    for fname in solr_files:
        print(f'loading {fname}')
        tree = ET.parse(fname)
        root = tree.getroot()
        yield from iterate_bitext(root)


def write_corpus_file(corpus, fname, from_idx, to_idx):
    print(f'writing {fname}')
    with open(fname, 'w') as h:
        for entry in corpus:
            from_str = entry[from_idx]
            from_str = from_str.replace('\t', ' ')
            h.write(from_str)
            if to_idx is not None:
                to_str = entry[to_idx]
                to_str = to_str.replace('\t', ' ')
                h.write('\t')
                h.write(to_str)
            h.write('\n')


def write_corpus(corpus, index_range, base_name):
    dname = os.path.dirname(base_name)
    os.makedirs(dname, exist_ok=True)
    write_corpus_file(corpus, f'{base_name}.jb-en', 0, 1)
    write_corpus_file(corpus, f'{base_name}.jb', 0, None)
    write_corpus_file(corpus, f'{base_name}.en-jb', 1, 0)
    write_corpus_file(corpus, f'{base_name}.en', 1, None)


def main():
    args = parse_command_line()

    split_spec = list(map(lambda p: p[1], args.paths))
    file_spec = list(map(lambda p: p[0], args.paths))

    corpus = list(load_bitext_from_dir(args.solr_dir))
    split_idx = split_to_indexes(split_spec, len(corpus))
    print(f'Size of the corpus: {len(corpus)} pairs, '
          f'split {split_spec}: {split_idx}')

    random.seed(args.seed)
    random.shuffle(corpus)

    for (base_name, index_range) in zip(file_spec, split_idx):
        write_corpus(corpus, index_range, base_name)


if '__main__' == __name__:
    main()
