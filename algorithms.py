import random


# =========================================================
# DATASET GENERATION
# =========================================================

def generate_array(size, minimum=10, maximum=100):
    """Generate a random array of integers."""
    return [random.randint(minimum, maximum) for _ in range(size)]


# =========================================================
# BUBBLE SORT
# =========================================================

def bubble_sort(array):
    """Bubble Sort with operation statistics."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(arr)):
        swapped = False

        for j in range(0, len(arr) - i - 1):
            comparisons += 1

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return arr, comparisons, swaps


def bubble_sort_steps(array):
    """
    Bubble Sort generator.

    Yields:
        array state
        comparison count
        swap count
        highlighted indices
    """
    arr = array.copy()
    comparisons = 0
    swaps = 0

    yield arr.copy(), comparisons, swaps, ()

    for i in range(len(arr)):
        swapped = False

        for j in range(0, len(arr) - i - 1):
            comparisons += 1

            yield arr.copy(), comparisons, swaps, (j, j + 1)

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

                yield arr.copy(), comparisons, swaps, (j, j + 1)

        if not swapped:
            break

    yield arr.copy(), comparisons, swaps, ()


# =========================================================
# SELECTION SORT
# =========================================================

def selection_sort(array):
    """Selection Sort with operation statistics."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(arr)):
        minimum_index = i

        for j in range(i + 1, len(arr)):
            comparisons += 1

            if arr[j] < arr[minimum_index]:
                minimum_index = j

        if minimum_index != i:
            arr[i], arr[minimum_index] = (
                arr[minimum_index],
                arr[i],
            )
            swaps += 1

    return arr, comparisons, swaps


def selection_sort_steps(array):
    """Selection Sort generator for visualization."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    yield arr.copy(), comparisons, swaps, ()

    for i in range(len(arr)):
        minimum_index = i

        for j in range(i + 1, len(arr)):
            comparisons += 1

            yield arr.copy(), comparisons, swaps, (
                minimum_index,
                j,
            )

            if arr[j] < arr[minimum_index]:
                minimum_index = j

        if minimum_index != i:
            arr[i], arr[minimum_index] = (
                arr[minimum_index],
                arr[i],
            )
            swaps += 1

            yield arr.copy(), comparisons, swaps, (
                i,
                minimum_index,
            )

    yield arr.copy(), comparisons, swaps, ()


# =========================================================
# INSERTION SORT
# =========================================================

def insertion_sort(array):
    """Insertion Sort with operation statistics."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break

        arr[j + 1] = key

    return arr, comparisons, swaps


def insertion_sort_steps(array):
    """Insertion Sort generator for visualization."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    yield arr.copy(), comparisons, swaps, ()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            yield arr.copy(), comparisons, swaps, (
                j,
                i,
            )

            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1

                yield arr.copy(), comparisons, swaps, (
                    j + 1,
                    i,
                )
            else:
                break

        arr[j + 1] = key

        yield arr.copy(), comparisons, swaps, (
            j + 1,
            i,
        )

    yield arr.copy(), comparisons, swaps, ()


# =========================================================
# MERGE SORT
# =========================================================

def merge_sort(array):
    """Merge Sort with operation statistics."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    def merge(left, right):
        nonlocal comparisons, swaps

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons += 1

            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        swaps += len(result)

        return result

    def sort(values):
        if len(values) <= 1:
            return values

        middle = len(values) // 2

        left = sort(values[:middle])
        right = sort(values[middle:])

        return merge(left, right)

    sorted_array = sort(arr)

    return sorted_array, comparisons, swaps


def merge_sort_steps(array):
    """Merge Sort generator for visualization."""
    arr = array.copy()
    comparisons = 0
    moves = 0

    def merge_sort_recursive(values, start):
        nonlocal comparisons, moves

        if len(values) <= 1:
            return values

        middle = len(values) // 2

        left = merge_sort_recursive(
            values[:middle],
            start,
        )

        right = merge_sort_recursive(
            values[middle:],
            start + middle,
        )

        merged = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons += 1

            yield (
                arr.copy(),
                comparisons,
                moves,
                (
                    start + i,
                    start + middle + j,
                ),
            )

            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        for index, value in enumerate(merged):
            arr[start + index] = value
            moves += 1

            yield (
                arr.copy(),
                comparisons,
                moves,
                (start + index,),
            )

        return merged

    generator = merge_sort_recursive(arr.copy(), 0)

    for state in generator:
        yield state

    yield arr.copy(), comparisons, moves, ()


# =========================================================
# QUICK SORT
# =========================================================

def quick_sort(array):
    """Quick Sort with operation statistics."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1

            if arr[j] <= pivot:
                i += 1

                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1

        if i + 1 != high:
            arr[i + 1], arr[high] = (
                arr[high],
                arr[i + 1],
            )
            swaps += 1

        return i + 1

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)

            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(arr) - 1)

    return arr, comparisons, swaps


def quick_sort_steps(array):
    """Quick Sort generator for visualization."""
    arr = array.copy()
    comparisons = 0
    swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1

            yield (
                arr.copy(),
                comparisons,
                swaps,
                (j, high),
            )

            if arr[j] <= pivot:
                i += 1

                if i != j:
                    arr[i], arr[j] = (
                        arr[j],
                        arr[i],
                    )
                    swaps += 1

                    yield (
                        arr.copy(),
                        comparisons,
                        swaps,
                        (i, j),
                    )

        if i + 1 != high:
            arr[i + 1], arr[high] = (
                arr[high],
                arr[i + 1],
            )
            swaps += 1

            yield (
                arr.copy(),
                comparisons,
                swaps,
                (i + 1, high),
            )

        return i + 1

    def sort(low, high):
        if low < high:
            pivot_generator = partition(low, high)

            pivot_index = None

            for state in pivot_generator:
                yield state

            # The generator's return value is not directly
            # accessible through a normal for-loop, so
            # calculate the partition boundary again.
            pivot = arr[high]
            i = low - 1

            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1

            pivot_index = i + 1

            yield from sort(low, pivot_index - 1)
            yield from sort(pivot_index + 1, high)

    # A simpler recursive implementation specifically
    # for reliable visualization.
    def visual_sort(low, high):
        nonlocal comparisons, swaps

        if low >= high:
            return

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            comparisons += 1

            yield (
                arr.copy(),
                comparisons,
                swaps,
                (j, high),
            )

            if arr[j] <= pivot:
                i += 1

                if i != j:
                    arr[i], arr[j] = (
                        arr[j],
                        arr[i],
                    )
                    swaps += 1

                    yield (
                        arr.copy(),
                        comparisons,
                        swaps,
                        (i, j),
                    )

        if i + 1 != high:
            arr[i + 1], arr[high] = (
                arr[high],
                arr[i + 1],
            )
            swaps += 1

            yield (
                arr.copy(),
                comparisons,
                swaps,
                (i + 1, high),
            )

        pivot_index = i + 1

        yield from visual_sort(
            low,
            pivot_index - 1,
        )

        yield from visual_sort(
            pivot_index + 1,
            high,
        )

    yield arr.copy(), comparisons, swaps, ()

    yield from visual_sort(
        0,
        len(arr) - 1,
    )

    yield arr.copy(), comparisons, swaps, ()


# =========================================================
# ALGORITHM REGISTRIES
# =========================================================

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}


STEP_ALGORITHMS = {
    "Bubble Sort": bubble_sort_steps,
    "Selection Sort": selection_sort_steps,
    "Insertion Sort": insertion_sort_steps,
    "Merge Sort": merge_sort_steps,
    "Quick Sort": quick_sort_steps,
}


# =========================================================
# RUN STANDARD ALGORITHM
# =========================================================

def run_algorithm(name, array):
    """Run a selected algorithm and return final statistics."""
    if name not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {name}")

    return ALGORITHMS[name](array)


# =========================================================
# RUN VISUALIZATION ALGORITHM
# =========================================================

def get_algorithm_steps(name, array):
    """Return the step generator for a selected algorithm."""
    if name not in STEP_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {name}")

    return STEP_ALGORITHMS[name](array)