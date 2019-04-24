def periods_filter(selected_periods, threshold, cut_option):
    length = [[period[1] - period[0] for period in channel] for channel in selected_periods]
