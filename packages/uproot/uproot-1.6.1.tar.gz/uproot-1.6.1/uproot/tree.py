#!/usr/bin/env python

# Copyright (c) 2017, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from collections import namedtuple
from functools import reduce
import re
import sys

import numpy
array_types = (numpy.ndarray,)
toarray = lambda x: x

try:
    import pandas.core.series
except ImportError:
    pass
else:
    array_types = array_types + (pandas.core.series.Series,)
    oldtoarray = toarray
    def newtoarray(x):
        if isinstance(x, pandas.core.series.Series):
            return x.values
        else:
            return oldtoarray(x)
    toarray = newtoarray

import uproot.core
import uproot.rootio
import uproot._walker.arraywalker
import uproot._walker.lazyarraywalker

def _delayedraise(cls, err, trc):
    if sys.version_info[0] <= 2:
        exec("raise cls, err, trc")
    else:
        raise err.with_traceback(trc)
    
class TTree(uproot.core.TNamed,
            uproot.core.TAttLine,
            uproot.core.TAttFill,
            uproot.core.TAttMarker):
    """Represents a TTree, a table of data (possibly a ragged table, as some types allow for multiple items per TTree entry).

    Reading data:

        * `tree.arrays(...)` gets all or selected branches as arrays. It has many options; see help(TTree.arrays).
        * `tree.array(branch, ...)` gets a single branch as an array. It has many options; see help(TTree.array).
        * `tree.iterator(numentries, ...)` iterates over a fixed number of numentries at a time. It has many options; see help(TTree.iterator).

    Information about the tree:

        * `tree.numentries` is the number of entries.
        * `tree.branch(name)` gets a branch object by name.
        * `tree.branches` are the TBranch objects directly attached to the TTree's root.
        * `tree.allbranches` are all the TBranch objects, recursively following branches' branches.
        * `tree.branchnames` are all the directly attached branch names.
        * `tree.allbranchnames` are all the branch names, recursively following branches' branches.
        * `tree.branchtypes` is a `{name: dtype}` dict of all the directly attached branch names.
        * `tree.allbranchtypes` is a `{name: dtype}` dict of all the branch names, recursively following branches' branches.
        * `tree.leaves` are all the TLeaf objects.
        * `tree.counter` is a dict from branch names to Counter(branch, leaf) for branches that may have multiple items per TTree entry.

    `tree[name]` is a synonym for `tree.branch(name)`.

    TTree is not iterable, but `len(tree)` is a synonym for `tree.numentries`.
    """
    def __init__(self, filewalker, walker):
        walker.startcontext()
        start = walker.index
        vers, bcnt = self._readversion(walker)

        uproot.core.TNamed.__init__(self, filewalker, walker)
        uproot.core.TAttLine.__init__(self, filewalker, walker)
        uproot.core.TAttFill.__init__(self, filewalker, walker)
        uproot.core.TAttMarker.__init__(self, filewalker, walker)

        self.numentries, totbytes, zipbytes = walker.readfields("!qqq")

        if vers < 16:
            raise NotImplementedError("TTree too old")

        if vers >= 16:
            walker.skip("!q")  # fSavedBytes

        if vers >= 18:
            walker.skip("!q")  # flushed bytes

        walker.skip("!diii")   # fWeight, fTimerInterval, fScanField, fUpdate

        if vers >= 17:
            walker.skip("!i")  # fDefaultEntryOffsetLen

        if vers >= 19:
            nclus = walker.readfield("!i")  # fNClusterRange

        walker.skip("!qqqq")   # fMaxEntries, fMaxEntryLoop, fMaxVirtualSize, fAutoSave

        if vers >= 18:
            walker.skip("!q")  # fAutoFlush

        walker.skip("!q")      # fEstimate

        if vers >= 19:         # "FIXME" in go-hep
            walker.skip(1)
            walker.skip(nclus * 8)   # fClusterRangeEnd
            walker.skip(1)
            walker.skip(nclus * 8)   # fClusterSize

        self.branches = list(uproot.core.TObjArray(filewalker, walker))
        self.leaves = list(uproot.core.TObjArray(filewalker, walker))

        for i in range(7):
            # fAliases, fIndexValues, fIndex, fTreeIndex, fFriends, fUserInfo, fBranchRef
            uproot.rootio.Deserialized._deserialize(filewalker, walker)

        self._checkbytecount(walker.index - start, bcnt)

        leaves2branches = {}
        def recurse(obj):
            for branch in obj.branches:
                branch.numentries = self.numentries
                for leaf in branch.leaves:
                    leaves2branches[leaf.name] = branch.name
                recurse(branch)
        recurse(self)

        self.counter = {}
        def recurse(obj):
            for branch in obj.branches:
                for leaf in branch.leaves:
                    if leaf.counter is not None:
                        leafname = leaf.counter.name
                        branchname = leaves2branches[leafname]
                        self.counter[branch.name] = self.Counter(branchname, leafname)
                recurse(branch)
        recurse(self)

    Counter = namedtuple("Counter", ["branch", "leaf"])

    def __del__(self):
        del self.branches

    def __repr__(self):
        return "<TTree {0} len={1} at 0x{2:012x}>".format(repr(self.name), self.numentries, id(self))

    def __len__(self):
        return self.numentries

    def __getitem__(self, name):
        return self.branch(name)

    def __iter__(self):
        # prevent Python's attempt to interpret __len__ and __getitem__ as iteration
        raise TypeError("'TTree' object is not iterable")

    def branch(self, name):
        """Get a branch object by name.
        """
        if isinstance(name, str):
            name = name.encode("ascii")

        for branch in self.branches:
            if branch.name == name:
                return branch

            if isinstance(branch, TBranchElement):
                try:
                    return branch.branch(name)
                except KeyError:
                    pass

        raise KeyError("not found: {0}".format(repr(name)))

    @property
    def allbranches(self):
        out = []
        for branch in self.branches:
            out.append(branch)
            out.extend(branch.allbranches)
        return out

    @property
    def branchnames(self):
        return [branch.name for branch in self.branches if hasattr(branch, "dtype")]

    @property
    def allbranchnames(self):
        return [branch.name for branch in self.allbranches if hasattr(branch, "dtype")]

    @property
    def branchtypes(self):
        return dict((branch.name, branch.dtype) for branch in self.branches if hasattr(branch, "dtype"))

    @property
    def allbranchtypes(self):
        return dict((branch.name, branch.dtype) for branch in self.allbranches if hasattr(branch, "dtype"))

    @staticmethod
    def _normalizeselection(branchdtypes, allbranches):
        if callable(branchdtypes):
            for branch in allbranches:
                dtype = branchdtypes(branch)
                if dtype is not None:
                    if isinstance(dtype, array_types):
                        dtype = dtype.reshape(reduce(lambda x, y: x*y, dtype.shape, 1))
                    elif not isinstance(dtype, numpy.dtype):
                        dtype = numpy.dtype(dtype)
                    yield branch, dtype

        elif isinstance(branchdtypes, dict):
            allbranches = dict((x.name, x) for x in allbranches)
            for name, dtype in branchdtypes.items():
                if hasattr(name, "encode"):
                    name = name.encode("ascii")
                if name in allbranches:
                    branch = allbranches[name]
                    if hasattr(branch, "dtype"):
                        if isinstance(dtype, array_types):
                            dtype = dtype.reshape(reduce(lambda x, y: x*y, dtype.shape, 1))
                        elif not isinstance(dtype, numpy.dtype):
                            dtype = numpy.dtype(dtype)
                        yield branch, dtype
                    else:
                        raise ValueError("cannot produce an array from branch {0}".format(repr(name)))
                else:
                    raise ValueError("cannot find branch {0}".format(repr(name)))

        elif isinstance(branchdtypes, (str, bytes)):
            if hasattr(branchdtypes, "encode"):
                name = branchdtypes.encode("ascii")
            else:
                name = branchdtypes

            branch = [x for x in allbranches if x.name == name]
            if len(branch) == 1:
                if hasattr(branch[0], "dtype"):
                    yield branch[0], branch[0].dtype
                else:
                    raise ValueError("cannot produce an array from branch {0}".format(repr(name)))
            else:
                raise ValueError("cannot find branch {0}".format(repr(name)))

        else:
            try:
                names = [x.encode("ascii") if hasattr(x, "encode") else x for x in branchdtypes]
            except:
                raise TypeError("branchdtypes argument not understood")
            else:
                allbranches = dict((x.name, x) for x in allbranches)
                for name in names:
                    if name in allbranches:
                        branch = allbranches[name]
                        if hasattr(branch, "dtype"):
                            yield branch, branch.dtype
                        else:
                            raise ValueError("cannot produce an array from branch {0}".format(repr(name)))
                    else:
                        raise ValueError("cannot find branch {0}".format(repr(name)))

    def iterator(self, entries, branchdtypes=lambda branch: getattr(branch, "dtype", None), executor=None, outputtype=dict, reportentries=False):
        """Iterates over a fixed number of entries at a time.

        Instead of loading all entries from a tree with `tree.arrays()`, load a manageable number that will fit in memory at once and apply a continuous process to it. Example use:

            for px, py in tree.iterator(10000, ["px", "py"], outputtype=tuple):
                do_something(sqrt(px**2 + py**2))

        Arguments:

            * `entries` *(required)*

              If a positive integer, the number of entries to yield in each step of iteration.
              Otherwise, `entries` is interpreted as an iterable over `(entrystart, entryend)` ranges, which must be strictly increasing.

            * `branchdtypes` (same as in `TTree.arrays`)

              If a single string, the string names the only branch to load.
              If an iterable of strings, all of these are loaded (in the specified order).
              If a dict of `{name: dtype}`, load the specified branch names and cast them into a given `dtype` (such as conversion to little endian).
              If a function from branch names to `dtype` or `None`, load the branches into the given `dtypes` and don't load the branches mapped to `None`.

              If any `dtypes` are actually arrays, rather than `dtype` objects, then those arrays will be filled instead of creating new ones (shape must match).

            * `executor` (same as in `TTree.arrays`)

              A `concurrent.futures.Executor` that would be used to parallelize the basket loading/decompression.
              If `None`, the process is serial.

            * `outputtype` (same as in `TTree.arrays`)

              Constructor for the objects to yield in the iterator. Good choices include `dict`, `tuple`, `namedtuple`, `list`.

            * `reportentries`

              If `True`, yield `(entrystart, entryend, data)` instead of just `data`. Intended as a convenience or cross-check for analysis.
        """
        if isinstance(entries, int):
            if entries < 1:
                raise ValueError("number of entries per iteration must be at least 1")
            if sys.version_info[0] <= 2:
                ranges = ((x, x + entries) for x in xrange(0, self.numentries, entries))
            else:
                ranges = ((x, x + entries) for x in range(0, self.numentries, entries))
        else:
            ranges = entries
        
        toget = []
        for branch, dtype in self._normalizeselection(branchdtypes, self.allbranches):
            toget.append((branch, dtype, []))
            if not hasattr(branch, "basketwalkers"):
                branch._preparebaskets()

        if outputtype == namedtuple:
            outputtype = namedtuple("Arrays", [branch.name.decode("ascii") for branch, dtype, cache in toget])

        lastentryend = None
        for entrystart, entryend in ranges:
            if lastentryend is not None and entrystart < lastentryend:
                raise ValueError("entries expressed as (entrystart, entryend) pairs must always have entrystart[i+1] >= entryend[i], but entrystart[i+1] is {0} and entryend[i] is {1}".format(entrystart, lastentryend))
            lastentryend = entryend

            def dobranch(branchdtypecache):
                branch, dtype, cache = branchdtypecache

                # always addtocache before delfromcache so that it doesn't forget the last basketnumber (i)
                branch._addtocache(cache, entrystart, entryend, executor is not None)
                branch._delfromcache(cache, entrystart)

                out = branch._getfromcache(cache, entrystart, entryend, dtype)

                if issubclass(outputtype, dict):
                    return branch.name, out
                else:
                    return out

            if executor is None:
                out = [dobranch(x) for x in toget]
            else:
                out = list(executor.map(dobranch, toget))

            if issubclass(outputtype, dict) or outputtype == tuple or outputtype == list:
                out = outputtype(out)
            else:
                out = outputtype(*out)

            if reportentries:
                yield entrystart, min(entryend, self.numentries), out
            else:
                yield out

    def lazyarrays(self, branchdtypes=lambda branch: getattr(branch, "dtype", None), outputtype=dict):
        """Creates a proxy for an array that gets data on demand.

        Arguments:

            * `branchdtypes` (same as in `TTree.iterator`)

              If a single string, the string names the only branch to load.
              If an iterable of strings, all of these are loaded (in the specified order).
              If a dict of `{name: dtype}`, load the specified branch names and cast them into a given `dtype` (such as conversion to little endian).
              If a function from branch names to `dtype` or `None`, load the branches into the given `dtypes` and don't load the branches mapped to `None`.

              If any `dtypes` are actually arrays, rather than `dtype` objects, then those arrays will be filled instead of creating new ones (shape must match).

            * `outputtype` (same as in `TTree.iterator`)

              Constructor for the objects to yield in the iterator. Good choices include `dict`, `tuple`, `namedtuple`, `list`.
        """
        toget = []
        for branch, dtype in self._normalizeselection(branchdtypes, self.allbranches):
            toget.append((branch, dtype))

        if outputtype == namedtuple:
            outputtype = namedtuple("Arrays", [branch.name.decode("ascii") for branch, dtype in toget])

        out = []
        for branch, dtype in toget:
            outi = branch.lazyarray(dtype)
            if outputtype == dict:
                out.append((branch.name, outi))
            else:
                out.append(outi)

        if issubclass(outputtype, dict) or outputtype == tuple or outputtype == list:
            return outputtype(out)
        else:
            return outputtype(*out)

    def arrays(self, branchdtypes=lambda branch: getattr(branch, "dtype", None), executor=None, outputtype=dict, block=True):
        """Extracts whole branches into Numpy arrays.

        Individual branches from TTrees are typically small enough to fit into memory. If this is not your case, consider `tree.iterator(entries)` to load a given number of entries at a time.

        Arguments:

            * `branchdtypes` (same as in `TTree.iterator`)

              If a single string, the string names the only branch to load.
              If an iterable of strings, all of these are loaded (in the specified order).
              If a dict of `{name: dtype}`, load the specified branch names and cast them into a given `dtype` (such as conversion to little endian).
              If a function from branch names to `dtype` or `None`, load the branches into the given `dtypes` and don't load the branches mapped to `None`.

              If any `dtypes` are actually arrays, rather than `dtype` objects, then those arrays will be filled instead of creating new ones (shape must match).

            * `executor` (same as in `TTree.iterator`)

              A `concurrent.futures.Executor` that would be used to parallelize the basket loading/decompression.
              If `None`, the process is serial.

            * `outputtype` (same as in `TTree.iterator`)

              Constructor for the objects to yield in the iterator. Good choices include `dict`, `tuple`, `namedtuple`, `list`.

            * `block`

              If `True` and parallel processing with an `executor`, return `data, errors` instead of just `data`, where `errors` is a generator of exceptions raised by the parallel threads.
              When you're ready to wait for all threads to finish, evaluate the `errors` generator.
        """
        toget = []
        for branch, dtype in self._normalizeselection(branchdtypes, self.allbranches):
            toget.append((branch, dtype))
            if not hasattr(branch, "basketwalkers"):
                branch._preparebaskets()

        if outputtype == namedtuple:
            outputtype = namedtuple("Arrays", [branch.name.decode("ascii") for branch, dtype in toget])

        out = []
        errorslist = []
        for branch, dtype in toget:
            outi, res = branch.array(dtype, executor, False)
            if outputtype == dict:
                out.append((branch.name, outi))
            else:
                out.append(outi)
            errorslist.append(res)

        if issubclass(outputtype, dict) or outputtype == tuple or outputtype == list:
            out = outputtype(out)
        else:
            out = outputtype(*out)

        if block:
            for errors in errorslist:
                for cls, err, trc in errors:
                    if cls is not None:
                        _delayedraise(cls, err, trc)
            return out
        else:
            return out, (item for sublist in errorslist for item in sublist)

    def lazyarray(self, branch, dtype=None):
        """Creates a proxy for an array that gets data on demand.

        Arguments:

            * `branch` *(required)*

               Branch name to extract.

            * `dtype`

               If not `None`, cast the array into a given `dtype` (such as conversion to little endian).
        """
        branch = branch.encode("ascii") if hasattr(branch, "encode") else branch
        return self.branch(branch).lazyarray(dtype)

    def array(self, branch, dtype=None, executor=None, block=True):
        """Extracts a whole branch into a Numpy array.

        Individual branches from TTrees are typically small enough to fit into memory. If this is not your case, consider `tree.iterator(entries)` to load a given number of entries at a time.

        Arguments:

            * `branch` *(required)*

               Branch name to extract.

            * `dtype`

               If not `None`, cast the array into a given `dtype` (such as conversion to little endian).
               If an array object, fill that array instead of creating a new one (shape must match).

            * `executor` (same as in `TTree.arrays`)

              A `concurrent.futures.Executor` that would be used to parallelize the basket loading/decompression.
              If `None`, the process is serial.

            * `block`

              If `True` and parallel processing with an `executor`, return `data, errors` instead of just `data`, where `errors` is a generator of exceptions raised by the parallel threads.
              When you're ready to wait for all threads to finish, evaluate the `errors` generator.
        """
        branch = branch.encode("ascii") if hasattr(branch, "encode") else branch

        if dtype is None:
            branchdtypes = branch
        else:
            branchdtypes = {branch: dtype}

        if block:
            out, = self.arrays(branchdtypes=branchdtypes, executor=executor, outputtype=tuple, block=block)
            return out
        else:
            (out,), errors = self.arrays(branchdtypes=branchdtypes, executor=executor, outputtype=tuple, block=block)
            return out, errors

    class _Connector(object): pass

    @property
    def arrowed(self):
        import uproot._connect.toarrowed
        connector = self._Connector()

        def schema(*args, **kwds):
            return uproot._connect.toarrowed.schema(self, *args, **kwds)
        connector.schema = schema

        def proxy(schema=None):
            return uproot._connect.toarrowed.proxy(self, schema)
        connector.proxy = proxy

        def run(*args, **kwds):
            return uproot._connect.toarrowed.run(self, *args, **kwds)
        connector.run = run

        def compile(*args, **kwds):
            return uproot._connect.toarrowed.compile(self, *args, **kwds)
        connector.compile = compile

        return connector

    @property
    def pandas(self):
        import pandas
        connector = self._Connector()

        def df(branchdtypes, executor=None, block=True):
            toget = []
            for branch, dtype in self._normalizeselection(branchdtypes, self.allbranches):
                toget.append((branch, dtype))

            size = None
            oldname = None
            data = {}
            columns = []
            for b, d in toget:
                if size is None:
                    size = b.numitems
                elif size != b.numitems:
                    raise ValueError("cannot construct a DataFrame because branch {0} has {1} items but branch {2} has {3} items".format(repr(oldname), size, repr(b.name), b.numitems))
                oldname = b.name
                data[b.name] = d.type(0)
                columns.append(b.name)

            df = pandas.DataFrame(data, columns=columns, index=numpy.arange(size))

            errorslist = []
            for b, d in toget:
                arr, err = b.array(df[b.name], executor=executor, block=False)
                errorslist.append(err)

            if block:
                for errors in errorslist:
                    for cls, err, trc in errors:
                        if cls is not None:
                            _delayedraise(cls, err, trc)
                return df
            else:
                return df, (item for sublist in errorslist for item in sublist)
        connector.df = df

        return connector

uproot.rootio.Deserialized.classes[b"TTree"] = TTree

## TODO: this is a good candidate for acceleration with Numba...
if sys.version_info[0] <= 2:
    def _fixspeedbumps(array, outdata, offs):
        outi = 0
        for i in xrange(len(offs) - 1):
            length = offs[i + 1] - offs[i] - 1
            outdata[outi:outi + length] = array[offs[i] + 1:offs[i + 1]]
            outi += length
else:
    def _fixspeedbumps(array, outdata, offs):
        outi = 0
        for i in range(len(offs) - 1):
            length = offs[i + 1] - offs[i] - 1
            outdata[outi:outi + length] = array[offs[i] + 1:offs[i + 1]]
            outi += length

class TBranch(uproot.core.TNamed,
              uproot.core.TAttFill):
    """Represents a TBranch, a single column of data in a TTree.

    Reading data:

        * `branch.array(...)` gets the branch as an array. It has many options; see help(TBranch.array).
        * `tree.iterator(entries, ...)` iterates over a fixed number of entries at a time. It has many options; see help(TTree.iterator).

    Information about the branch:

        * `branch.itemdims` are the fixed (non-counter) dimensions of this branch, derived from its title.
        * `branch.branch(name)` gets a subbranch object by name.
        * `branch.branches` are the subbranches directly attached to this TBranch.
        * `branch.allbranches` are all the subbranches, recursively following subbranches' branches.
        * `branch.branchnames` are all the directly attached subbranch names.
        * `branch.allbranchnames` are all the subbranch names, recursively following subbranches' branches.
        * `branch.branchtypes` is a `{name: dtype}` dict of all the directly attached subbranch names.
        * `branch.allbranchtypes` is a `{name: dtype}` dict of all the subbranch names, recursively following subbranches' branches.
        * `branch.leaves` are all the TLeaf objects directly attached to this TBranch.
        * `branch.numentries` is the number of entries in this branch (same as in the tree).
        * `branch.numbaskets` is the number of baskets.
        * `branch.numbytes` is the number of bytes used by data in this branch.
        * `branch.numitems` is the number of items, such as integers, floating point values, or the number of characters in the strings in this branch.
        * `branch.basketbytes(i)` is the number of bytes used by data in basket i.
        * `branch.basketitems(i)` is the number of items, such as integers, floating point values, or the number of characters in the strings in basket i.
        * `branch.basketentries(i)` is the number of entries in basket i.
        * `branch.basketstart(i)` is the starting entry for basket i.

    `branch[name]` is a synonym for `branch.branch(name)`.
    """
    def __init__(self, filewalker, walker):
        walker.startcontext()
        start = walker.index
        vers, bcnt = self._readversion(walker)

        if vers < 11:
            raise NotImplementedError("TBranch version too old")

        uproot.core.TNamed.__init__(self, filewalker, walker)
        uproot.core.TAttFill.__init__(self, filewalker, walker)

        compression, basketSize, entryOffsetLen, writeBasket, entryNumber, offset, maxBaskets, splitLevel, entries, firstEntry, totBytes, zipBytes = walker.readfields("!iiiiqiiiqqqq")
        self.compression = uproot.rootio._interpret_compression(compression)

        self.branches = list(uproot.core.TObjArray(filewalker, walker))
        self.leaves = list(uproot.core.TObjArray(filewalker, walker))
        self._skipbcnt(walker) # reading baskets is expensive and useless

        # walker.skip(1)  # isArray
        # self._basketBytes = walker.readarray(">i4", maxBaskets)[:writeBasket]
        walker.skip(1 + 4*maxBaskets)
        
        walker.skip(1)  # isArray
        self._basketEntry = walker.readarray(">i8", maxBaskets)[:writeBasket]

        walker.skip(1)  # isArray
        self._basketSeek = walker.readarray(">i8", maxBaskets)[:writeBasket]

        fname = walker.readstring()

        self._checkbytecount(walker.index - start, bcnt)

        if len(self.leaves) == 1 and hasattr(self.leaves[0], "dtype"):
            self.dtype = self.leaves[0].dtype
            self._speedbumps = self.leaves[0]._speedbumps

        self._filewalker = filewalker

        self.itemdims = ()
        if len(self.leaves) == 1:
            m = self._titlehasdims.match(self.leaves[0].title)
            if m is not None:
                self.itemdims = tuple(int(x) for x in re.findall(self._itemdimpattern, self.leaves[0].title))

    _titlehasdims = re.compile(br"^([^\[\]]+)(\[[^\[\]]+\])+")
    _itemdimpattern = re.compile(br"\[([1-9][0-9]*)\]")

    def __del__(self):
        del self.branches
        del self._filewalker

    @property
    def numbaskets(self):
        return len(self._basketSeek)

    @property
    def numbytes(self):
        return sum(self.basketbytes(i) for i in range(len(self._basketSeek)))

    @property
    def numitems(self):
        if self.dtype == numpy.dtype(object):
            return self.numbytes - self.numentries
        else:
            return self.numbytes // self.dtype.itemsize

    def basketbytes(self, i):
        if not hasattr(self, "basketobjlens"):
            self._minipreparebaskets()

        if not 0 <= i < len(self._basketobjlens):
            raise IndexError("index {0} out of range for branch with {1} baskets".format(i, len(self._basketobjlens)))
        trial = self._basketobjlens[i]
        entries = self.basketentries(i)

        if self._speedbumps:
            return trial - entries*4 - 8 - entries
        elif self.dtype == numpy.dtype(object) or trial != entries * reduce(lambda x, y: x*y, self.itemdims, self.dtype.itemsize):
            return trial - entries*4 - 8
        else:
            return trial

    def basketitems(self, i):
        if self.dtype == numpy.dtype(object):
            return self.basketbytes(i) - self.basketentries(i)
        else:
            return self.basketbytes(i) // self.dtype.itemsize

    def basketentries(self, i):
        if not 0 <= i < len(self._basketEntry):
            raise IndexError("index {0} out of range for branch with {1} baskets".format(i, len(self._basketEntry)))
        if i + 1 == len(self._basketEntry):
            return self.numentries - self._basketEntry[i]
        else:
            return self._basketEntry[i + 1] - self._basketEntry[i]

    def basketstart(self, i):
        if not 0 <= i < len(self._basketEntry):
            raise IndexError("index {0} out of range for branch with {1} baskets".format(i, len(self._basketEntry)))
        return self._basketEntry[i]

    @property
    def allbranches(self):
        out = []
        for branch in self.branches:
            out.append(branch)
            out.extend(branch.allbranches)
        return out

    @property
    def branchnames(self):
        return [branch.name for branch in self.branches if hasattr(branch, "dtype")]

    @property
    def allbranchnames(self):
        return [branch.name for branch in self.allbranches if hasattr(branch, "dtype")]

    @property
    def branchtypes(self):
        return dict((branch.name, branch.dtype) for branch in self.branches if hasattr(branch, "dtype"))

    @property
    def allbranchtypes(self):
        return dict((branch.name, branch.dtype) for branch in self.allbranches if hasattr(branch, "dtype"))

    def __getitem__(self, name):
        return self.branch(name)

    def __iter__(self):
        # prevent Python's attempt to interpret __getitem__ as iteration
        raise TypeError("'TBranch' object is not iterable")

    def branch(self, name):
        """Get a subbranch object by name.
        """
        if isinstance(name, str):
            name = name.encode("ascii")

        for branch in self.branches:
            if branch.name == name:
                return branch
            try:
                return branch.branch(name)
            except KeyError:
                pass

        raise KeyError("not found: {0}".format(repr(name)))

    def _minipreparebaskets(self):
        self._filewalker.startcontext()

        self._basketobjlens = []
        self._basketkeylens = []
        for seek in self._basketSeek:
            basketwalker = self._filewalker.copy(seek)
            basketwalker.startcontext()

            bytes, version, objlen, datetime, keylen, cycle = basketwalker.readfields("!ihiIhh")
        
            self._basketobjlens.append(objlen)
            self._basketkeylens.append(keylen)

    def _preparebaskets(self):
        self._filewalker.startcontext()

        self._basketobjlens = []
        self._basketkeylens = []
        self._basketborders = []
        self._basketlengths = []
        self._basketwalkers = []
        for seek in self._basketSeek:
            basketwalker = self._filewalker.copy(seek)
            basketwalker.startcontext()

            bytes, version, objlen, datetime, keylen, cycle = basketwalker.readfields("!ihiIhh")
            if version > 1000:
                seekkey, seekpdir = basketwalker.readfields("!qq")
            else:
                seekkey, seekpdir = basketwalker.readfields("!ii")

            self._basketobjlens.append(objlen)
            self._basketkeylens.append(keylen)

            classname = basketwalker.readstring()
            name = basketwalker.readstring()
            title = basketwalker.readstring()
            vers, bufsize, nevsize, nevbuf, last, flag = basketwalker.readfields("!HiiiiB")
            border = last - keylen

            self._basketborders.append(border)
            if self._speedbumps:
                self._basketlengths.append(border - (objlen - border - 8) // 4)
            else:
                self._basketlengths.append(border)

            #  object size != compressed size means it's compressed
            if objlen != bytes - keylen:
                function = uproot.rootio._decompressfcn(self.compression, objlen)
                self._basketwalkers.append(uproot._walker.lazyarraywalker.LazyArrayWalker(self._filewalker.copy(seekkey + keylen), function, bytes - keylen))

            # otherwise, it's uncompressed
            else:
                self._basketwalkers.append(self._filewalker.copy(seek + keylen))

    def _basket(self, i, offsets=False, parallel=False):
        self._basketwalkers[i]._evaluate(parallel)
        self._basketwalkers[i].startcontext()
        start = self._basketwalkers[i].index

        try:
            if self.dtype == numpy.dtype(object) or self._speedbumps:
                array = self._basketwalkers[i].readarray(numpy.uint8, self._basketobjlens[i])
            else:
                array = self._basketwalkers[i].readarray(self.dtype, self._basketobjlens[i] // self.dtype.itemsize)
        finally:
            self._basketwalkers[i]._unevaluate()
            self._basketwalkers[i].index = start

        if self._speedbumps:
            offs = array[self._basketborders[i] + 4:].view(">i4") - self._basketkeylens[i]
            offs[-1] = self._basketborders[i]

            outdata = numpy.empty(self._basketborders[i] - (len(offs) - 1), dtype=numpy.uint8)
            _fixspeedbumps(array, outdata, offs)

            if offsets:
                return outdata.view(self.dtype), None
            else:
                return outdata.view(self.dtype)

        if self.dtype == numpy.dtype(object):
            dataend = self._basketborders[i]
        else:
            dataend = self._basketborders[i] // self.dtype.itemsize
                
        if offsets:
            if dataend == len(array):
                return array, None
            else:
                outdata = array[:dataend]
                outoff = array.view(numpy.uint8)[self._basketborders[i] + 4 : -4].view(">i4") - self._basketkeylens[i]
                return outdata, outoff

        elif dataend < len(array):
            return array[:dataend]

        else:
            return array

    def _adddimensions(self, array):
        if self.itemdims == () or len(array.shape) != 1:
            return array
        else:
            product = reduce(lambda x, y: x*y, self.itemdims, 1)
            if len(array) % product != 0:
                raise IOError("data shape of {0} is misaligned ({1} elements can't be reshaped as {2})".format(repr(self.name), len(array), self.itemdims))
            else:
                newlen = len(array) // product
                return array.reshape((newlen,) + self.itemdims)

    def _addtocache(self, cache, entrystart, entryend, parallel=False):
        if len(cache) == 0:
            i = 0
        else:
            i = cache[-1][0] + 1

        while i < len(self._basketEntry) and entryend > self._basketEntry[i]:
            if i + 1 >= len(self._basketEntry) or self._basketEntry[i + 1] > entrystart:
                data, off = self._basket(i, offsets=True, parallel=parallel)
                cache.append((i, data, off))
            i += 1

    def _delfromcache(self, cache, entrystart):
        firsttokeep = 0
        for i, data, off in cache:
            if i + 1 < len(self._basketEntry) and self._basketEntry[i + 1] <= entrystart:
                firsttokeep += 1
            else:
                break
        del cache[:firsttokeep]

    def _getfromcache(self, cache, entrystart, entryend, dtype):
        if len(cache) == 0:
            if isinstance(dtype, array_types):
                out = dtype.reshape(reduce(lambda x, y: x*y, dtype.shape, 1))
                dtype = out.dtype
                if out.shape != (0,):
                    raise ValueError("provided array does not have the right number of elements: {0}".format(0))
                return self._adddimensions(out)
            else:
                return self._adddimensions(numpy.array([], dtype=dtype))

        entrywidth = reduce(lambda x, y: x*y, self.itemdims, 1)
        strings = (dtype == numpy.dtype(object))
        if strings:
            selfitemsize = 1
        else:
            selfitemsize = self.dtype.itemsize

        i, firstdata, firstoff = cache[0]
        if firstoff is None:
            istart = (entrystart - self._basketEntry[i]) * entrywidth
        else:
            istartoff = entrystart - self._basketEntry[i]
            istart = firstoff[istartoff] // selfitemsize

        i, lastdata, lastoff = cache[-1]
        iendoff = entryend - self._basketEntry[i]
        if lastoff is None:
            iend = min((entryend - self._basketEntry[i]) * entrywidth, len(lastdata))
        elif iendoff < len(lastoff):
            iendoff = min(iendoff, len(lastoff))
            iend = lastoff[iendoff] // selfitemsize
        else:
            iendoff = min(iendoff, len(lastoff))
            iend = len(lastdata)

        if len(cache) == 1:
            outdata = firstdata[istart:iend]
            if not strings:
                if isinstance(dtype, array_types):
                    out = toarray(dtype)
                    dtype = out.dtype
                    expected = len(firstdata)
                    if out.shape != (expected,):
                        raise ValueError("provided array does not have the right number of elements: {0}".format(expected))
                    out[:] = outdata
                    outdata = out
                else:
                    outdata = numpy.array(outdata, dtype=dtype)
            else:
                outoff = firstoff[istartoff:iendoff] - istart

        else:
            middle = cache[1:-1]
            size = (len(firstdata) - istart) + sum(len(mdata) for mi, mdata, moff in middle) + (iend)

            if isinstance(dtype, array_types):
                outdata = toarray(dtype)
                dtype = outdata.dtype
                if outdata.shape != (size,):
                    raise ValueError("provided array does not have the right number of elements: {0}".format(size))
            else:
                outdata = numpy.empty(size, dtype=numpy.uint8 if strings else dtype)

            if strings:
                outoff = numpy.empty((len(firstoff) - istartoff) + sum(len(moff) for mi, mdata, moff in middle) + (iendoff), dtype=firstoff.dtype)

            i = len(firstdata) - istart
            outdata[:i] = firstdata[istart:]
            if strings:
                ioff = len(firstoff) - istartoff
                outoff[:ioff] = firstoff[istartoff:] - istart
                correction = i

            for mi, mdata, moff in middle:
                outdata[i:i + len(mdata)] = mdata
                i += len(mdata)
                if strings:
                    outoff[ioff:ioff + len(moff)] = moff + correction
                    ioff += len(moff)
                    correction += len(mdata)

            outdata[i:] = lastdata[:iend]
            if strings:
                outoff[ioff:] = lastoff[:iendoff] + correction

        if strings:
            out = numpy.empty(len(outoff), dtype=numpy.dtype(object))
            for j, offset in enumerate(outoff):
                size = outdata[offset]
                out[j] = outdata[offset + 1:offset + 1 + size].tostring()
            return self._adddimensions(out)
        else:
            return self._adddimensions(outdata)

    def baskets(self, callback=None, offsets=False, reportentries=False, executor=None):
        """Extracts all baskets from the branch as separate Numpy arrays.

        This provides access to the data in the most raw form: zero-copy views. If your ROOT file is uncompressed and you opened it as a memory map (the default), the Numpy arrays returned from this function will be views into the operating system's own page cache.
        
        This method does not have a `dtype` argument because data are not copied, so the user has no choice about its contents. (The `callback` or subsequent processing may change its `dtype`.)

        Arguments:

            * `callback`

              If `None`, this method returns an iterator over arrays, one basket at a time.
              If a callable, this method applies `callback` to each basket array as it becomes available, returning the return values of the `callback` as an iterator.

            * `offsets`

              If `True`, the iterator yields an `offset` array, specifying the starting index of each entry in the basket, or an `offset` array is given as the second argument to the `callback` (after `array`, the first argument).

            * `reportentries`

              If `True`, the iterator yields `entrystart` and `entryend`, specifying the first and last-plus-one entry in the basket, as the last two items in the yielded tuple or the last two arguments to the `callback`.

              Different branches are not guaranteed to begin and end baskets at the same entry boundaries, though they often do align by happenstance, especially for flat ntuples.

            * `executor` (same as in `TTree.array`)

              If `None`, this method reads baskets serially, loading and/or decompressing one basket after the previous has been yielded or the previous `callback` has finished running.
              If a `concurrent.futures.Executor`, this `executor` is used to do basket loading, decompression, and `callback` execution in parallel. The return result is an iterator over arrays, `callback` results, or exceptions raised as sys.exc_info() 3-tuples, all in basket order.
        """

        if not hasattr(self, "basketwalkers"):
            self._preparebaskets()

        entrywidth = reduce(lambda x, y: x*y, self.itemdims, 1)

        if executor is None:
            for i in range(len(self._basketwalkers)):
                if offsets:
                    array, offs = self._basket(i, offsets=offsets, parallel=False)

                    if offs is None:
                        offs = numpy.linspace(0, (self.basketentries(i) - 1) * entrywidth, self.basketentries(i), dtype=">i4")
                    else:
                        offs = offs // self.dtype.itemsize

                    out = (array, offs)

                else:
                    out = (self._adddimensions(self._basket(i, offsets=offsets, parallel=False)),)
                
                if reportentries:
                    entrystart = self._basketEntry[i]
                    entryend = self._basketEntry[i + 1] if i + 1 < len(self._basketEntry) else self.numentries
                    out = out + (entrystart, entryend)

                if callback is None:
                    yield out
                else:
                    yield callback(*out)

        else:
            def fill(i):
                try:
                    if offsets:
                        array, offs = self._basket(i, offsets=offsets, parallel=False)

                        if offs is None:
                            offs = numpy.linspace(0, (self.basketentries(i) - 1) * entrywidth, self.basketentries(i), dtype=">i4")
                        else:
                            offs = offs // self.dtype.itemsize

                        out = (array, offs)

                    else:
                        out = (self._adddimensions(self._basket(i, offsets=offsets, parallel=False)),)

                    if reportentries:
                        entrystart = self._basketEntry[i]
                        entryend = self._basketEntry[i + 1] if i + 1 < len(self._basketEntry) else self.numentries
                        out = out + (entrystart, entryend)

                    if callback is None:
                        return out
                    else:
                        return callback(*out)

                except:
                    return sys.exc_info()

            for result in executor.map(fill, range(len(self._basketwalkers))):
                yield result

    def array(self, dtype=None, executor=None, block=True):
        """Extracts the whole branch into a Numpy array.

        Individual branches are typically small enough to fit into memory. If this is not your case, consider `tree.iterator(entries)` to load a given number of entries at a time.

        Arguments:

            * `dtype`

               If not `None`, cast the array into a given `dtype` (such as conversion to little endian).
               If an array object, fill that array instead of creating a new one (shape must match).

            * `executor` (same as in `TTree.array`)

              A `concurrent.futures.Executor` that would be used to parallelize the basket loading/decompression.
              If `None`, the process is serial.

            * `block`

              If `True` and parallel processing with an `executor`, return `data, errors` instead of just `data`, where `errors` is a generator of exceptions raised by the parallel threads.
              When you're ready to wait for all threads to finish, evaluate the `errors` generator.
        """

        if not hasattr(self, "basketwalkers"):
            self._preparebaskets()

        if self.dtype == numpy.dtype(object):
            selfitemsize = 1
        else:
            selfitemsize = self.dtype.itemsize

        if isinstance(dtype, array_types):
            out = toarray(dtype).reshape(reduce(lambda x, y: x*y, dtype.shape, 1))
            dtype = out.dtype

            if isinstance(out, numpy.ndarray) and dtype == numpy.dtype(object):
                expected = self.numentries
            else:
                expected = sum(self._basketlengths) // selfitemsize

            if out.shape != (expected,):
                raise ValueError("provided array does not have the right number of elements: {0}".format(expected))

        else:
            if dtype is None:
                dtype = self.dtype

            if not isinstance(dtype, numpy.dtype):
                dtype = numpy.dtype(dtype)

            if dtype == numpy.dtype(object):
                out = numpy.empty(self.numentries, dtype=numpy.dtype(object))
            else:
                out = numpy.empty(sum(self._basketlengths) // selfitemsize, dtype=dtype)

        if dtype == numpy.dtype(object):
            return self._adddimensions(self._strings(out, executor, block))

        if executor is None:
            start = 0
            for i in range(len(self._basketwalkers)):
                end = start + self._basketlengths[i] // selfitemsize
                out[start:end] = self._basket(i, parallel=False)
                start = end

            if block:
                return self._adddimensions(out)
            else:
                return self._adddimensions(out), ()

        else:
            ends = (numpy.cumsum(self._basketlengths) // selfitemsize).tolist()
            starts = [0] + ends[:-1]

            def fill(i):
                try:
                    out[starts[i]:ends[i]] = self._basket(i, parallel=True)
                except:
                    return sys.exc_info()
                else:
                    return None, None, None

            errors = executor.map(fill, range(len(self._basketwalkers)))
            if block:
                for cls, err, trc in errors:
                    if cls is not None:
                        _delayedraise(cls, err, trc)
                return self._adddimensions(out)
            else:
                return self._adddimensions(out), errors

    def _strings(self, out, executor, block):
        if executor is None:
            for i in range(len(self._basketwalkers)):
                data, offsets = self._basket(i, offsets=True, parallel=False)
                for j, offset in enumerate(offsets):
                    size = data[offset]
                    out[self._basketEntry[i] + j] = data[offset + 1:offset + 1 + size].tostring()

            if block:
                return out
            else:
                return out, ()

        else:
            def fill(i):
                try:
                    data, offsets = self._basket(i, offsets=True, parallel=True)
                    for j, offset in enumerate(offsets):
                        size = data[offset]
                        out[self._basketEntry[i] + j] = data[offset + 1:offset + 1 + size].tostring()
                except:
                    return sys.exc_info()
                else:
                    return None, None, None

            errors = executor.map(fill, range(len(self._basketwalkers)))
            if block:
                for cls, err, trc in errors:
                    if cls is not None:
                        _delayedraise(cls, err, trc)
                return out
            else:
                return out, errors

    class LazyArray(object):
        def __init__(self, branch, dtype):
            if dtype == numpy.dtype(object):
                raise NotImplementedError
            self._branch = branch
            self.dtype = dtype

        @property
        def shape(self):
            newlen = self._branch.numitems // reduce(lambda x, y: x*y, self._branch.itemdims, 1)
            return (newlen,) + self._branch.itemdims

        def __len__(self):
            return self.shape[0]
            
        # interpret negative indexes as starting at the end of the dataset
        def __normalize(self, i, clip, step):
            lenself = len(self)
            if i < 0:
                j = lenself + i
                if j < 0:
                    if clip:
                        return 0 if step > 0 else lenself
                    else:
                        raise IndexError("index out of range: {0} for length {1}".format(i, lenself))
                else:
                    return j
            elif i < lenself:
                return i
            elif clip:
                return lenself if step > 0 else 0
            else:
                raise IndexError("index out of range: {0} for length {1}".format(i, lenself))

        def __normalizeslice(self, s):
            lenself = len(self)
            if s.step is None:
                step = 1
            else:
                step = s.step
            if step == 0:
                raise ValueError("slice step cannot be zero")
            if s.start is None:
                if step > 0:
                    start = 0
                else:
                    start = lenself - 1
            else:
                start = self.__normalize(s.start, True, step)
            if s.stop is None:
                if step > 0:
                    stop = lenself
                else:
                    stop = -1
            else:
                stop = self.__normalize(s.stop, True, step)

            return start, stop, step

        def __startfill(self):
            if not hasattr(self._branch, "basketwalkers"):
                self._branch._preparebaskets()
                self._baskets = [None] * len(self._branch._basketwalkers)
                self._ends = (numpy.cumsum(self._branch._basketlengths) // self._branch.dtype.itemsize).tolist()
                self._starts = [0] + self._ends[:-1]

        def __ensurefilled(self, basketindex):
            if self._baskets[basketindex] is None:
                self._baskets[basketindex] = self._branch._adddimensions(self._branch._basket(basketindex))
                if self._baskets[basketindex].dtype != self.dtype:
                    self._baskets[basketindex] = numpy.array(self._baskets[basketindex], dtype=self.dtype)

        def cumsum(self, axis=None, dtype=None, out=None):
            self.__startfill()            
            for i in range(len(self._baskets)):
                self.__ensurefilled(i)
            array = numpy.concatenate(self._baskets)
            return array.cumsum(axis, dtype, out)

        def __getitem__(self, index):
            self.__startfill()

            product = reduce(lambda x, y: x*y, self._branch.itemdims, 1)

            if isinstance(index, slice):
                start, stop, step = self.__normalizeslice(index)
                if start == stop:
                    return self._branch._adddimensions(numpy.empty(0, dtype=self._branch.dtype))

                flatstart = start * product
                flatstop = stop * product
                firststart = None
                firstindex = None
                lastindex = None

                for basketindex, start in enumerate(self._starts):
                    if start <= flatstart and firststart is None:
                        firststart = start
                    if start >= flatstop:
                        break
                    self.__ensurefilled(basketindex)
                    if firstindex is None:
                        firstindex = basketindex
                    lastindex = basketindex

                return numpy.concatenate(self._baskets[firstindex:lastindex + 1])[(flatstart - firststart) // product : (flatstop - firststart) // product : step]
                
            else:
                flatindex = self.__normalize(index, False, 1) * product
                for basketindex, start in enumerate(self._starts):
                    if start <= flatindex < self._ends[basketindex]:
                        self.__ensurefilled(basketindex)
                        break
                return self._baskets[basketindex][(flatindex - start) // product]

    def lazyarray(self, dtype=None):
        """Creates a proxy for an array that gets data on demand.

        Arguments:

            * `dtype` If not `None`, cast the array into a given `dtype` (such as conversion to little endian).
        """
        if dtype is None:
            dtype = self.dtype
        return self.LazyArray(self, dtype)

uproot.rootio.Deserialized.classes[b"TBranch"] = TBranch

class TBranchElement(TBranch):
    """Represents a TBranchElement, a column of data represented an object that has been split.

    All methods and members are the same as TBranch.
    """
    def __init__(self, filewalker, walker):
        walker.startcontext()
        start = walker.index
        vers, bcnt = self._readversion(walker)

        if vers < 9:
            raise NotImplementedError("TBranchElement version too old")

        TBranch.__init__(self, filewalker, walker)

        self.classname = walker.readstring()
        parent = walker.readstring()
        clones = walker.readstring()

        checksum = walker.readfield("!I")
        if vers >= 10:
            classversion = walker.readfield("!H")
        else:
            classversion = walker.readfield("!I")
        identifier, btype, stype, themax = walker.readfields("!iiii")
            
        bcount1 = uproot.rootio.Deserialized._deserialize(filewalker, walker)
        bcount2 = uproot.rootio.Deserialized._deserialize(filewalker, walker)

        self._checkbytecount(walker.index - start, bcnt)

    def array(self, dtype=None, executor=None, block=True):
        """Extracts the whole branch into a Numpy array.

        Individual branches are typically small enough to fit into memory. If this is not your case, consider `tree.iterator(entries)` to load a given number of entries at a time.

        Arguments:

            * `dtype`

               If not `None`, cast the array into a given `dtype` (such as conversion to little endian).
               If an array object, fill that array instead of creating a new one (shape must match).

            * `executor` (same as in `TTree.array`)

              A `concurrent.futures.Executor` that would be used to parallelize the basket loading/decompression.
              If `None`, the process is serial.

            * `block`

              If `True` and parallel processing with an `executor`, return `data, errors` instead of just `data`, where `errors` is a generator of exceptions raised by the parallel threads.
              When you're ready to wait for all threads to finish, evaluate the `errors` generator.
        """
        if hasattr(self, "dtype"):
            return TBranch.array(self, dtype, executor, block)
        else:
            raise NotImplementedError

uproot.rootio.Deserialized.classes[b"TBranchElement"] = TBranchElement

class TLeaf(uproot.core.TNamed):
    """Represents a TLeaf object, which is only used for type and dimensionality information.
    """
    def __init__(self, filewalker, walker):
        walker.startcontext()
        start = walker.index
        vers, bcnt = self._readversion(walker)

        uproot.core.TNamed.__init__(self, filewalker, walker)

        len, etype, offset, hasrange, self.unsigned = walker.readfields("!iii??")
        self.counter = uproot.rootio.Deserialized._deserialize(filewalker, walker)

        self._checkbytecount(walker.index - start, bcnt)

uproot.rootio.Deserialized.classes[b"TLeaf"] = TLeaf

for classname, format, dtype1, dtype2 in [
    ("TLeafO", "!??", "bool", "bool"),
    ("TLeafB", "!bb", "i1", "u1"),
    ("TLeafS", "!hh", ">i2", ">u2"),
    ("TLeafI", "!ii", ">i4", ">u4"),
    ("TLeafL", "!qq", ">i8", ">u8"),
    ("TLeafF", "!ff", ">f4", ">f4"),
    ("TLeafD", "!dd", ">f8", ">f8"),
    ("TLeafC", "!ii", "object", "object"),
    ("TLeafObject", "!ii", "object", "object"),
    ]:
    exec("""
class {0}(TLeaf):
    "Represents a {0} object, which is only used for type and dimensionality information."
    def __init__(self, filewalker, walker):
        walker.startcontext()
        start = walker.index
        vers, bcnt = self._readversion(walker)

        TLeaf.__init__(self, filewalker, walker)

        min, max = walker.readfields("{1}")
        if self.unsigned:
            self.dtype = numpy.dtype("{3}")
        else:
            self.dtype = numpy.dtype("{2}")
        self._speedbumps = False
        
        self._checkbytecount(walker.index - start, bcnt)

uproot.rootio.Deserialized.classes[b"{0}"] = {0}
""".format(classname, format, dtype1, dtype2), globals())

class TLeafElement(TLeaf):
    """Represents a TLeafElement object, which is only used for type and dimensionality information.
    """
    def __init__(self, filewalker, walker):
        walker.startcontext()
        start = walker.index
        vers, bcnt = self._readversion(walker)

        TLeaf.__init__(self, filewalker, walker)

        identifier, ltype = walker.readfields("!ii")

        if ltype == 65:
            self.dtype = numpy.dtype(object)

        elif ltype > 0 and ltype % 20 not in (0, 9, 10, 19):
            # typename = [
            #     "", "Char_t",  "Short_t",  "Int_t",  "Long_t",  "Float_t", "Int_t",    "char*",     "Double_t", "Double32_t",
            #     "", "UChar_t", "UShort_t", "UInt_t", "ULong_t", "UInt_t",  "Long64_t", "ULong64_t", "Bool_t",   "Float16_t"
            #     ][ltype % 20]
            self.dtype = numpy.dtype([
                None, "i1", ">i2", ">i4", ">i8", ">f4", ">i4", "u1",  ">f8",  None,
                None, "u1", ">u2", ">u4", ">u8", ">u4", ">i8", ">u8", "bool", None
                ][ltype % 20])

        elif ltype == -1:  # counter
            self.dtype = numpy.dtype(">i4")

        self._speedbumps = 40 <= ltype < 60

        self._checkbytecount(walker.index - start, bcnt)

uproot.rootio.Deserialized.classes[b"TLeafElement"] = TLeafElement
