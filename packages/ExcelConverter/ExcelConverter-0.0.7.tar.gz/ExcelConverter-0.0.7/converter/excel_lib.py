"""
Python equivalents of various excel functions
"""

# TODOMatthijs: waarom faalt de test hieronder?
# Foutmelding bij mij: ImportError: cannot import name 'Cell'

import numpy as np
from datetime import datetime
from math import log
from decimal import Decimal, ROUND_HALF_UP
from collections import Iterable, Counter
from converter.excel_util import flatten, is_number, date_from_int, normalize_year, is_leap_year, \
    find_corresponding_index

# #####################################################################################
# A dictionary that maps excel function names onto python equivalents. You should
# only add an entry to this map if the python name is different to the excel name
# (which it may need to be to prevent conflicts with existing python functions
# with that name, e.g., max).

# So if excel defines a function foobar(), all you have to do is add a function
# called foobar to this module.  You only need to add it to the function map,
# if you want to use a different name in the python code. 

# Note: some functions (if, pi, atan2, and, or, array, ...) are already taken care of
# in the FunctionNode code, so adding them here will have no effect.
FUNCTION_MAP = {
    "ln": "xlog",
    "min": "xmin",
    "max": "xmax",
    "sum": "xsum",
    "gammaln": "lgamma",
    "round": "xround",
    "VerschilDekking": "verschildekking",
}

######################################################################################
# List of excel equivalent functions
# TODO: needs unit testing

def value(text):
    # make the distinction for naca numbers
    if text.find('.') > 0:
        return float(text)
    else:
        return int(text)

def xlog(a):
    if isinstance(a, (list, tuple, np.ndarray)):
        return [log(x) for x in flatten(a)]
    else:
        # print a
        return log(a)

def xmax(*args):
    # ignore non numeric cells
    data = [x for x in flatten(args) if isinstance(x, (int, float))]

    # however, if no non numeric cells, return zero (is what excel does)
    if len(data) < 1:
        return 0
    else:
        return max(data)

def xmin(*args):
    # ignore non numeric cells
    data = [x for x in flatten(args) if isinstance(x, (int, float))]

    # however, if no non numeric cells, return zero (is what excel does)
    if len(data) < 1:
        return 0
    else:

        return min(data)

def xsum(*args):
    # ignore Non Numeric Cells
    data = [x for x in flatten(args) if isinstance(x, (int))]

    # however, if no non numeric cells, return zero (is what excel does)
    if len(data) < 1:
        return 0
    else:
        return sum(data)

def sumif(total_range, criteria,
          sum_range=None):
    # Excel reference: https://support.office.com/en-us/article/SUMIF-function-169b8c99-c05c-4483-a712-1697a653039b

    # WARNING: 
    # - wildcards not supported
    # - doesn't really follow 2nd remark about sum_range length

    if sum_range is None:
        sum_range = []
    if type(total_range) != list:
        raise TypeError('%s must be a list' % str(total_range))

    if type(sum_range) != list:
        raise TypeError('%s must be a list' % str(sum_range))

    if isinstance(criteria, list) and not isinstance(criteria, (str, bool)):  # ugly...
        return 0

    indexes = find_corresponding_index(total_range, criteria)

    def f(x):
        return sum_range[x] if x < len(sum_range) else 0

    if len(sum_range) == 0:
        return sum([total_range[x] for x in indexes])
    else:
        return sum(map(f, indexes))

def average(*args):
    l = list(flatten(*args))
    return sum(l) / len(l)

def right(text, n):
    if isinstance(text, str) or isinstance(text, str):
        return text[-n:]
    else:
        # TODO: get rid of the decimal
        return str(int(text))[-n:]

def index(*args):
    array = args[0]
    row = args[1]

    if len(args) == 3:
        col = args[2]
    else:
        col = 1

    if isinstance(array[0], (list, tuple, np.ndarray)):
        # rectangular array
        array[row - 1][col - 1]
    elif row == 1 or col == 1:
        return array[row - 1] if col == 1 else array[col - 1]
    else:
        raise Exception("index (%s,%s) out of range for %s" % (row, col, array))

def lookup(value, lookup_range, result_range):
    if not isinstance(value, (int, float)):
        raise Exception("Non numeric lookups (%s) not supported" % value)

    # TODO: note, may return the last equal value

    # index of the last numeric value
    lastnum = -1
    for i, v in enumerate(lookup_range):
        if isinstance(v, (int, float)):
            if v > value:
                break
            else:
                lastnum = i

    if lastnum < 0:
        raise Exception("No numeric data found in the lookup range")
    else:
        if i == 0:
            raise Exception("All values in the lookup range are bigger than %s" % value)
        else:
            if i >= len(lookup_range) - 1:
                # return the biggest number smaller than value
                return result_range[lastnum]
            else:
                return result_range[i - 1]

"""
It will convert the list of rows to a dictionary such that the keys correspond 
to the first column in the list of row and the values to the column indicated through the 
argument col index.
"""
def to_Dictionary(row_list, col_index_num):
    return {row[0]: row[col_index_num] for row in row_list}

def hlookup_row(item, row_dict, case_sensitive=False):
    if not case_sensitive:
        for key in row_dict.keys():
            if str(key).lower() == str(item).lower():
                return row_dict[key]
    else:
        return row_dict[item]

"""
Method_doc of Vlookup Function
@item: The value you want to lookup
@rows: Each row specified in the lookup range
@col_index_num: The Number of the column to look for the item
@case_sensitive: Checks the if the item is a string if so set it to Lowercase
"""
def vlookup(item, rows, col_index_num, case_sensitive=False):
    # Get the range from excel and put it in a list
    rows = [x for x in rows if x is not None]  # remove any None values
    col_values = to_Dictionary(rows, col_index_num - 1)
    return vlookup_column(item, col_values, case_sensitive)

"""
":" means Start:End
Finds the specified col_index_num in excel rows and selects that row
and creates a dictionary of the specified row
"""
def create_column_dict(excel_rows, col_index_num, case_sensitive=False):
    if case_sensitive:
        return {row: row[col_index_num] for row in excel_rows}
    else:
        return {row[0]: row[col_index_num] for row in excel_rows}

"""
Gets the given lookup_value in the column dictionary, and returns the key with value
"""
def vlookup_column(item, column_values, case_sensitive=False):
    if case_sensitive:
        for key in column_values.keys():
            if (str(key).lower() == str(item).lower()):
                return column_values[key]
    else:
        return column_values[item]

# TODOMatthijs: doc?
def hlookup(item, rows, row_index_num, case_sensitive=False):
    rows = [x for x in rows if x is not None]
    for i in range(len(rows[0])):
        if (str(rows[0][i]).lower() == str(item).lower() if case_sensitive else str(rows[0][i]) == str(item)):
            return rows[row_index_num - 1][i]
    return None

# Change item from Uppercase to Lowercase
def lower_case_item(item):
    if isinstance(item, Iterable):
        item = [str(entry).lower() for entry in item]
        return item
    else:
        return str(item).lower()

def linest(*args, **kwargs):
    y = args[0]
    x = args[1]

    if len(args) == 3:
        const = args[2]
        if isinstance(const, str):
            const = (const.lower() == "true")
    else:
        const = True

    degree = kwargs.get('degree', 1)

    # build the vandermonde matrix
    a = np.vander(x, degree + 1)

    if not const:
        # force the intercept to zero
        a[:, -1] = np.zeros((1, len(x)))

    # perform the fit
    (coefs, residuals, rank, sing_vals) = np.linalg.lstsq(a, y)

    return coefs

def npv(*args):
    discount_rate = args[0]
    cashflow = args[1]
    return sum([float(x) * (1 + discount_rate) ** -(i + 1) for (i, x) in enumerate(cashflow)])

def match(lookup_value, lookup_array, match_type=1):
    def type_convert(value):
        if type(value) == str:
            value = value.lower()
        elif type(value) == int:
            value = float(value)

        return value

    lookup_value = type_convert(lookup_value)

    if match_type == 1:
        # Verify ascending sort
        posmax = -1
        for i in range((len(lookup_array))):
            current = type_convert(lookup_array[i])

            if i is not len(lookup_array) - 1 and current > type_convert(lookup_array[i + 1]):
                raise Exception('for match_type 0, lookup_array must be sorted ascending')
            if current <= lookup_value:
                posmax = i
        if posmax == -1:
            raise Exception('no result in lookup_array for match_type 0')
        return posmax + 1  # Excel starts at 1

    elif match_type == 0:
        # No string wildcard
        return [type_convert(x) for x in lookup_array].index(lookup_value) + 1

    elif match_type == -1:
        # Verify descending sort
        posmin = -1
        for i in range((len(lookup_array))):
            current = type_convert(lookup_array[i])

            if i is not len(lookup_array) - 1 and current < type_convert(lookup_array[i + 1]):
                raise Exception("for match_type 0, lookup_array must be sorted descending")
            if current >= lookup_value:
                posmin = i
        if posmin == -1:
            raise Exception('no result in lookup_array for match_type 0')
        return posmin + 1  # Excel starts at 1

def mod(nb,
        q):
    # Excel Reference: https://support.office.com/en-us/article/MOD-function-9b6cd169-b6ee-406a-a97b-edf2a9dc24f3
    if not isinstance(nb, int):
        raise TypeError("%s is not an integer" % str(nb))
    elif not isinstance(q, int):
        raise TypeError("%s is not an integer" % str(q))
    else:
        return nb % q

def count(
        *args):
    # Excel reference: https://support.office.com/en-us/article/COUNT-function-a59cd7fc-b623-4d93-87a4-d23bf411294c
    l = list(args)

    total = 0

    for arg in l:
        if type(arg) == list:
            total += len([x for x in arg if is_number(x) and type(x) is not bool])  # count inside a list
        elif is_number(arg):  # int() is used for text representation of numbers
            total += 1

    return total

def countif(range, criteria):
    # Excel reference: https://support.office.com/en-us/article/COUNTIF-function-e0de10c6-f885-4e71-abb4-1f464816df34

    # WARNING: 
    # - wildcards not supported
    # - support of strings with >, <, <=, =>, <> not provided

    valid = find_corresponding_index(range, criteria)

    return len(valid)

def countifs(
        *args):
    # Excel reference: https://support.office.com/en-us/article/COUNTIFS-function-dda3dc6e-f74e-4aee-88bc-aa8c2a866842

    arg_list = list(args)
    l = len(arg_list)

    if l % 2 != 0:
        raise Exception('excellib.countifs() must have a pair number of arguments, here %d' % l)

    if l >= 2:
        indexes = find_corresponding_index(args[0], args[1])  # find indexes that match first layer of countif

        remaining_ranges = [elem for i, elem in enumerate(arg_list[2:]) if i % 2 == 0]  # get only ranges
        remaining_criteria = [elem for i, elem in enumerate(arg_list[2:]) if i % 2 == 1]  # get only criteria

        filtered_remaining_ranges = []

        for range in remaining_ranges:  # filter items in remaining_ranges that match valid indexes from first countif layer
            filtered_remaining_range = []

            for index, item in enumerate(range):
                if index in indexes:
                    filtered_remaining_range.append(item)

            filtered_remaining_ranges.append(filtered_remaining_range)

        new_tuple = ()

        for index, range in enumerate(
                filtered_remaining_ranges):  # rebuild the tuple that will be the argument of next layer
            new_tuple += (range, remaining_criteria[index])

        return min(countifs(*new_tuple), len(indexes))  # only consider the minimum number across all layer responses

    else:
        return float('inf')

def xround(number,
           num_digits=0):  # Excel reference: https://support.office.com/en-us/article/ROUND-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c

    if not is_number(number):
        raise TypeError("%s is not a number" % str(number))
    if not is_number(num_digits):
        raise TypeError("%s is not a number" % str(num_digits))

    if num_digits >= 0:  # round to the right side of the point
        return float(Decimal(repr(number)).quantize(Decimal(repr(pow(10, -num_digits))), rounding=ROUND_HALF_UP))
        # see https://docs.python.org/2/library/functions.html#round
        # and https://gist.github.com/ejamesc/cedc886c5f36e2d075c5

    else:
        return round(number, num_digits)

def mid(text, start_num,
        num_chars):  # Excel reference: https://support.office.com/en-us/article/MID-MIDB-functions-d5f9e25c-d7d6-472e-b568-4ecb12433028

    text = str(text)

    if type(start_num) != int:
        raise TypeError("%s is not an integer" % str(start_num))
    if type(num_chars) != int:
        raise TypeError("%s is not an integer" % str(num_chars))

    if start_num < 1:
        raise ValueError("%s is < 1" % str(start_num))
    if num_chars < 0:
        raise ValueError("%s is < 0" % str(num_chars))

    return text[start_num:num_chars]

def date(year, month,
         day):  # Excel reference: https://support.office.com/en-us/article/DATE-function-e36c0c8c-4104-49da-ab83-82328b832349

    if type(year) != int:
        raise TypeError("%s is not an integer" % str(year))

    if type(month) != int:
        raise TypeError("%s is not an integer" % str(month))

    if type(day) != int:
        raise TypeError("%s is not an integer" % str(day))

    if year < 0 or year > 9999:
        raise ValueError("Year must be between 1 and 9999, instead %s" % str(year))

    if year < 1900:
        year = 1900 + year

    year, month, day = normalize_year(year, month, day)  # taking into account negative month and day values

    date_0 = datetime(1900, 1, 1)
    date = datetime(year, month, day)

    result = (datetime(year, month, day) - date_0).days + 2

    if result <= 0:
        raise ArithmeticError("Date result is negative")
    else:
        return result

def yearfrac(start_date, end_date,
             basis=0):  # Excel reference: https://support.office.com/en-us/article/YEARFRAC-function-3844141e-c76d-4143-82b6-208454ddc6a8

    def actual_nb_days_ISDA(start, end):  # needed to separate days_in_leap_year from days_not_leap_year
        y1, m1, d1 = start
        y2, m2, d2 = end

        days_in_leap_year = 0
        days_not_in_leap_year = 0

        year_range = list(range(y1, y2 + 1))

        for y in year_range:

            if y == y1 and y == y2:
                nb_days = date(y2, m2, d2) - date(y1, m1, d1)
            elif y == y1:
                nb_days = date(y1 + 1, 1, 1) - date(y1, m1, d1)
            elif y == y2:
                nb_days = date(y2, m2, d2) - date(y2, 1, 1)
            else:
                nb_days = 366 if is_leap_year(y) else 365

            if is_leap_year(y):
                days_in_leap_year += nb_days
            else:
                days_not_in_leap_year += nb_days

        return days_not_in_leap_year, days_in_leap_year

    def actual_nb_days_AFB_alter(start,
                                 end):  # http://svn.finmath.net/finmath%20lib/trunk/src/main/java/net/finmath/time/daycount/DayCountConvention_ACT_ACT_YEARFRAC.java
        y1, m1, d1 = start
        y2, m2, d2 = end

        delta = date(*end) - date(*start)

        if delta <= 365:
            if is_leap_year(y1) and is_leap_year(y2):
                denom = 366
            elif is_leap_year(y1) and date(y1, m1, d1) <= date(y1, 2, 29):
                denom = 366
            elif is_leap_year(y2) and date(y2, m2, d2) >= date(y2, 2, 29):
                denom = 366
            else:
                denom = 365
        else:
            year_range = list(range(y1, y2 + 1))
            nb = 0

            for y in year_range:
                nb += 366 if is_leap_year(y) else 365

            denom = nb / len(year_range)

        return delta / denom

    if not is_number(start_date):
        raise TypeError("start_date %s must be a number" % str(start_date))
    if not is_number(end_date):
        raise TypeError("end_date %s must be number" % str(end_date))
    if start_date < 0:
        raise ValueError("start_date %s must be positive" % str(start_date))
    if end_date < 0:
        raise ValueError("end_date %s must be positive" % str(end_date))

    if start_date > end_date:  # switch dates if start_date > end_date
        temp = end_date
        end_date = start_date
        start_date = temp

    y1, m1, d1 = date_from_int(start_date)
    y2, m2, d2 = date_from_int(end_date)

    if basis == 0:  # US 30/360
        d2 = 30 if d2 == 31 and (d1 == 31 or d1 == 30) else min(d2, 31)
        d1 = 30 if d1 == 31 else d1

        count = 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
        result = count / 360

    elif basis == 1:  # Actual/actual
        result = actual_nb_days_AFB_alter((y1, m1, d1), (y2, m2, d2))

    elif basis == 2:  # Actual/360
        result = (end_date - start_date) / 360

    elif basis == 3:  # Actual/365
        result = (end_date - start_date) / 365

    elif basis == 4:  # Eurobond 30/360
        d2 = 30 if d2 == 31 else d2
        d1 = 30 if d1 == 31 else d1

        count = 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
        result = count / 360

    else:
        raise ValueError("%d must be 0, 1, 2, 3 or 4" % basis)

    return result

def isNa(value):
    # This function might need more solid testing

    try:
        eval(value)
        return False
    except:
        return True

def verschildekking(minvalue, rijvalue):
    lager = 0
    hoger = 0
    verschil = 0
    data = ""

    if rijvalue or minvalue is not None:
        if rijvalue < minvalue:
            lager += 1
            verschil = np.array(rijvalue) - np.array(minvalue)
        if rijvalue > minvalue:
            hoger += 1
    if lager == 0 and hoger == 0:
        data += "Vergelijkbaar"
    elif lager == 1 and hoger is None and verschil == -1:
        data += "Slechter1"
    elif lager > 1 and hoger is None:
        data += "Slechter"
    elif lager == 1 and hoger > 0:
        data += "Anders"
    elif lager == 0 and hoger > 0:
        data += "Beter"

    return data

def PositieMinimumAls(criteriumbereik, criterium, minimum, minimumbereik):
    minpositie = 0
    while criteriumbereik is not None:
        if criteriumbereik == criterium:
            if minimum or minimumbereik < minimum:
                minimum = minimumbereik
            minpositie = i
        i = i + 1
    return minpositie

def PositieBucketMinder(criteriumbereik, bucketbereik, prijsbereik):
    i = 1
    minpositie = 0

    while criteriumbereik(i) is not None:
        if criteriumbereik(i).value == "Anders1" or criteriumbereik(i).value == "Slechter1":
            if bucketbereik(i) - prijsbereik(i) < minimum:
                if minimum is not None or prijsbereik(i) < minimum:
                    minimum = prijsbereik(i)
                minpositie = i
                i = i + 1
    return minpositie

def PositieMinBucketIncVervang(huidigebuckets, vervangwaarde, vervangpositie, allebuckets, prijsrange):
    minpositie = 0
    minprijs = 9999
    looprij = 1
    eindrij = allebuckets
    aantalbuckets = huidigebuckets

    while looprij < eindrij:
        if allebuckets(looprij, vervangpositie).value == vervangwaarde:
            bucket = 1
            geldig = 1
            while bucket <= aantalbuckets:
                if bucket != vervangpositie:
                    if allebuckets(looprij, bucket).value < huidigebuckets(1, bucket).value:
                        geldig = 0
                        bucket = aantalbuckets
                    bucket = bucket + 1

                if geldig == 1 and prijsrange(looprij, 1).value < minprijs:
                    minprijs = prijsrange(looprij, 1).value
                    minpositie = looprij

                looprij = looprij + 1
        return minpositie

    if __name__ == '__main__':
        pass
