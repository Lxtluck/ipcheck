# !/usr/bin/env python
# *-* coding:utf-8 *-*

def list_slice(l, n):
    for i in xrange(0, len(l), n):
        yield l[i: i+n]

def div_list(l, n):
    length = len(l)
    quo = length // n
    rem = length % n
    return map(lambda i: l[i*(quo + 1):i*(quo + 1) + (quo + 1)]\
        if i < rem else l[i*quo + rem: i*quo + rem +quo], range(n))



