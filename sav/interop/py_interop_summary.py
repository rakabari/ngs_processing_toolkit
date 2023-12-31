# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _py_interop_summary
else:
    import _py_interop_summary

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _py_interop_summary.delete_SwigPyIterator

    def value(self):
        return _py_interop_summary.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _py_interop_summary.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _py_interop_summary.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _py_interop_summary.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _py_interop_summary.SwigPyIterator_equal(self, x)

    def copy(self):
        return _py_interop_summary.SwigPyIterator_copy(self)

    def next(self):
        return _py_interop_summary.SwigPyIterator_next(self)

    def __next__(self):
        return _py_interop_summary.SwigPyIterator___next__(self)

    def previous(self):
        return _py_interop_summary.SwigPyIterator_previous(self)

    def advance(self, n):
        return _py_interop_summary.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _py_interop_summary.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _py_interop_summary.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _py_interop_summary.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _py_interop_summary.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _py_interop_summary.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _py_interop_summary.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _py_interop_summary:
_py_interop_summary.SwigPyIterator_swigregister(SwigPyIterator)

import interop.py_interop_run
import interop.py_interop_metrics
import interop.py_interop_run_metrics
import interop.py_interop_comm
class cycle_state_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _py_interop_summary.cycle_state_summary_swiginit(self, _py_interop_summary.new_cycle_state_summary())

    def empty(self):
        return _py_interop_summary.cycle_state_summary_empty(self)

    def extracted_cycle_range(self, *args):
        return _py_interop_summary.cycle_state_summary_extracted_cycle_range(self, *args)

    def called_cycle_range(self, *args):
        return _py_interop_summary.cycle_state_summary_called_cycle_range(self, *args)

    def qscored_cycle_range(self, *args):
        return _py_interop_summary.cycle_state_summary_qscored_cycle_range(self, *args)

    def error_cycle_range(self, *args):
        return _py_interop_summary.cycle_state_summary_error_cycle_range(self, *args)
    __swig_destroy__ = _py_interop_summary.delete_cycle_state_summary

# Register cycle_state_summary in _py_interop_summary:
_py_interop_summary.cycle_state_summary_swigregister(cycle_state_summary)

class stat_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, arg2):
        _py_interop_summary.stat_summary_swiginit(self, _py_interop_summary.new_stat_summary(arg2))

    def percent_gt_q30(self, *args):
        return _py_interop_summary.stat_summary_percent_gt_q30(self, *args)

    def yield_g(self, *args):
        return _py_interop_summary.stat_summary_yield_g(self, *args)

    def projected_yield_g(self, *args):
        return _py_interop_summary.stat_summary_projected_yield_g(self, *args)

    def reads(self, *args):
        return _py_interop_summary.stat_summary_reads(self, *args)

    def reads_pf(self, *args):
        return _py_interop_summary.stat_summary_reads_pf(self, *args)

    def density(self, *args):
        return _py_interop_summary.stat_summary_density(self, *args)

    def density_pf(self, *args):
        return _py_interop_summary.stat_summary_density_pf(self, *args)

    def cluster_count(self, *args):
        return _py_interop_summary.stat_summary_cluster_count(self, *args)

    def cluster_count_pf(self, *args):
        return _py_interop_summary.stat_summary_cluster_count_pf(self, *args)

    def percent_pf(self, *args):
        return _py_interop_summary.stat_summary_percent_pf(self, *args)

    def phasing(self, *args):
        return _py_interop_summary.stat_summary_phasing(self, *args)

    def prephasing(self, *args):
        return _py_interop_summary.stat_summary_prephasing(self, *args)

    def percent_aligned(self, *args):
        return _py_interop_summary.stat_summary_percent_aligned(self, *args)

    def error_rate(self, *args):
        return _py_interop_summary.stat_summary_error_rate(self, *args)

    def error_rate_35(self, *args):
        return _py_interop_summary.stat_summary_error_rate_35(self, *args)

    def error_rate_50(self, *args):
        return _py_interop_summary.stat_summary_error_rate_50(self, *args)

    def error_rate_75(self, *args):
        return _py_interop_summary.stat_summary_error_rate_75(self, *args)

    def error_rate_100(self, *args):
        return _py_interop_summary.stat_summary_error_rate_100(self, *args)

    def first_cycle_intensity(self, *args):
        return _py_interop_summary.stat_summary_first_cycle_intensity(self, *args)

    def phasing_slope(self, *args):
        return _py_interop_summary.stat_summary_phasing_slope(self, *args)

    def phasing_offset(self, *args):
        return _py_interop_summary.stat_summary_phasing_offset(self, *args)

    def prephasing_slope(self, *args):
        return _py_interop_summary.stat_summary_prephasing_slope(self, *args)

    def prephasing_offset(self, *args):
        return _py_interop_summary.stat_summary_prephasing_offset(self, *args)

    def percent_occupied(self, *args):
        return _py_interop_summary.stat_summary_percent_occupied(self, *args)

    def resize_stat(self, arg2):
        return _py_interop_summary.stat_summary_resize_stat(self, arg2)
    __swig_destroy__ = _py_interop_summary.delete_stat_summary

# Register stat_summary in _py_interop_summary:
_py_interop_summary.stat_summary_swigregister(stat_summary)

class surface_summary(stat_summary):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, surface=0, channel_count=0):
        _py_interop_summary.surface_summary_swiginit(self, _py_interop_summary.new_surface_summary(surface, channel_count))

    def surface(self, *args):
        return _py_interop_summary.surface_summary_surface(self, *args)

    def tile_count(self, *args):
        return _py_interop_summary.surface_summary_tile_count(self, *args)
    __swig_destroy__ = _py_interop_summary.delete_surface_summary

# Register surface_summary in _py_interop_summary:
_py_interop_summary.surface_summary_swigregister(surface_summary)

class metric_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, arg2):
        _py_interop_summary.metric_summary_swiginit(self, _py_interop_summary.new_metric_summary(arg2))

    def first_cycle_intensity(self, *args):
        return _py_interop_summary.metric_summary_first_cycle_intensity(self, *args)

    def error_rate(self, *args):
        return _py_interop_summary.metric_summary_error_rate(self, *args)

    def percent_aligned(self, *args):
        return _py_interop_summary.metric_summary_percent_aligned(self, *args)

    def percent_gt_q30(self, *args):
        return _py_interop_summary.metric_summary_percent_gt_q30(self, *args)

    def yield_g(self, *args):
        return _py_interop_summary.metric_summary_yield_g(self, *args)

    def projected_yield_g(self, *args):
        return _py_interop_summary.metric_summary_projected_yield_g(self, *args)

    def percent_occupied(self, *args):
        return _py_interop_summary.metric_summary_percent_occupied(self, *args)

    def percent_occupancy_proxy(self, *args):
        return _py_interop_summary.metric_summary_percent_occupancy_proxy(self, *args)

    def resize(self, arg2):
        return _py_interop_summary.metric_summary_resize(self, arg2)
    __swig_destroy__ = _py_interop_summary.delete_metric_summary

# Register metric_summary in _py_interop_summary:
_py_interop_summary.metric_summary_swigregister(metric_summary)

class lane_summary(stat_summary):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, lane=0, channel_count=0):
        _py_interop_summary.lane_summary_swiginit(self, _py_interop_summary.new_lane_summary(lane, channel_count))

    def at(self, n):
        return _py_interop_summary.lane_summary_at(self, n)

    def resize(self, n):
        return _py_interop_summary.lane_summary_resize(self, n)

    def cycle_state(self):
        return _py_interop_summary.lane_summary_cycle_state(self)

    def lane(self, *args):
        return _py_interop_summary.lane_summary_lane(self, *args)

    def tile_count(self, *args):
        return _py_interop_summary.lane_summary_tile_count(self, *args)

    def size(self):
        return _py_interop_summary.lane_summary_size(self)
    __swig_destroy__ = _py_interop_summary.delete_lane_summary

# Register lane_summary in _py_interop_summary:
_py_interop_summary.lane_summary_swigregister(lane_summary)

class metric_stat(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _py_interop_summary.metric_stat_swiginit(self, _py_interop_summary.new_metric_stat(*args))

    def clear(self):
        return _py_interop_summary.metric_stat_clear(self)

    def mean(self, *args):
        return _py_interop_summary.metric_stat_mean(self, *args)

    def stddev(self, *args):
        return _py_interop_summary.metric_stat_stddev(self, *args)

    def median(self, *args):
        return _py_interop_summary.metric_stat_median(self, *args)
    __swig_destroy__ = _py_interop_summary.delete_metric_stat

# Register metric_stat in _py_interop_summary:
_py_interop_summary.metric_stat_swigregister(metric_stat)

class read_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _py_interop_summary.read_summary_swiginit(self, _py_interop_summary.new_read_summary(*args))

    def at(self, n):
        return _py_interop_summary.read_summary_at(self, n)

    def resize(self, n):
        return _py_interop_summary.read_summary_resize(self, n)

    def read(self):
        return _py_interop_summary.read_summary_read(self)

    def summary(self, *args):
        return _py_interop_summary.read_summary_summary(self, *args)

    def size(self):
        return _py_interop_summary.read_summary_size(self)

    def lane_count(self):
        return _py_interop_summary.read_summary_lane_count(self)
    __swig_destroy__ = _py_interop_summary.delete_read_summary

# Register read_summary in _py_interop_summary:
_py_interop_summary.read_summary_swigregister(read_summary)

class run_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _py_interop_summary.run_summary_swiginit(self, _py_interop_summary.new_run_summary(*args))

    def initialize(self, *args):
        return _py_interop_summary.run_summary_initialize(self, *args)

    def copy_reads(self, dst):
        return _py_interop_summary.run_summary_copy_reads(self, dst)

    def at(self, n):
        return _py_interop_summary.run_summary_at(self, n)

    def size(self):
        return _py_interop_summary.run_summary_size(self)

    def lane_count(self, *args):
        return _py_interop_summary.run_summary_lane_count(self, *args)

    def channel_count(self):
        return _py_interop_summary.run_summary_channel_count(self)

    def surface_count(self, *args):
        return _py_interop_summary.run_summary_surface_count(self, *args)

    def total_summary(self, *args):
        return _py_interop_summary.run_summary_total_summary(self, *args)

    def nonindex_summary(self, *args):
        return _py_interop_summary.run_summary_nonindex_summary(self, *args)

    def cycle_state(self):
        return _py_interop_summary.run_summary_cycle_state(self)

    def clear(self):
        return _py_interop_summary.run_summary_clear(self)
    __swig_destroy__ = _py_interop_summary.delete_run_summary

# Register run_summary in _py_interop_summary:
_py_interop_summary.run_summary_swigregister(run_summary)

class surface_summary_vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _py_interop_summary.surface_summary_vector___nonzero__(self)

    def __bool__(self):
        return _py_interop_summary.surface_summary_vector___bool__(self)

    def __len__(self):
        return _py_interop_summary.surface_summary_vector___len__(self)

    def __getslice__(self, i, j):
        return _py_interop_summary.surface_summary_vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _py_interop_summary.surface_summary_vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _py_interop_summary.surface_summary_vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _py_interop_summary.surface_summary_vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _py_interop_summary.surface_summary_vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _py_interop_summary.surface_summary_vector___setitem__(self, *args)

    def pop(self):
        return _py_interop_summary.surface_summary_vector_pop(self)

    def append(self, x):
        return _py_interop_summary.surface_summary_vector_append(self, x)

    def empty(self):
        return _py_interop_summary.surface_summary_vector_empty(self)

    def size(self):
        return _py_interop_summary.surface_summary_vector_size(self)

    def swap(self, v):
        return _py_interop_summary.surface_summary_vector_swap(self, v)

    def rbegin(self):
        return _py_interop_summary.surface_summary_vector_rbegin(self)

    def rend(self):
        return _py_interop_summary.surface_summary_vector_rend(self)

    def clear(self):
        return _py_interop_summary.surface_summary_vector_clear(self)

    def get_allocator(self):
        return _py_interop_summary.surface_summary_vector_get_allocator(self)

    def pop_back(self):
        return _py_interop_summary.surface_summary_vector_pop_back(self)

    def erase(self, *args):
        return _py_interop_summary.surface_summary_vector_erase(self, *args)

    def __init__(self, *args):
        _py_interop_summary.surface_summary_vector_swiginit(self, _py_interop_summary.new_surface_summary_vector(*args))

    def push_back(self, x):
        return _py_interop_summary.surface_summary_vector_push_back(self, x)

    def front(self):
        return _py_interop_summary.surface_summary_vector_front(self)

    def back(self):
        return _py_interop_summary.surface_summary_vector_back(self)

    def assign(self, n, x):
        return _py_interop_summary.surface_summary_vector_assign(self, n, x)

    def resize(self, *args):
        return _py_interop_summary.surface_summary_vector_resize(self, *args)

    def insert(self, *args):
        return _py_interop_summary.surface_summary_vector_insert(self, *args)

    def reserve(self, n):
        return _py_interop_summary.surface_summary_vector_reserve(self, n)

    def capacity(self):
        return _py_interop_summary.surface_summary_vector_capacity(self)
    __swig_destroy__ = _py_interop_summary.delete_surface_summary_vector

# Register surface_summary_vector in _py_interop_summary:
_py_interop_summary.surface_summary_vector_swigregister(surface_summary_vector)

class lane_summary_vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _py_interop_summary.lane_summary_vector___nonzero__(self)

    def __bool__(self):
        return _py_interop_summary.lane_summary_vector___bool__(self)

    def __len__(self):
        return _py_interop_summary.lane_summary_vector___len__(self)

    def __getslice__(self, i, j):
        return _py_interop_summary.lane_summary_vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _py_interop_summary.lane_summary_vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _py_interop_summary.lane_summary_vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _py_interop_summary.lane_summary_vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _py_interop_summary.lane_summary_vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _py_interop_summary.lane_summary_vector___setitem__(self, *args)

    def pop(self):
        return _py_interop_summary.lane_summary_vector_pop(self)

    def append(self, x):
        return _py_interop_summary.lane_summary_vector_append(self, x)

    def empty(self):
        return _py_interop_summary.lane_summary_vector_empty(self)

    def size(self):
        return _py_interop_summary.lane_summary_vector_size(self)

    def swap(self, v):
        return _py_interop_summary.lane_summary_vector_swap(self, v)

    def rbegin(self):
        return _py_interop_summary.lane_summary_vector_rbegin(self)

    def rend(self):
        return _py_interop_summary.lane_summary_vector_rend(self)

    def clear(self):
        return _py_interop_summary.lane_summary_vector_clear(self)

    def get_allocator(self):
        return _py_interop_summary.lane_summary_vector_get_allocator(self)

    def pop_back(self):
        return _py_interop_summary.lane_summary_vector_pop_back(self)

    def erase(self, *args):
        return _py_interop_summary.lane_summary_vector_erase(self, *args)

    def __init__(self, *args):
        _py_interop_summary.lane_summary_vector_swiginit(self, _py_interop_summary.new_lane_summary_vector(*args))

    def push_back(self, x):
        return _py_interop_summary.lane_summary_vector_push_back(self, x)

    def front(self):
        return _py_interop_summary.lane_summary_vector_front(self)

    def back(self):
        return _py_interop_summary.lane_summary_vector_back(self)

    def assign(self, n, x):
        return _py_interop_summary.lane_summary_vector_assign(self, n, x)

    def resize(self, *args):
        return _py_interop_summary.lane_summary_vector_resize(self, *args)

    def insert(self, *args):
        return _py_interop_summary.lane_summary_vector_insert(self, *args)

    def reserve(self, n):
        return _py_interop_summary.lane_summary_vector_reserve(self, n)

    def capacity(self):
        return _py_interop_summary.lane_summary_vector_capacity(self)
    __swig_destroy__ = _py_interop_summary.delete_lane_summary_vector

# Register lane_summary_vector in _py_interop_summary:
_py_interop_summary.lane_summary_vector_swigregister(lane_summary_vector)

class read_summary_vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _py_interop_summary.read_summary_vector___nonzero__(self)

    def __bool__(self):
        return _py_interop_summary.read_summary_vector___bool__(self)

    def __len__(self):
        return _py_interop_summary.read_summary_vector___len__(self)

    def __getslice__(self, i, j):
        return _py_interop_summary.read_summary_vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _py_interop_summary.read_summary_vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _py_interop_summary.read_summary_vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _py_interop_summary.read_summary_vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _py_interop_summary.read_summary_vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _py_interop_summary.read_summary_vector___setitem__(self, *args)

    def pop(self):
        return _py_interop_summary.read_summary_vector_pop(self)

    def append(self, x):
        return _py_interop_summary.read_summary_vector_append(self, x)

    def empty(self):
        return _py_interop_summary.read_summary_vector_empty(self)

    def size(self):
        return _py_interop_summary.read_summary_vector_size(self)

    def swap(self, v):
        return _py_interop_summary.read_summary_vector_swap(self, v)

    def rbegin(self):
        return _py_interop_summary.read_summary_vector_rbegin(self)

    def rend(self):
        return _py_interop_summary.read_summary_vector_rend(self)

    def clear(self):
        return _py_interop_summary.read_summary_vector_clear(self)

    def get_allocator(self):
        return _py_interop_summary.read_summary_vector_get_allocator(self)

    def pop_back(self):
        return _py_interop_summary.read_summary_vector_pop_back(self)

    def erase(self, *args):
        return _py_interop_summary.read_summary_vector_erase(self, *args)

    def __init__(self, *args):
        _py_interop_summary.read_summary_vector_swiginit(self, _py_interop_summary.new_read_summary_vector(*args))

    def push_back(self, x):
        return _py_interop_summary.read_summary_vector_push_back(self, x)

    def front(self):
        return _py_interop_summary.read_summary_vector_front(self)

    def back(self):
        return _py_interop_summary.read_summary_vector_back(self)

    def assign(self, n, x):
        return _py_interop_summary.read_summary_vector_assign(self, n, x)

    def resize(self, *args):
        return _py_interop_summary.read_summary_vector_resize(self, *args)

    def insert(self, *args):
        return _py_interop_summary.read_summary_vector_insert(self, *args)

    def reserve(self, n):
        return _py_interop_summary.read_summary_vector_reserve(self, n)

    def capacity(self):
        return _py_interop_summary.read_summary_vector_capacity(self)
    __swig_destroy__ = _py_interop_summary.delete_read_summary_vector

# Register read_summary_vector in _py_interop_summary:
_py_interop_summary.read_summary_vector_swigregister(read_summary_vector)


def summarize_run_metrics(metrics, summary, skip_median=False, trim=True):
    return _py_interop_summary.summarize_run_metrics(metrics, summary, skip_median, trim)
class index_count_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _py_interop_summary.index_count_summary_swiginit(self, _py_interop_summary.new_index_count_summary(*args))

    def index1(self):
        return _py_interop_summary.index_count_summary_index1(self)

    def index2(self):
        return _py_interop_summary.index_count_summary_index2(self)

    def fraction_mapped(self):
        return _py_interop_summary.index_count_summary_fraction_mapped(self)

    def cluster_count(self):
        return _py_interop_summary.index_count_summary_cluster_count(self)

    def sample_id(self):
        return _py_interop_summary.index_count_summary_sample_id(self)

    def project_name(self):
        return _py_interop_summary.index_count_summary_project_name(self)

    def id(self, *args):
        return _py_interop_summary.index_count_summary_id(self, *args)

    def add(self, cluster_count):
        return _py_interop_summary.index_count_summary_add(self, cluster_count)

    def update_fraction_mapped(self, total_pf_cluster_count):
        return _py_interop_summary.index_count_summary_update_fraction_mapped(self, total_pf_cluster_count)

    def __lt__(self, rhs):
        return _py_interop_summary.index_count_summary___lt__(self, rhs)
    __swig_destroy__ = _py_interop_summary.delete_index_count_summary

# Register index_count_summary in _py_interop_summary:
_py_interop_summary.index_count_summary_swigregister(index_count_summary)

class index_lane_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, total_reads=0, total_pf_reads=0, total_fraction_mapped_reads=0, mapped_reads_cv=0, min_mapped_reads=0, max_mapped_reads=0):
        _py_interop_summary.index_lane_summary_swiginit(self, _py_interop_summary.new_index_lane_summary(total_reads, total_pf_reads, total_fraction_mapped_reads, mapped_reads_cv, min_mapped_reads, max_mapped_reads))

    def resize(self, n):
        return _py_interop_summary.index_lane_summary_resize(self, n)

    def reserve(self, n):
        return _py_interop_summary.index_lane_summary_reserve(self, n)

    def push_back(self, count_summary):
        return _py_interop_summary.index_lane_summary_push_back(self, count_summary)

    def size(self):
        return _py_interop_summary.index_lane_summary_size(self)

    def at(self, n):
        return _py_interop_summary.index_lane_summary_at(self, n)

    def total_reads(self):
        return _py_interop_summary.index_lane_summary_total_reads(self)

    def total_pf_reads(self):
        return _py_interop_summary.index_lane_summary_total_pf_reads(self)

    def total_fraction_mapped_reads(self):
        return _py_interop_summary.index_lane_summary_total_fraction_mapped_reads(self)

    def mapped_reads_cv(self):
        return _py_interop_summary.index_lane_summary_mapped_reads_cv(self)

    def min_mapped_reads(self):
        return _py_interop_summary.index_lane_summary_min_mapped_reads(self)

    def max_mapped_reads(self):
        return _py_interop_summary.index_lane_summary_max_mapped_reads(self)

    def sort(self):
        return _py_interop_summary.index_lane_summary_sort(self)

    def set(self, total_mapped_reads, pf_cluster_count_total, cluster_count_total, min_fraction_mapped, max_fraction_mapped, cv_fraction_mapped):
        return _py_interop_summary.index_lane_summary_set(self, total_mapped_reads, pf_cluster_count_total, cluster_count_total, min_fraction_mapped, max_fraction_mapped, cv_fraction_mapped)

    def clear(self):
        return _py_interop_summary.index_lane_summary_clear(self)
    __swig_destroy__ = _py_interop_summary.delete_index_lane_summary

# Register index_lane_summary in _py_interop_summary:
_py_interop_summary.index_lane_summary_swigregister(index_lane_summary)

class index_flowcell_summary(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, n=0):
        _py_interop_summary.index_flowcell_summary_swiginit(self, _py_interop_summary.new_index_flowcell_summary(n))

    def at(self, n):
        return _py_interop_summary.index_flowcell_summary_at(self, n)

    def size(self):
        return _py_interop_summary.index_flowcell_summary_size(self)

    def resize(self, n):
        return _py_interop_summary.index_flowcell_summary_resize(self, n)

    def sort(self):
        return _py_interop_summary.index_flowcell_summary_sort(self)

    def clear(self):
        return _py_interop_summary.index_flowcell_summary_clear(self)
    __swig_destroy__ = _py_interop_summary.delete_index_flowcell_summary

# Register index_flowcell_summary in _py_interop_summary:
_py_interop_summary.index_flowcell_summary_swigregister(index_flowcell_summary)

class index_count_summary_vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _py_interop_summary.index_count_summary_vector___nonzero__(self)

    def __bool__(self):
        return _py_interop_summary.index_count_summary_vector___bool__(self)

    def __len__(self):
        return _py_interop_summary.index_count_summary_vector___len__(self)

    def __getslice__(self, i, j):
        return _py_interop_summary.index_count_summary_vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _py_interop_summary.index_count_summary_vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _py_interop_summary.index_count_summary_vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _py_interop_summary.index_count_summary_vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _py_interop_summary.index_count_summary_vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _py_interop_summary.index_count_summary_vector___setitem__(self, *args)

    def pop(self):
        return _py_interop_summary.index_count_summary_vector_pop(self)

    def append(self, x):
        return _py_interop_summary.index_count_summary_vector_append(self, x)

    def empty(self):
        return _py_interop_summary.index_count_summary_vector_empty(self)

    def size(self):
        return _py_interop_summary.index_count_summary_vector_size(self)

    def swap(self, v):
        return _py_interop_summary.index_count_summary_vector_swap(self, v)

    def rbegin(self):
        return _py_interop_summary.index_count_summary_vector_rbegin(self)

    def rend(self):
        return _py_interop_summary.index_count_summary_vector_rend(self)

    def clear(self):
        return _py_interop_summary.index_count_summary_vector_clear(self)

    def get_allocator(self):
        return _py_interop_summary.index_count_summary_vector_get_allocator(self)

    def pop_back(self):
        return _py_interop_summary.index_count_summary_vector_pop_back(self)

    def erase(self, *args):
        return _py_interop_summary.index_count_summary_vector_erase(self, *args)

    def __init__(self, *args):
        _py_interop_summary.index_count_summary_vector_swiginit(self, _py_interop_summary.new_index_count_summary_vector(*args))

    def push_back(self, x):
        return _py_interop_summary.index_count_summary_vector_push_back(self, x)

    def front(self):
        return _py_interop_summary.index_count_summary_vector_front(self)

    def back(self):
        return _py_interop_summary.index_count_summary_vector_back(self)

    def assign(self, n, x):
        return _py_interop_summary.index_count_summary_vector_assign(self, n, x)

    def resize(self, *args):
        return _py_interop_summary.index_count_summary_vector_resize(self, *args)

    def insert(self, *args):
        return _py_interop_summary.index_count_summary_vector_insert(self, *args)

    def reserve(self, n):
        return _py_interop_summary.index_count_summary_vector_reserve(self, n)

    def capacity(self):
        return _py_interop_summary.index_count_summary_vector_capacity(self)
    __swig_destroy__ = _py_interop_summary.delete_index_count_summary_vector

# Register index_count_summary_vector in _py_interop_summary:
_py_interop_summary.index_count_summary_vector_swigregister(index_count_summary_vector)

class index_lane_summary_vector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _py_interop_summary.index_lane_summary_vector___nonzero__(self)

    def __bool__(self):
        return _py_interop_summary.index_lane_summary_vector___bool__(self)

    def __len__(self):
        return _py_interop_summary.index_lane_summary_vector___len__(self)

    def __getslice__(self, i, j):
        return _py_interop_summary.index_lane_summary_vector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _py_interop_summary.index_lane_summary_vector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _py_interop_summary.index_lane_summary_vector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _py_interop_summary.index_lane_summary_vector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _py_interop_summary.index_lane_summary_vector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _py_interop_summary.index_lane_summary_vector___setitem__(self, *args)

    def pop(self):
        return _py_interop_summary.index_lane_summary_vector_pop(self)

    def append(self, x):
        return _py_interop_summary.index_lane_summary_vector_append(self, x)

    def empty(self):
        return _py_interop_summary.index_lane_summary_vector_empty(self)

    def size(self):
        return _py_interop_summary.index_lane_summary_vector_size(self)

    def swap(self, v):
        return _py_interop_summary.index_lane_summary_vector_swap(self, v)

    def rbegin(self):
        return _py_interop_summary.index_lane_summary_vector_rbegin(self)

    def rend(self):
        return _py_interop_summary.index_lane_summary_vector_rend(self)

    def clear(self):
        return _py_interop_summary.index_lane_summary_vector_clear(self)

    def get_allocator(self):
        return _py_interop_summary.index_lane_summary_vector_get_allocator(self)

    def pop_back(self):
        return _py_interop_summary.index_lane_summary_vector_pop_back(self)

    def erase(self, *args):
        return _py_interop_summary.index_lane_summary_vector_erase(self, *args)

    def __init__(self, *args):
        _py_interop_summary.index_lane_summary_vector_swiginit(self, _py_interop_summary.new_index_lane_summary_vector(*args))

    def push_back(self, x):
        return _py_interop_summary.index_lane_summary_vector_push_back(self, x)

    def front(self):
        return _py_interop_summary.index_lane_summary_vector_front(self)

    def back(self):
        return _py_interop_summary.index_lane_summary_vector_back(self)

    def assign(self, n, x):
        return _py_interop_summary.index_lane_summary_vector_assign(self, n, x)

    def resize(self, *args):
        return _py_interop_summary.index_lane_summary_vector_resize(self, *args)

    def insert(self, *args):
        return _py_interop_summary.index_lane_summary_vector_insert(self, *args)

    def reserve(self, n):
        return _py_interop_summary.index_lane_summary_vector_reserve(self, n)

    def capacity(self):
        return _py_interop_summary.index_lane_summary_vector_capacity(self)
    __swig_destroy__ = _py_interop_summary.delete_index_lane_summary_vector

# Register index_lane_summary_vector in _py_interop_summary:
_py_interop_summary.index_lane_summary_vector_swigregister(index_lane_summary_vector)


def summarize_index_metrics(*args):
    return _py_interop_summary.summarize_index_metrics(*args)


