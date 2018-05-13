from typing import List, Tuple, Dict
from math import ceil, inf
from heapq import heapify, heappop, heappushpop

def solve(q: List[int], u: int) -> Tuple[List[Dict[int, int]], List[int]]:
  """The general case."""
  # preconditions: q is monotonically nonincreasing; all(qv > 0 for qv in q); u > 0
  F = [] # type: List[Dict(int, int)]
  p = [] # type: List[int]
  base = 0
  while base < len(q):
      f, pf = oneForm(q[base : base + min(len(q), u)], u)
      F.append(dict(zip((base + i for i in range(len(f))), f)))
      p.append(pf)
      base += len(f)
  return F, p

def oneForm(q: List[int], u: int):
    """Given q and U, return (f, p)."""
    # precondition: len(q) <= u and all(qv > 0 for qv in q)
    def pVal(qv: int, fv: int) -> Tuple[List[int], int]:
        return inf if fv == 0 else ceil(qv / fv)

    while True:
        idealP = sum(q) / u
        p = int(ceil(idealP))
        f = [float(qv // p) for qv in q]
        if p == idealP and all(qv % p == 0 for qv in q):
            break # perfect; we're done

        uncommitted = [] # type: List[int]
        pvHeap = list(zip((-pVal(qv, fv) for qv, fv in zip(q, f)), range(len(q))))
        heapify(pvHeap)
        p, v = heappop(pvHeap)
        for _ in range(u - int(sum(f))):
            uncommitted.append(v)
            f[v] += 1
            pNew, v = heappushpop(pvHeap, (-pVal(q[v], f[v]), v))
            if pNew > p:
                uncommitted = []
                p = pNew
        # Discard uncommitted leftovers.
        for v in uncommitted:
            f[v] -= 1
        if p != -inf:
            p = int(-p)
            break # for now, we'll call it good if it's feasible
        # Discard zeroes in f and corresponding q
        # TODO: add code to test our belief that the zeroes, if present, are
        # all at the end of f. Monotonicity of q *should* imply that, but...
        q, f = zip(*[x for x in zip(q, f) if x[1] != 0])

    return ([int(fv) for fv in f], p)
