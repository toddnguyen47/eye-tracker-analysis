def progress_bar(current, total, elapsed_time, char_to_use="#"):
    """
    Return a string that details the current progress using hashtags.
    """
    import math
    max_hashtag = 30
    num_hashtags = math.floor(current / total * max_hashtag)
    s = ""
    for i in range(num_hashtags):
        s = "".join((s, char_to_use))
    for i in range(max_hashtag - num_hashtags):
        s = "".join((s, " "))

    return_string = "[{}] {:.2%}, {:.2f} seconds collapsed".format(s, current / total, elapsed_time)
    return return_string
