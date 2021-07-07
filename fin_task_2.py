import argparse
import os
import collections
from scipy.stats import entropy


parser = argparse.ArgumentParser(description='This utility detect encrypted/compressed files',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter, prefix_chars='-+',
                                allow_abbrev=True)

parser.add_argument('-d', '--dir', default='./',
                    help='specifies the path to directory where to look for encrypted/compressed files.')
parser.add_argument('-c', '--confidence', default=80, type=int,
                    help='specifies the threshold level of confidence (in percents from 0 to 100) to treat '
                         'a certain file as encryped/compressed.')
parser.add_argument('-p', '--print-confidence', dest='p', action='store_true',
                    help='print the confidence level along with the file name.')

parser.add_argument('-s', dest='descending', help='specifies the path to directory where to look '
                                                  'for encrypted/compressed files.',
                    action='store_true')
parser.add_argument('+s', dest='ascending', help='specifies the path to directory where to look '
                                                 'for encrypted/compressed files.',
                    action='store_true')

args = parser.parse_args()

folder = args.dir
file_list = []
dict_f = {}


def estimate_shannon_entropy(dna_sequence):
    bases = collections.Counter([tmp_base for tmp_base in dna_sequence])
    dist = [x / sum(bases.values()) for x in bases.values()]

    entropy_value = entropy(dist, base=2)

    confidence = round(entropy_value / 8 * 100)

    return confidence


for file in os.listdir(folder):
    if os.path.isfile(folder+file):
        file_list.append(file)

for i in file_list:
    confidence = estimate_shannon_entropy(i)
    if confidence > args.confidence:
        dict_f[confidence] = i


def sort_dict(dict_s, rev=False):
    if rev:
        sorted_dict = {k: v for k, v in sorted(dict_s.items(), key=lambda item: item[0], reverse=True)}
    else:
        sorted_dict = {k: v for k, v in sorted(dict_s.items(), key=lambda item: item[0])}
    return sorted_dict


def print_dict(dict_p, confidence=False):
    if confidence:
        for key, value in dict_p.items():
            print(key, '%', value)
    else:
        for key, value in dict_p.items():
            print(value)


if args.p and args.descending:
    sorted_dict = sort_dict(dict_f, rev=True)
    print_dict(sorted_dict, confidence=True)
elif args.p and args.ascending:
    sorted_dict = sort_dict(dict_f)
    print_dict(sorted_dict, confidence=True)
elif args.p:
    print_dict(dict_f, confidence=True)
elif args.descending:
    sorted_dict = sort_dict(dict_f, rev=True)
    print_dict(sorted_dict)
elif args.ascending:
    sorted_dict = sort_dict(dict_f)
    print_dict(sorted_dict)
else:
    print_dict(dict_f)
