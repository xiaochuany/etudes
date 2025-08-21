import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import numpy as np
    import polars as pl  # Initialization code that runs before all other cells


@app.cell
def _():
    rng = np.random.default_rng(1)
    return (rng,)


@app.cell
def _():
    N = mo.ui.slider(1000, 10000)
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
    np.quantile(a=raw[:, 0], q=np.arange(1, 10) * 0.1)
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
