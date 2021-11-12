import argparse
import json
import logging
import pickle
from collections import defaultdict

import sortvalid.validator as validator
from sortvalid.constants import PATTERN_DCT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sort valid")


def __segment_is_invalid(segment: list):
    """
    :param segment: Сегмент(список) который необходимо проверить на необходимость сортировать по сегментам.
    :return: Возвращает True, если спиок необходимо сортировать по сегментам, False в противоположном случае.
    """
    s = sum(segment)
    length = len(segment)
    for i in segment:
        if i != s / length:
            return True
    return False


def sort_by_segments(array: list):
    """
    :param array: Список чисел, который необходимо отсортировать.
    :return: Возвращает отсортированный список.
    """
    if bool(array):
        bucket_below_zero = []
        bucket_above_zero = []
        normalization = sum(array) / len(array)
        if not normalization:
            normalization = 1
        for element in range(len(array)):
            bucket_above_zero.append([])
            bucket_below_zero.append([])
        for value in array:
            index_in_bucket = abs(int(value / normalization))
            if value >= 0:
                if index_in_bucket < len(array):
                    bucket_above_zero[index_in_bucket].append(value)
                else:
                    bucket_above_zero[len(array) - 1].append(value)
            else:
                if index_in_bucket < len(array):
                    bucket_below_zero[index_in_bucket].append(value)
                else:
                    bucket_below_zero[len(array) - 1].append(value)
        for element in bucket_below_zero:
            element.reverse()
        bucket_below_zero.reverse()
        bucket = bucket_below_zero + bucket_above_zero
        sorted_data = []
        for segment in bucket:
            if bool(segment):
                if __segment_is_invalid(segment):
                    segment = sort_by_segments(segment)
                sorted_data += segment
            else:
                continue
        return sorted_data
    else:
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='File to sort')
    parser.add_argument("output", help='File to write sorted data in')
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.loads(f.read())

    sorted_valid_data = []
    temp_dct = defaultdict(list)
    records = []
    for dct in data:
        records.append(validator.Record(dct))
    temp_valid_data = validator.Validator(records, PATTERN_DCT).validate()
    for record in temp_valid_data:
        for key in record.keys():
            if isinstance((record.data[key]), int):
                temp_dct[record.data[key]].append(record)
                break
    logger.info('Sort...')
    sorted_keys = sort_by_segments(list(temp_dct.keys()))
    for key in sorted_keys:
        for value in temp_dct[key]:
            sorted_valid_data.append(value)

    logger.info(f"Serialize to file {args.output}...")
    with open(args.output, 'wb') as file:
        pickle.dump(sorted_valid_data, file)
    logger.info(f"De-serialize from file {args.output}...")
    with open(args.output, 'rb') as file:
        pickle_obj = pickle.load(file)
    logger.info(f"Serialization is correct:{sorted_valid_data == pickle_obj}")
