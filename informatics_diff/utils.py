import contextlib


@contextlib.contextmanager
def print_done(*args, **kwargs):
    kwargs['end'] = '... '
    print(*args, **kwargs)
    yield
    print('done')
