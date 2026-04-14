import time
import random
import statistics
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", nargs="+", type=int, default=[3, 4, 5])
parser.add_argument("-s", nargs="+", type=int, default=[100, 500, 1000, 3000, 5000, 10000])
parser.add_argument("-e", type=int, default=1)
parser.add_argument("-r", type=int, default=10)
args = parser.parse_args()

algorithms = args.a
sizes_of_arrays = args.s
experiment_type = args.e
repetitions = args.r

""" ______________________________PART A -  Algorithm Implementation ___________________________"""
# --------------------------------insertion_sort (ID = 3)--------------------------------------------------
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:         # Insert arr[i] into the sorted subarray arr[0: i]
            arr[j+1] = arr[j]
            j = j - 1
        arr[j+1] = key
    return arr


# --------------------------------merge_sort (ID = 4)------------------------------------------------------
def last_merge(right, left):
    i, j = 0, 0
    result = []
    while i < len(right) and j < len(left):
        if right[i] <= left[j]:
            result.append(right[i])
            i += 1
        else:
            result.append(left[j])
            j += 1
    result.extend(left[j:])
    result.extend(right[i:])
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    right = merge_sort(arr[mid:])
    left = merge_sort(arr[:mid])

    return last_merge(right, left)


# -------------------------------------quick_sort (ID = 5)--------------------------------------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less, equal, greater = [], [], []
    for i in range(len(arr)):
        if arr[i] < pivot:
            less.append(arr[i])
        elif arr[i] == pivot:
            equal.append(arr[i])
        else:
            greater.append(arr[i])
    return quick_sort(less) + equal + quick_sort(greater)


"""   PART B - Comparative Experiment (Random Arrays)   +   PART C - Experiment with Noise or Partial Order"""


def list_maker(n):
    i = 0
    list_n = []
    while i < n:
        list_n.append(random.randint(0, 1000000))
        i += 1
    return list_n


def array_with_noise(arr, noise_level):
    sorted_arr = sorted(arr.copy())
    swaps = int(len(sorted_arr) * noise_level)
    for i in range(swaps):
        rand_index1 = random.randint(0, len(sorted_arr) - 1)
        rand_index2 = random.randint(0, len(sorted_arr) - 1)
        buffer = sorted_arr[rand_index1]
        sorted_arr[rand_index1] = sorted_arr[rand_index2]
        sorted_arr[rand_index2] = buffer
    arr_noisy = sorted_arr
    return arr_noisy


# sizes_of_arrays = [100, 500, 1000, 3000, 5000, 20000]
lst_avg_i, lst_avg_m, lst_avg_q = [], [], []        # part B
lst_dev_i, lst_dev_m, lst_dev_q = [], [], []

noise_avg_i, noise_avg_m, noise_avg_q = [], [], []  # part C
noise_dev_i, noise_dev_m, noise_dev_q = [], [], []

if experiment_type == 1:     # IF for noise level base on the terminal = 0.05 or 0.2
    noise_level = 0.05
elif experiment_type == 2:
    noise_level = 0.2
else:
    noise_level = 0.05

# -------------------------------MAIN CODE-----------------------------------------------------
for size in sizes_of_arrays:
    times_i, times_m, times_q = [], [], []       # part B
    times_in, times_mn, times_qn = [], [], []    # part C
    for r in range(repetitions):                     # 10 repeats for each size
        list_unsorted = list_maker(size)
        arr_noisy = array_with_noise(list_unsorted, noise_level)

        # -----------------------------------part B
        arr1 = list_unsorted.copy()      # insertion_sort
        start = time.perf_counter()
        insertion_sort(arr1)
        end = time.perf_counter()
        insertion_time = end - start
        times_i.append(insertion_time)

        arr2 = list_unsorted.copy()      # merge_sort
        start = time.perf_counter()
        merge_sort(arr2)
        end = time.perf_counter()
        merge_time = end - start
        times_m.append(merge_time)

        arr3 = list_unsorted.copy()      # quick_sort
        start = time.perf_counter()
        quick_sort(arr3)
        end = time.perf_counter()
        quick_time = end - start
        times_q.append(quick_time)

        # -----------------------------------part C
        arr1n = arr_noisy.copy()  # insertion_sort
        start = time.perf_counter()
        insertion_sort(arr1n)
        end = time.perf_counter()
        insertion_time = end - start
        times_in.append(insertion_time)

        arr2n = arr_noisy.copy()  # merge_sort
        start = time.perf_counter()
        merge_sort(arr2n)
        end = time.perf_counter()
        merge_time = end - start
        times_mn.append(merge_time)

        arr3n = arr_noisy.copy()  # quick_sort
        start = time.perf_counter()
        quick_sort(arr3n)
        end = time.perf_counter()
        quick_time = end - start
        times_qn.append(quick_time)
    lst_avg_i.append(statistics.mean(times_i))     # part B
    lst_avg_m.append(statistics.mean(times_m))
    lst_avg_q.append(statistics.mean(times_q))
    lst_dev_i.append(statistics.stdev(times_i))
    lst_dev_m.append(statistics.stdev(times_m))
    lst_dev_q.append(statistics.stdev(times_q))

    noise_avg_i.append(statistics.mean(times_in))  # part C
    noise_avg_m.append(statistics.mean(times_mn))
    noise_avg_q.append(statistics.mean(times_qn))
    noise_dev_i.append(statistics.stdev(times_in))
    noise_dev_m.append(statistics.stdev(times_mn))
    noise_dev_q.append(statistics.stdev(times_qn))


# ------------------------------comparison plot part B
plt.figure(figsize=(10, 6))

plt.plot(sizes_of_arrays, lst_avg_i, marker='o', label='Insertion Sort')
plt.plot(sizes_of_arrays, lst_avg_m, marker='o', label='Merge Sort')
plt.plot(sizes_of_arrays, lst_avg_q, marker='o', label='Quick Sort')

plt.fill_between(sizes_of_arrays,
                [lst_avg_i[i] - lst_dev_i[i] for i in range(len(lst_avg_i))],
                [lst_avg_i[i] + lst_dev_i[i] for i in range(len(lst_avg_i))],
                alpha=0.2)

plt.fill_between(sizes_of_arrays,
                [lst_avg_m[i] - lst_dev_m[i] for i in range(len(lst_avg_m))],
                [lst_avg_m[i] + lst_dev_m[i] for i in range(len(lst_avg_m))],
                alpha=0.2)

plt.fill_between(sizes_of_arrays,
                [lst_avg_q[i] - lst_dev_q[i] for i in range(len(lst_avg_q))],
                [lst_avg_q[i] + lst_dev_q[i] for i in range(len(lst_avg_q))],
                alpha=0.2)

plt.title("Runtime Comparison (unsorted)")
plt.xlabel("Array size (n)")
plt.ylabel("Runtime (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)

plt.savefig("result1.png")


# ------------------------------comparison plot part C
plt.figure(figsize=(10, 6))

plt.plot(sizes_of_arrays, noise_avg_i, marker='o', label='Insertion Sort')
plt.plot(sizes_of_arrays, noise_avg_m, marker='o', label='Merge Sort')
plt.plot(sizes_of_arrays, noise_avg_q, marker='o', label='Quick Sort')

plt.fill_between(sizes_of_arrays,
                [noise_avg_i[i] - noise_dev_i[i] for i in range(len(noise_avg_i))],
                [noise_avg_i[i] + noise_dev_i[i] for i in range(len(noise_avg_i))],
                alpha=0.2)

plt.fill_between(sizes_of_arrays,
                [noise_avg_m[i] - noise_dev_m[i] for i in range(len(noise_avg_m))],
                [noise_avg_m[i] + noise_dev_m[i] for i in range(len(noise_avg_m))],
                alpha=0.2)

plt.fill_between(sizes_of_arrays,
                [noise_avg_q[i] - noise_dev_q[i] for i in range(len(noise_avg_q))],
                [noise_avg_q[i] + noise_dev_q[i] for i in range(len(noise_avg_q))],
                alpha=0.2)

plt.title(f"Runtime Comparison (Nearly Sorted, noise={int(noise_level*100)}%)")
plt.xlabel("Array size (n)")
plt.ylabel("Runtime (seconds)")
plt.legend()
plt.grid(True, alpha=0.3)

plt.savefig("result2.png")
plt.show()

