def to_timestamp(date):
    """
    Convert date from input format to timestamp
    """
    try:
        return time.mktime(datetime.datetime.strptime(date, "%d%m%Y%H%M").timetuple())
    except:
        try:
            return time.mktime(datetime.datetime.strptime(date, "%d%m%Y").timetuple())
        except:
            return 0
    
