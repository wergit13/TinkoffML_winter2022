import sys
import argparse
import numpy as np


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))
    parser.add_argument("scores", type=argparse.FileType("w"))
    return parser


def get_paths(input):
    for i in range(len(input)):
        input[i] = input[i].split()
    return input


def levenstein(s1, s2):
    if len(s1) < len(s2):
        return levenstein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        cur_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = cur_row[j] + 1
            replaces = prev_row[j] + (c1 != c2)
            cur_row.append(min(insertions, deletions, replaces))
        prev_row = cur_row

    return prev_row[-1]


def normalize(arr):
    norm_arr = []
    diff_arr = max(arr) - min(arr)
    if (diff_arr == 0):
        return arr
    for i in arr:
        temp = (i - min(arr)) / diff_arr
        norm_arr.append(temp)
    return norm_arr


def calculate_levenstein_distance(paths):
    with open(paths[0], "r") as file1:
        with open(paths[1], "r") as file2:
            text1 = file1.readlines()
            text2 = file2.readlines()
            if len(text2) > len(text1):
                max_text = text2
                min_text = text1
            else:
                max_text = text1
                min_text = text2
            distances = []

            for i in range(len(max_text)):
                try:
                    distances.append(levenstein(max_text[i], min_text[i]))
                except IndexError:
                    distances.append(len(max_text[i]))  
    return np.mean(normalize(distances))


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    paths = get_paths(args.input.readlines())
    for i in range(len(paths)):
        args.scores.write(str(calculate_levenstein_distance((paths[i]))))
        args.scores.write('\n')
