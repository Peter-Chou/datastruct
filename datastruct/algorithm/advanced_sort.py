# -*- coding: utf-8 -*-


def merge_sort(seq):
    if len(seq) <= 1:
        return seq
    else:
        mid = int(len(seq)/2)
        left_half = merge_sort(seq[:mid])
        right_half = merge_sort(seq[mid:])
    # 合并两个有序的数组
    new_seq = merge_sorted_list(left_half, right_half)
    return new_seq


def merge_sorted_list(sorted_a, sorted_b):
    """合并两个有序数组，返回一个新的有序数组"""
    len_a, len_b = len(sorted_a), len(sorted_b)
    a = b = 0
    new_sorted_seq = list()

    while a < len_a and b < len_b:
        if sorted_a[a] < sorted_b[b]:
            new_sorted_seq.append(sorted_a[a])
            a += 1
        else:
            new_sorted_seq.append(sorted_b[b])
            b += 1

    while a < len_a:
        new_sorted_seq.append(sorted_a[a])
        a += 1
    while b < len_b:
        new_sorted_seq.append(sorted_b[b])
        b += 1

    return new_sorted_seq
