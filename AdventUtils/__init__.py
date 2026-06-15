# main library
from .core import Solution
from .grid import Grid, T, N, Coordinate
from .graph import Graph, UnionFind, DirectedGraph
from .utils import Vector, recursive_split, string_multi_replace, quicksort, rref_gf2, find_pivots
from .constants import UP, DOWN, LEFT, RIGHT, UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT, CROSS_DIRECTIONS, ALL_DIRECTIONS

# builtins & utils
import numpy as np
import pandas as pd
import networkx as nx
import heapq
import copy
import re
import scipy
from itertools import combinations, permutations, chain, compress, groupby, product
from functools import partial, cache, wraps
from enum import Enum, auto
from sympy import Matrix
from enum import Enum
from math import prod

# helpers / semantics
from typing import NewType, Callable, TypeVar, Any, TypeAlias, Optional, Union, List, Dict, TypeAlias, Generic, Set, cast, final, overload
from collections import defaultdict, namedtuple, deque
from collections.abc import Mapping, Callable
from pprint import pprint
import inspect

# legacy
import itertools as it 
magnitudevec = Vector.magnitudevec
unitvec = Vector.unitvec
is_coincident = Vector.is_coincident

np.set_printoptions(threshold=np.inf, suppress=True, linewidth=np.inf)
