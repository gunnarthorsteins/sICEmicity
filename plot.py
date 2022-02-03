import matplotlib.pyplot as plt
import pandas as pd


def plot(df: pd.DataFrame):
    plt.scatter(df.Lengd, df.Breidd, s=df.ML * 10, c=df.Datetime, edgecolors='k')
    plt.savefig('plots/figure.png', dpi=200)