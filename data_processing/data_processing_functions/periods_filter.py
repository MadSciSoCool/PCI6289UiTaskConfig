def intersect(tup1, tup2):
    low1, high1 = tup1
    low2, high2 = tup2
    if low1 >= high2 or low2 >= high1:
        return None
    else:
        return max(low1, low2), min(high1, high2)


def intersect_reduce(tups1, tups2):
    reduced_tups = []
    for tup1 in tups1:
        for tup2 in tups2:
            intersection = intersect(tup1, tup2)
            if intersection is not None:
                reduced_tups.append(intersection)
    return reduced_tups


def periods_filter(selected_periods, threshold):
    return_periods = selected_periods[0].copy()
    for i in range(1, len(selected_periods)):
        return_periods = intersect_reduce(return_periods, selected_periods[i])
    if len(return_periods) > 0:
        threshold = max([x[1] - x[0] for x in return_periods]) * threshold
        return_periods = list(filter(lambda x: x[1] - x[0] > threshold, return_periods))
    return return_periods
