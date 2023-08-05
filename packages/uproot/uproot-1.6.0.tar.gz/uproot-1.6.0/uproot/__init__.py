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

# load all classes into uproot.rootio.Deserialized.classes
import uproot.rootio
import uproot.core
import uproot.tree

del uproot

def open(path, memmap=True):
    """Opens a single file for reading.

    Arguments:

        * `path`

          The name of the file, possibly a URL for XRootD.

        * `memmap` (same as in `uproot.iterator`)

          If `True`, load local files as memory maps. If `False`, load normally.
          The advantage of memory maps is that parallel reads only require one file handle, and random access (of which there is a *lot* in ROOT) is more efficient.
          The advantage of normal files is that memory maps sometimes load more data from disk than intended, which might (?) be a performance issue for slow disks.
    """
    try:
        from urlparse import urlparse
    except ImportError:
        from urllib.parse import urlparse
    import uproot.rootio

    parsed = urlparse(path)
    if parsed.scheme == "file" or parsed.scheme == b"file" or parsed.scheme == "" or parsed.scheme == b"":
        path = parsed.netloc + parsed.path
        if memmap:
            import uproot._walker.arraywalker
            return uproot.rootio.TFile(uproot._walker.arraywalker.ArrayWalker.memmap(path))
        else:
            import uproot._walker.localfilewalker
            return uproot.rootio.TFile(uproot._walker.localfilewalker.LocalFileWalker(path))

    elif parsed.scheme == "root" or parsed.scheme == b"root":
        return xrootd(path)

    else:
        raise ValueError("URI scheme not recognized: {0}".format(path))

def xrootd(path):
    """Opens a single remote file for reading.

    Although `uproot.open` will use XRootD when it encounters a URL, this function *always* invokes XRootD.
    """
    import uproot._walker.xrootdwalker
    import uproot.rootio
    return uproot.rootio.TFile(uproot._walker.xrootdwalker.XRootDWalker(path))

def iterator(entries, path, treepath, branchdtypes=lambda branch: getattr(branch, "dtype", None), memmap=True, executor=None, outputtype=dict, reportentries=False):
    """Iterates over a collection of files, a fixed number of entries at a time (even across the gap between files).

    Use this function when you have a huge dataset, too large to load into memory, spread across many files. Example use:

        for px, py in uproot.iterator(10000, "/bigdisk/mydata*.root", "events", ["px", "py"], outputtype=tuple):
            do_something(sqrt(px**2 + py**2))

    Arguments:

        * `entries` *(required)*

          If a positive integer, the number of entries to yield in each step of iteration.
          
        * `path` *(required)*

          If a single string, the name of the file, possibly a URL for XRootD.
          If an iterable, a set of names or URLs.
          Local files can be glob patterns (`mydata*.root`).
          After expansion, paths will be traversed in *sorted* order. This is to ensure that entry numbers for the same file set have the same meaning from run to run.

        * `treepath` *(required)*

          A string describing the path through TDirectories (using '/' and ';' conventions) to the TTree of interest. Must be the same in all files.

        * `branchdtypes` (same as in `TTree.iterator`)

          If a single string, the string names the only branch to load.
          If an iterable of strings, all of these are loaded (in the specified order).
          If a dict of `{name: dtype}`, load the specified branch names and cast them into a given `dtype` (such as conversion to little endian).
          If a function from branch names to `dtype` or `None`, load the branches into the given `dtypes` and don't load the branches mapped to `None`.

        * `memmap` (same as in `uproot.open`)

          If `True`, load local files as memory maps. If `False`, load normally.
          The advantage of memory maps is that parallel reads only require one file handle, and random access (of which there is a *lot* in ROOT) is more efficient.
          The advantage of normal files is that memory maps sometimes load more data from disk than intended, which might (?) be a performance issue for slow disks.

        * `executor` (same as in `TTree.iterator`)

          A `concurrent.futures.Executor` that would be used to parallelize the basket loading/decompression.
          If `None`, the process is serial.

        * `outputtype` (same as in `TTree.iterator`)

          Constructor for the objects to yield in the iterator. Good choices include `dict`, `tuple`, `namedtuple`, `list`.

        * `reportentries`

          If `True`, yield `(entrystart, entryend, data)` instead of just `data`. Intended as a convenience or cross-check for analysis.
          These are not entry numbers in any one file, they're global numbers for the whole set of files (much like TChain in ROOT).
    """
    import sys
    import glob
    import os.path
    from collections import namedtuple
    try:
        from collections import OrderedDict
    except ImportError:
        class OrderedDict(dict):
            def __init__(self, pairs):
                pairs = list(pairs)
                self.__order = [k for k, v in pairs]
                super(OrderedDict, self).__init__(pairs)
            def keys(self):
                return self.__order
            def values(self):
                return [self[k] for k in self.__order]
            def items(self):
                return [(k, self[k]) for k in self.__order]
            def __setitem__(self, name, value):
                if name not in self.__order:
                    self.__order.append(name)
                super(OrderedDict, self).__setitem__(name, value)
            def __delitem__(self, name):
                if name in self.__order:
                    self.__order.remove(name)
                super(OrderedDict, self).__delitem__(name)
            def __repr__(self):
                return "OrderedDict([{0}])".format(", ".join("({0}, {1})".format(repr(k), repr(v)) for k, v in self.items()))
    try:
        from urlparse import urlparse
    except ImportError:
        from urllib.parse import urlparse
    import numpy
    import uproot.tree

    if hasattr(path, "decode"):
        path = path.decode("ascii")

    def explode(x):
        parsed = urlparse(x)
        if parsed.scheme == "file" or parsed.scheme == "":
            return sorted(glob.glob(os.path.expanduser(parsed.netloc + parsed.path)))
        else:
            return [x]

    if (sys.version_info[0] <= 2 and isinstance(path, unicode)) or \
       (sys.version_info[0] > 2 and isinstance(path, str)):
        paths = explode(path)
    else:
        paths = [y for x in path for y in explode(x)]

    if not isinstance(entries, int) or entries < 1:
        raise ValueError("number of entries per iteration must be an integer, at least 1")

    oldpath = None
    oldtoget = None

    holdover = None
    holdoverentries = 0

    outerstart = 0
    outerend = 0

    for path in paths:
        tree = open(path, memmap=memmap)[treepath]

        toget = list(uproot.tree.TTree._normalizeselection(branchdtypes, tree.allbranches))

        newtoget = OrderedDict((b.name, d) for b, d in toget)
        if oldtoget is not None:
            for key in set(oldtoget.keys()).union(set(newtoget.keys())):
                if key not in newtoget:
                    raise ValueError("branch {0} cannot be found in {1}, but it was in {2}".format(repr(key), repr(path), repr(oldpath)))

                if key not in oldtoget:
                    del newtoget[key]
                elif newtoget[key] != newtoget[key]:
                    raise ValueError("branch {0} is a {1} in {2}, but it was a {3} in {4}".format(repr(key), newtoget[key], repr(path), oldtoget[key], repr(oldpath)))

        oldpath = path
        oldtoget = newtoget

        if outputtype == namedtuple:
            outputtype = namedtuple("Arrays", [branch.name.decode("ascii") for branch, dtype in toget])

        def output(arrays, outerstart, outerend):
            if outputtype == dict or outputtype == OrderedDict:
                out = arrays
            elif issubclass(outputtype, dict):
                out = outputtype(arrays.items())
            elif outputtype == tuple or outputtype == list:
                out = outputtype(arrays.values())
            else:
                out = outputtype(*arrays.values())

            if reportentries:
                return outerstart, outerend, out
            else:
                return out

        def ranges():
            x = 0
            while x < tree.numentries:
                if x == 0 and holdoverentries != 0:
                    nextx = x + (entries - holdoverentries)
                    yield (x, nextx)
                    x = nextx
                else:
                    yield (x, x + entries)
                    x += entries

        for entrystart, entryend, arrays in tree.iterator(ranges(), newtoget, executor=executor, outputtype=OrderedDict, reportentries=True):
            thisentries = entryend - entrystart

            if holdover is not None:
                arrays = OrderedDict((name, numpy.concatenate((oldarray, arrays[name]))) for name, oldarray in holdover.items())
                thisentries += holdoverentries
                holdover = None
                holdoverentries = 0

            if thisentries < entries:
                holdover = arrays
                holdoverentries = thisentries

            else:
                yield output(arrays, outerstart, outerstart + thisentries)
                outerstart = outerend = outerstart + thisentries

    if holdover is not None:
        yield output(arrays, outerstart, outerstart + thisentries)
