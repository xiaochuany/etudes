import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import numpy as np
    import polars as pl


@app.cell
def _():
    rng = np.random.default_rng(1)
    return (rng,)


@app.cell
def _():
    N = mo.ui.slider(1000, 10001)
    N
    return (N,)


@app.cell
def _(N, rng):
    xs = rng.standard_normal(size=(N.value))
    ys = rng.choice([0, 1], size=(N.value))
    raw = pl.DataFrame(np.stack([xs, ys], axis=1), schema=list("AB"))
    return (raw,)


@app.cell
def _(raw):
    raw.with_columns(
        pl.first()
        .qcut(quantiles=np.arange(1, 10) * 0.1, include_breaks=True)
        .alias("qcut")
    ).unnest("qcut")
    return


@app.cell
def _(raw):
    (
        raw.with_columns(
            pl.first()
            .cut(breaks=np.quantile(a=raw[:, 0], q=np.arange(1, 10) * 0.1))
            .alias("cut")
        )
        .group_by("cut")
        .agg(pl.mean("B").alias("dr"))
        .sort("cut")
        .plot.line(x="cut", y="dr")
    )
    return


@app.function
def get_bins(raw):
    res = (
        raw.with_columns(
            pl.first()
            .qcut(quantiles=np.arange(1, 10) * 0.1, include_breaks=True)
            .alias("qcut")
        )
        .unnest("qcut")
        .select(pl.col("breakpoint").unique().sort())
        .select(
            pl.col("breakpoint")
            .shift(1, fill_value=float("-inf"))
            .alias("low"),
            pl.col("breakpoint").alias("high"),
        )
        .with_row_index()
    )
    return res


@app.cell
def _(raw):
    bins = get_bins(raw)
    return (bins,)


@app.function
def get_rate(raw, low, high):
    v = (
        raw.filter(pl.first().is_between(pl.lit(low), pl.lit(high)))
        .select(pl.last())
        .mean()
    )
    return v.item()


@app.cell
def _(bins, raw):
    imap = {}
    for d in bins.to_dicts():
        k = d.pop("index")
        imap[k] = d

    while len(imap) >= 2:
        cur, nxt = 0, 1
        iters = len(imap)
        print(iters)
        while nxt < iters:
            low, high = imap[cur].values()
            low_, high_ = imap[nxt].values()
            rate = get_rate(raw, low, high)
            rate_ = get_rate(raw, low_, high_)
            # print(rate, rate_, low, high)
            if rate < rate_:
                imap[nxt]["low"] = imap[cur]["low"]
                imap.pop(cur)
            cur, nxt = nxt, nxt + 1
        _breaks = [
            v.get("low") for v in imap.values() if v.get("low") > float("-inf")
        ]
        _B = (
            raw.with_columns(
                pl.col("A").cut(breaks=_breaks, include_breaks=True).alias("_cut")
            )
            .unnest("_cut")
            .group_by("breakpoint")
            .agg(pl.mean("B"))
            .sort("breakpoint")
            .get_column("B")
        )
        # print("checking monotonicity")
        # print(_B)
        # print(imap)
        if _B.is_close(_B.sort(descending=True)).all():
            break
        else:
            imap = dict(enumerate(imap.values()))
    return (imap,)


@app.cell
def _(bins, imap, raw):
    def main():
        imap_l = bins.drop("index").to_dicts()

        while len(imap) >= 2:
            cur, nxt = 0, 1
            iters = len(imap)
            print(iters)
            while nxt < iters:
                low, high = imap[cur].values()
                low_, high_ = imap[nxt].values()
                rate = get_rate(raw, low, high)
                rate_ = get_rate(raw, low_, high_)
                # print(rate, rate_, low, high)
                if rate < rate_:
                    imap[nxt]["low"] = imap[cur]["low"]
                    imap.pop(cur)
                cur, nxt = nxt, nxt + 1
            _breaks = [
                v.get("low") for v in imap.values() if v.get("low") > float("-inf")
            ]
            _B = (
                raw.with_columns(
                    pl.col("A").cut(breaks=_breaks, include_breaks=True).alias("_cut")
                )
                .unnest("_cut")
                .group_by("breakpoint")
                .agg(pl.mean("B"))
                .sort("breakpoint")
                .get_column("B")
            )
            # print("checking monotonicity")
            # print(_B)
            # print(imap)
            if _B.is_close(_B.sort(descending=True)).all():
                break
            else:
                imap = dict(enumerate(imap.values()))
    return


@app.cell
def _(breaks, raw):
    raw.with_columns(
        pl.col("A").cut(breaks=breaks, include_breaks=True).alias("_cut")
    ).unnest("_cut").group_by("breakpoint").agg(pl.mean("B")).sort("breakpoint")
    return


@app.cell
def _(imap):
    breaks = [v.get("low") for v in imap.values() if v.get("low") > float("-inf")]
    return (breaks,)


@app.cell
def _(imap):
    imap
    return


@app.function
def pava(x, constraint=lambda a, b: a[0] / a[1] <= b[0] / b[1]):
    """x : list of pairs of counts (total, default)"""
    n = len(x)
    active_pools = [[i] for i in range(n)]
    active_values = list(np.asarray(x))

    i = 0
    while i < len(active_pools) - 1:
        if not constraint(active_values[i], active_values[i + 1]):
            # Violation found, merge pools
            active_pools[i].extend(active_pools[i + 1])
            del active_pools[i + 1]
            active_values[i] = active_values[i] + active_values[i + 1]
            del active_values[i + 1]

            # Step back to check for new violations with the merged pool
            if i > 0:
                i -= 1
        else:
            i += 1

    return active_pools


@app.function
def pavai(x, constraint=lambda a, b: a[0] / a[1] <= b[0] / b[1]):
    """
    x: list of pairs of counts, e.g., [(numerator, denominator), ...]
    
    This implementation uses a stack-based approach. It is also O(n) but
    is often cleaner and more intuitive than a linked list.
    """
    if not x:
        return []

    # The stack will store tuples of (value, indices) for each active pool.
    stack = []
    
    # Process each data point one by one.
    for i, val in enumerate(x):
        # The new data point starts as its own pool.
        current_value = np.asarray(val)
        current_indices = [i]
        
        # --- Backwards Merging ---
        # While the stack is not empty and the top pool violates the constraint
        # with the current pool, merge them.
        while stack and not constraint(stack[-1][0], current_value):
            # Pop the last pool from the stack.
            prev_value, prev_indices = stack.pop()
            
            # Merge it into the current pool.
            current_value += prev_value
            current_indices = prev_indices + current_indices # Prepend old indices
        
        # Now that all violations are resolved, push the new pool onto the stack.
        stack.append((current_value, current_indices))

    # --- Finalization: Unpack the stack into the final list of pools ---
    final_pools = [indices for value, indices in stack]
        
    return final_pools


@app.cell
def _():
    pava([[5, 100], [8, 90], [15, 120], [12, 100], [25, 150]])
    return


@app.cell
def _():
    pavai([[5, 100], [8, 90], [15, 120], [12, 100], [25, 150]])
    return


@app.cell
def _():
    mo.md(
        r"""
    ## correctness

    we can decompose the state into two alternating phase

    - either forward merge happens and backtracks and merges until monotonicity is restored
    - or forward merge does not happen and index advances by 1

    index advancing happens at most n times because the number of indices ahead of the current index stays unchanged during the merge and backtracks phase. everytime we advances index there are less places for the advancement to happen.

    let $b_i$ denote the number of index backtracks in the i-th round of phase 1 (forward merge followed by a number of backward merges). we bound 

    $$
    \sum_{i}^r b_i  =  r + \sum_{i=1}^r (b_i-1) \le \sharp\{forward merge\}+\sharp\{backward merge\} \le \sharp\{merge\}\le n
    $$


    the bulk of the work is done by the merges which are O(1) operations. there are at most n merges because the total number of merges cannot be larger than the number of data points.
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
