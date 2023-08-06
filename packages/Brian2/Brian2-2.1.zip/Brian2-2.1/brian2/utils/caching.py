'''
Module to support caching of function results to memory (used to cache results
of parsing, generation of state update code, etc.). Provides the `cached`
decorator.
'''

import functools
import collections


class CacheKey(object):
    '''
    Mixin class for objects that will be used as keys for caching (e.g.
    `Variable` objects) and have to define a certain "identity" with respect
    to caching. This "identity" is different from standard Python hashing and
    equality checking: a `Variable` for example would be considered "identical"
    for caching purposes regardless which object (e.g. `NeuronGroup`) it belongs
    to (because this does not matter for parsing, creating abstract code, etc.)
    but this of course matters for the values it refers to and therefore for
    comparison of equality to other variables.

    Classes that mix in the `CacheKey` class should re-define the
    ``_cache_irrelevant_attributes`` attribute to note all the attributes that
    should be ignored. The property ``_state_tuple`` will refer to a tuple of
    all attributes that were not excluded in such a way; this tuple will be used
    as the key for caching purposes.
    '''
    #: Set of attributes that should not be considered for caching of state
    #: update code, etc.
    _cache_irrelevant_attributes = set()

    @property
    def _state_tuple(self):
        '''A tuple with this object's attribute values, defining its identity
        for caching purposes. See `CacheKey` for details.'''
        return tuple(value for key, value in sorted(self.__dict__.iteritems())
                     if key not in self._cache_irrelevant_attributes)


class _CacheStatistics(object):
    '''
    Helper class to store cache statistics
    '''
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def __repr__(self):
        return '<Cache statistics: %d hits, %d misses>' % (self.hits, self.misses)


def cached(func):
    '''
    Decorator to cache a function so that it will not be re-evaluated when
    called with the same arguments. Uses the `_hashable` function to make
    arguments usable as a dictionary key even though they mutable (lists,
    dictionaries, etc.).

    Notes
    -----
    This is *not* a general-purpose caching decorator in any way comparable to
    ``functools.lru_cache`` or joblib's caching functions. It is very simplistic
    (no maximum cache size, no normalization of calls, e.g. ``foo(3)`` and
    ``foo(x=3)`` are not considered equivalent function calls) and makes very
    specific assumptions for our use case. Most importantly, `Variable` objects
    are considered to be identical when they refer to the same object, even
    though the actually stored values might have changed.

    Parameters
    ----------
    func : function
        The function to decorate.

    Returns
    -------
    decorated : function
        The decorated function.
    '''
    # For simplicity, we store the cache in the function itself
    func._cache = {}
    func._cache_statistics = _CacheStatistics()

    @functools.wraps(func)
    def cached_func(*args, **kwds):
        cache_key = tuple([_hashable(arg) for arg in args] +
                          [(key, _hashable(value))
                           for key, value in sorted(kwds.iteritems())])
        if cache_key in func._cache:
            func._cache_statistics.hits += 1
        else:
            func._cache_statistics.misses += 1
            func._cache[cache_key] = func(*args, **kwds)
        return func._cache[cache_key]

    return cached_func


def _hashable(obj):
    '''Helper function to make a few data structures hashable (e.g. a
    dictionary gets converted to a frozenset). The function is specifically
    tailored to our use case and not meant to be generally useful.'''
    if hasattr(obj, '_state_tuple'):
        return _hashable(obj._state_tuple)

    try:
        # If the object is already hashable, do nothing
        hash(obj)
        return obj
    except TypeError:
        pass

    if isinstance(obj, set):
        return frozenset(_hashable(el) for el in obj)
    elif isinstance(obj, collections.Sequence):
        return tuple(_hashable(el) for el in obj)
    elif isinstance(obj, collections.Mapping):
        return frozenset((_hashable(key), _hashable(value))
                         for key, value in obj.iteritems())
    else:
        raise AssertionError('Do not know how to handle object of type '
                             '%s' % type(obj))
