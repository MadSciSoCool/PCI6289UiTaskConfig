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


def periods_filter(selected_periods, threshold, cut_option):
    # first step: calculate the length of each tuple
    length = [[period[1] - period[0] for period in channel] for channel in selected_periods]
    if cut_option == "total":
        total_length = [sum(channel) for channel in length]
        desired_length = min(total_length)
        for channel in selected_periods:
            rest_length = desired_length
            for i in len(channel):
                period = channel[i]
                period_length = period[1] - period[0]
                if period_length >= rest_length > 0:
                    channel[i] = (period[0], period[0] + rest_length)
                    del(channel[i+1:])
                    break
        return selected_periods
    elif cut_option == "each":
        if len(selected_periods) == 1:
            return selected_periods
        elif len(selected_periods) > 1:
            max_length = max([max(channel) for channel in length])
            threshold = threshold * max_length
            filtered_periods = [filter(lambda x: x>threshold, channel) for channel in selected_periods]
            return_periods = filtered_periods[0]
            for i in range(1, len(filtered_periods)):
                return_periods = intersect_reduce(return_periods, filtered_periods[i])
            return return_periods
    else:
        raise Exception("Not a valid cut option")
