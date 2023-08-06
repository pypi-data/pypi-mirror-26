import time
from collections import namedtuple
from arkdbtools import dbtools

def api_call(func, *args, **kwargs):
    result = None
    for i in range(15):
        if len(args):
            if kwargs:
                result = func(*args, **kwargs)
            else:
                result = func(*args)
        else:
            if kwargs:
                result = func(**kwargs)
            else:
                result = func()
        if result and 'success' in result and result['success']:
            return result
        time.sleep(5)
    return result


def api_call_cached(func, *args, **kwargs):
    if not hasattr(api_call_cached, 'cache'):
        api_call_cached.cache = {}
    cache_key = '%s/%s/%s' % (str(func), str(args), str(kwargs))
    if cache_key not in api_call_cached.cache:
        api_call_cached.cache[cache_key] = api_call(func, *args, **kwargs)
    return api_call_cached.cache[cache_key]


def timestamp(t = None, forfilename=False):
    """Returns a human-readable timestamp given a Unix timestamp 't' or
    for the current time. The Unix timestamp is the number of seconds since
    start of epoch (1970-01-01 00:00:00).

    When forfilename is True, then spaces and semicolons are replace with
    hyphens. The returned string is usable as a (part of a) filename. """

    datetimesep = ' '
    timesep     = ':'
    if forfilename:
        datetimesep = '-'
        timesep     = '-'

    return time.strftime('%Y-%m-%d' + datetimesep +
                         '%H' + timesep + '%M' + timesep + '%S',
                         time.localtime(t))


def arktimestamp(arkt, forfilename=False):
    """Returns a human-readable timestamp given an Ark timestamp 'arct'.
    An Ark timestamp is the number of seconds since Genesis block,
    2017:03:21 15:55:44."""

    t = arkt + time.mktime((2017, 3, 21, 15, 55, 44, 0, 0, 0))
    return '%d %s' % (arkt, timestamp(t))


def get_transactionlist(delegate_pubkey):
    """returns a list of named tuples of all transactions relevant to a specific delegates voters.
    Flow: finds all voters and unvoters, SELECTs all transactions of those voters, names all transactions according to
    the scheme: 'transaction', 'id amount timestamp recipientId senderId rawasset type fee blockId'"""
    cursor = dbtools.DbCursor()

    res = cursor.execute_and_fetchall("""
        SELECT transactions."id", transactions."amount",
               transactions."timestamp", transactions."recipientId",
               transactions."senderId", transactions."rawasset",
               transactions."type", transactions."fee", transactions."blockId"
        FROM transactions
        WHERE transactions."senderId" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{0}')
        OR transactions."recipientId" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{0}')
        ORDER BY transactions."timestamp" ASC;""".format(delegate_pubkey))

    Transaction = namedtuple(
        'transaction',
        'id amount timestamp recipientId senderId rawasset type fee')
    named_transactions = []

    for i in res:
        tx_id = Transaction(
            id=i[0],
            amount=i[1],
            timestamp=i[2],
            recipientId=i[3],
            senderId=i[4],
            rawasset=i[5],
            type=i[6],
            fee=i[7],
                            )

        named_transactions.append(tx_id)
    return named_transactions

