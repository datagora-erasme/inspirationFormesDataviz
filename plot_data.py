import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_kde():

    plt.figure(1)
    sns.kdeplot(
        data=new_df,
        x="MM-DD",
        hue='year',
        palette="crest",
    )
    plt.title("Densité des arrivées au lab")

def plot_hist_4():
    plt.figure(2)
    sns.histplot(
        data=new_df,
        x='MM-DD',
        hue='year',
        bins=4
    )
    plt.title("Histogramme des arrivées au lab (4 bins)")

def plot_hist_16():
    plt.figure(3)
    sns.histplot(
        data=new_df,
        x='MM-DD',
        hue='year',
        bins=16
    )
    plt.title("Histogramme des arrivées au lab (16 bins)")

def plot_ridge():

    #initialize the FacetGrid object
    pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
    g = sns.FacetGrid(new_df, row="year", hue="year", aspect=15, height=0.5, palette=pal)
    # Draw the densities in a few steps
    g.map(sns.kdeplot, "MM-DD",
        bw_adjust=.5, clip_on=False,
        fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "MM-DD", clip_on=False, color="w", lw=2, bw_adjust=.5)

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)


    g.map(label, "MM-DD")

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)

if __name__ == '__main__':
    new_df = pd.read_csv("processed_data.csv")
    new_df["MM-DD"] = pd.to_datetime(new_df["MM-DD"])

    plot_kde()
    plot_hist_4()
    plot_hist_16()
    plot_ridge()
    plt.show()
