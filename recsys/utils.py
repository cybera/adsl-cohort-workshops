def topn_from_dict(dic, n=10):
    """
    Returns the top-[n] highest valued items from [dic]
    """
    return sorted(dic.items(), key=lambda kv: kv[1])[::-1][:n]