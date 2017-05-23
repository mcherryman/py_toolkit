from contextlib import contextmanager

"""Implements the python 3 suppress context manager, allowing for cleaner suppression of errors where no action is required."""

@contextmanager
def suppress(*args):
    for t in args: assert (issubclass(t, BaseException))
    try:yield
    except tuple(args): pass

def main():
    try:
        with suppress(IOError):
            with open('blahblah'):
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")
        print("WIN: Suppressed a single error")

        with suppress(IOError, KeyError):
            with open('blahblah'):
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")
            d = {}
            print(d['Bad key'])
            raise Exception("FAIL: Bad key exists....")
        print("WIN: Suppressed multiple errors")

        with suppress(IOError), suppress(KeyError):
            with open('blahblah'):
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")
            d = {}
            print(d['Bad key'])
            raise Exception("FAIL: Bad key exists....")
        print("WIN: Suppressed multiple errors with chained suppressions")

        with suppress(KeyError):
            with open('blahblah') as fout:
                raise Exception("FAIL: Somehow opened blahblah, why on earth does it exist!")
    except Exception as e:
        assert(isinstance(e, IOError))
        print("WIN: Caught an error that wasn't suppressed.")
        return

    raise Exception("FAIL: Oh no! Hang our heads in shame. This is a sad day.")

if __name__ == "__main__":
    # Super quick manual tests
    main()