"""Portfolio figures generated only from the current client-report tables."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def render():
    source = Path("reports/client")
    target = Path("reports/portfolio"); target.mkdir(exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
                        "axes.spines.top":False, "axes.spines.right":False})
    yearly = pd.read_csv(source / "yearly.csv")
    fig, axes = plt.subplots(1,2,figsize=(10,3.8),layout="constrained")
    axes[0].bar(yearly.year.astype(str), yearly.revenue/1000, color="#087f83")
    axes[0].set(ylabel="Revenue ($ thousands)", title="Revenue by year")
    for i,r in yearly.iterrows(): axes[0].text(i,r.revenue/1000+12,f"{r.revenue/1000:.0f}",ha="center")
    axes[0].set_ylim(0,850)
    axes[1].plot(yearly.year.astype(str),yearly.margin*100, marker="o",color="#376480",linewidth=2.5)
    axes[1].set(ylabel="Weighted profit margin (%)",title="Profitability by year",ylim=(0,16))
    for i,r in yearly.iterrows(): axes[1].text(i,r.margin*100+.55,f"{r.margin*100:.2f}%",ha="center")
    for ax in axes: ax.grid(axis="y",alpha=.15); ax.set_axisbelow(True)
    fig.savefig(target / "revenue_and_margin.png",dpi=180); plt.close(fig)
    sub = pd.read_csv(source / "subcategories.csv").query("profit < 0").sort_values("profit")
    fig,ax=plt.subplots(figsize=(10,3),layout="constrained")
    ax.barh(sub.sub_category, -sub.profit,color="#b6604d")
    for i,r in enumerate(sub.itertuples()): ax.text(-r.profit+220,i,f"${-r.profit:,.0f}",va="center")
    ax.set(xlabel="Historical loss magnitude ($)",xlim=(0,22000));ax.invert_yaxis()
    ax.grid(axis="x",alpha=.15);ax.set_axisbelow(True)
    fig.savefig(target / "loss_making_categories.png",dpi=180);plt.close(fig)


if __name__ == "__main__": render()
