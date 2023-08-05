# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-27 08:32:14
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-27 08:42:30

def timed_pipe(generator, seconds=3):
    ''' This is a time limited pipeline. If you have a infinite pipeline and
        want it to stop yielding after a certain amount of time, use this! '''
    # grab the highest precision timer
    from timeit import default_timer as ts
    # when it started
    start = ts()
    # when it will stop
    end = start + seconds
    # iterate over the pipeline
    for i in generator:
        # if there is still time
        if ts() < end:
            # yield the next item
            yield i
        # otherwise
        else:
            # stop
            break

if __name__ == '__main__':
    from generators import counter
    # this counts forever
    count = counter()
    # add a time limit
    count = timed_pipe(count, seconds=2)

    # run the pipeline for 2 seconds
    for i in count:
        print(i)
