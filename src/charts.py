import matplotlib.pyplot as plt


def _format_axis(ax, xlabel: str, ylabel: str, title: str):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)


def build_revenue_chart(df):
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(df["month"], df["revenue"])
    _format_axis(ax, "Month", "Revenue", "Revenue by Month")
    fig.tight_layout()
    return fig


def build_ebitda_chart(df):
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(df["month"], df["ebitda"])
    _format_axis(ax, "Month", "EBITDA", "EBITDA by Month")
    fig.tight_layout()
    return fig


def build_margin_chart(df):
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    ax.plot(df["month"], df["ebitda_margin_pct"])
    _format_axis(ax, "Month", "Margin %", "EBITDA Margin")
    fig.tight_layout()
    return fig


def build_headcount_chart(df):
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    ax.plot(df["month"], df["headcount"])
    _format_axis(ax, "Month", "Headcount", "Headcount Trend")
    fig.tight_layout()
    return fig
