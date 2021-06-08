import math
import sys

# Auxilery functions, including error checks, round and jaccard calculation

def CHECK_DIV_ZERO(val,source):
    if val == 0:
        sys.exit("FATAL: Devision by zero during " + source + ".")

def jaccard(clusters1, clusters2):
    union_len = len(clusters1.union(clusters2))
    CHECK_DIV_ZERO(union_len,"calculation of Jaccard distance.")
    return len(clusters1.intersection(clusters2))/union_len
    
def round_sig(number, significant_digits):
    return round(number, significant_digits - int(math.floor(math.log10(abs(number)))) - 1)