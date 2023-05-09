import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def set_plot_defaults():
    """Set defaults formatting for consistency across all plots """

    # set plot style
    sns.set_style("whitegrid")

    palette = sns.color_palette("viridis_r", 15)

    base_color = palette[-4]

    # red
    base_highlight_intense = sns.color_palette("viridis_r", 15)[0]
    base_highlight = sns.color_palette("viridis_r", 15)[1]

    # yellow
    base_complementary = palette[0]

    # grey - used for comparison to all flights
    base_grey = 'lightgrey'

    base_color_arr = palette[-6]
    base_color_dep = palette[-9]

    # up and down arrows for growth indicators
    symbols = [u'\u25BC', u'\u25B2']

    small_size = 8
    medium_size = 10
    bigger_size = 12

    plt.rc('font', size=small_size, weight='ultralight', family='sans-serif')  # controls default text sizes and font
    plt.rc('axes', titlesize=bigger_size, titlecolor='black', titleweight='bold', labelsize=medium_size,
           labelcolor='black', labelweight='ultralight')  # axes settings
    plt.rc('xtick', labelsize=small_size)  # fontsize of the ytick labels
    plt.rc('ytick', labelsize=small_size)  # fontsize of the xtick labels
    plt.rc('legend', fontsize=small_size)  # legend fontsize
    plt.rc('figure', titlesize=bigger_size, titleweight="bold", figsize=[8, 4])  # fontsize of the figure title

    return base_color, base_highlight_intense, base_highlight, base_complementary, base_grey, base_color_arr, base_color_dep, symbols


# set default plot formatting
BASE_COLOR, BASE_HIGHLIGHT_INTENSE, BASE_HIGHLIGHT, BASE_COMPLEMENTARY, BASE_GREY, BASE_COLOR_ARR, BASE_COLOR_DEP, SYMBOLS = set_plot_defaults()


def improve_yticks(maxvalue, bins=10):
    """Dynamically set the binsize to control space between annotation and bars"""

    binsize = maxvalue / bins
    if maxvalue > 4000000:
        ind = 'mil'
        div = 1000000
        binsize = 500000
        yticks = np.arange(0, maxvalue + binsize, binsize)
        ylabels = ['{:1.1f}'.format(tick / div) + ind for tick in yticks]
    elif maxvalue > 1000000:
        ind = 'mil'
        div = 1000000
        binsize = 200000
        yticks = np.arange(0, maxvalue + binsize, binsize)
        ylabels = ['{:1.1f}'.format(tick / div) + ind for tick in yticks]
    elif maxvalue > 10000:
        ind = 'k'
        div = 1000
        yticks = np.arange(0, maxvalue + binsize, binsize)
        ylabels = ['{:1.0f}'.format(tick / div) + ind for tick in yticks]
    else:
        ind = ''
        div = 1
        yticks = np.arange(0, maxvalue + binsize, binsize)
        ylabels = ['{:1.0f}'.format(tick / div) + ind for tick in yticks]

    return yticks, ylabels, binsize


def plot_period_side_by_side(df, col, annotate=True, title='month', rotate=False, sharey=False, base_grey=BASE_GREY,
                             base_color=BASE_COLOR, order=None):
    """ 2 bar plots side by side for a certain category: plot 1 showing only delays, plot 2 all flights"""

    flight_total = df.groupby(col)['total_flights'].mean().sum()
    delay_total = df.groupby(col)['delayed'].mean().sum()

    # Customize annotation
    if rotate:
        plt.figure(figsize=[14, 4])
        weight = 'ultralight'
        rotation = 90
        color = 'black'
        xytext = (0, 8)
        size = 6
    else:
        plt.figure(figsize=[14, 4])
        weight = 'ultralight'
        rotation = None
        color = 'black'
        xytext = (0, 3)
        size = 8

    # PLOT 2: visualize distribution of ALL flights per selected period
    ax1 = plt.subplot(1, 2, 2)
    sns.barplot(data=df, x=col, y='total_flights', color=base_grey, label='All flights', errorbar=None, errwidth=1,
                order=order)

    # improve yticks
    maxvalue = df.groupby(col)['total_flights'].mean().max()
    yticks, ylabels, binsize = improve_yticks(maxvalue)
    plt.yticks(yticks, ylabels)

    # annotate bars with % of total flights
    if annotate:
        for p in ax1.patches:
            ax1.annotate("{:.1%}".format(p.get_height() / flight_total),
                         (p.get_x() + p.get_width() / 2.,
                          p.get_height()),
                         ha='center', va='center',
                         xytext=xytext,
                         textcoords='offset points',
                         size=7,
                         weight=weight,
                         color='black',
                         rotation=rotation)

    plt.title('Average total flights {}'.format(title))
    plt.xlabel(title)
    plt.ylabel('')

    # PLOT 1: visualize distribution of DELAYED flights per selected period

    # control stacking
    if sharey:
        ax2 = plt.subplot(1, 2, 1, sharey=ax1, sharex=ax1)
    else:
        ax2 = plt.subplot(1, 2, 1, sharex=ax1)

    sns.barplot(data=df, x=col, y='delayed', color=base_color, label='Delayed flights', errorbar=None, errwidth=1,
                order=order)

    if not sharey:
        # improve yticks
        maxvalue = df.groupby(col)['delayed'].mean().max()
        yticks, ylabels, binsize = improve_yticks(maxvalue)
        plt.yticks(yticks, ylabels)

    # annote bars with % of total flights
    if annotate:
        for p in ax2.patches:
            ax2.annotate("{:.1%}".format(p.get_height() / delay_total),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=xytext,
                         textcoords='offset points',
                         size=7,
                         weight=weight,
                         color=color,
                         rotation=rotation)

    plt.title('Average delayed flights per {}'.format(title))
    plt.xlabel(title)
    plt.ylabel('Number of flights')

    plt.suptitle('Distribution of flights per {}'.format(title))
    plt.tight_layout()
    plt.show()


def plot_period_stacked(df, col, figsize=None, base_grey=BASE_GREY, base_color=BASE_COLOR, annotate=True, title='month',
                        rotate=False):
    """Plot proportion total flights vs delayed flights per category

       Print % of total flights at the top of each bar, example

       % of all flights in January / all flights
       % of delayed flights in January / all flights
    """

    flight_total = df.groupby(col)['total_flights'].mean().sum()

    if figsize:
        plt.figure(figsize=figsize)

        # Customize annotation
    if rotate:
        weight = 'ultralight'
        rotation = 90
        color = 'black'
        xytext = (0, 8)
        size = 6
    else:
        weight = 'ultralight'
        rotation = None
        color = 'black'
        xytext = (0, 3)
        size = 8

    ax1 = sns.barplot(data=df, x=col, y='total_flights', color=base_grey, label='All flights', errorbar=None,
                      errwidth=1)
    ax2 = sns.barplot(data=df, x=col, y='delayed', color=base_color, label='Delayed flights', errorbar=None, errwidth=1,
                      width=0.6, edgecolor=base_color)

    #   improve yticks
    maxvalue = df.groupby(col)['total_flights'].mean().max()
    yticks, ylabels, binsize = improve_yticks(maxvalue)
    plt.yticks(yticks, ylabels)

    #  annotate bars with % of total flights
    if annotate:
        for p in ax2.patches:
            ax2.annotate("{:.1%}".format(p.get_height() / flight_total),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=xytext,
                         textcoords='offset points',
                         size=7,
                         weight=weight,
                         color=color,
                         rotation=rotation)

    plt.title('Average total flights for {}'.format(title))
    plt.xlabel(title)
    plt.ylabel('Number of flights')

    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def flights_by_cat(df, col, title='Origin airports with most delayed flights', topn=20, base_color=BASE_COLOR,
                   base_highlight=BASE_HIGHLIGHT_INTENSE,
                   lookup=False, df_lookup=None, df_lookup_field=None):
    """ Count plot - first 3 highest bars are highlighted """

    # calculate top category and order of bar charts
    top = df[col].value_counts(ascending=False)
    top_order = top.index[:topn]

    # replace index key with key and description
    if lookup:
        top.index = top.index + ':' + df_lookup.loc[top.index][df_lookup_field]

    clrs = [base_color if i >= 3 else base_highlight for i in np.arange(0, topn + 1, 1)]

    ax = sns.countplot(data=df, y=col, order=top_order, palette=clrs, orient='h', width=0.6)

    plt.title('{} '.format(title), weight='bold')
    plt.xlabel(title)
    plt.ylabel(col)

    # improve xticks and labels      
    ticks, xlabels, binsize = improve_yticks(top[0])
    plt.xticks(ticks, xlabels)

    #   calculate and print % on the top of each bar
    ticks = ax.get_yticks()
    new_labels = []
    locs, labels = plt.yticks()
    for loc, label in zip(locs, labels):
        count = top[loc]
        perc = '{:0.1f}%'.format((count / top.sum()) * 100)
        # print only the first characters of xlabel descriptions
        text = top.index[loc][:40]
        new_labels.append(text)
        plt.text(count + (0.2 * binsize), loc, perc, ha='center', va='center', color='black', fontsize=6,
                 weight='ultralight')
    plt.yticks(ticks, new_labels, fontsize=6, weight='ultralight')

    plt.tight_layout()
    plt.show()


def plot_categories(df, annotate=True, title='month', rotate=False, topn=20, figsize=(12, 6), orient='v',
                    base_color=BASE_COLOR, base_grey=BASE_GREY):
    ontime_total = df['on_time'].sum()
    delay_total = df['delayed'].sum()
    grand_total = ontime_total + delay_total

    # avoid do print categories with low amount of flights
    df = df.loc[df['delayed'] >= 10000]

    df = df[:topn]

    plt.figure(figsize=figsize)
    weight = 'ultralight'
    color = 'black'
    xytext = (0, 3)
    size = 8

    # Customize annotation
    if rotate:
        rotation = 90
        xytext = (0, 2)
    else:
        rotation = None
        xytext = (0, 3)

    if orient == 'v':
        ax1 = sns.barplot(data=df, y=df.index, x='on_time', color=base_grey,
                          label='On-time flights (% on-time / all flights)', errorbar=None, errwidth=1)
        ax2 = sns.barplot(data=df, y=df.index, x='delayed', color=base_color,
                          label='Delayed flights (% delay / on-time)', errorbar=None, errwidth=1, width=0.6,
                          edgecolor=base_color)
        ticks = ax1.get_yticks()
        locs, labels = plt.yticks()
    else:
        ax1 = sns.barplot(data=df, x=df.index, y='on_time', color=base_grey,
                          label='On-time flights (% on-time / all flights)', errorbar=None, errwidth=1)
        ax2 = sns.barplot(data=df, x=df.index, y='delayed', color=base_color,
                          label='Delayed flights (% delay / on-time)', errorbar=None, errwidth=1, width=0.6,
                          edgecolor=base_color)
        ticks = ax1.get_xticks()
        locs, labels = plt.xticks()

    #   improve yticks
    maxvalue = df['on_time'].max()
    yticks, ylabels, binsize = improve_yticks(maxvalue)

    #   print only the first 20 characters of the categorical variable description
    new_labels = []
    for loc, label in zip(locs, labels):
        text = df.index[loc][:30]
        new_labels.append(text)

    if orient == 'v':
        plt.yticks(ticks, new_labels, fontsize=8, weight='ultralight')
        plt.ylabel(title)
        plt.xlabel('Number of flights')
        plt.xticks(yticks, ylabels)
    else:
        plt.xticks(ticks, new_labels, rotation=90, fontsize=8, weight='ultralight')
        plt.ylabel(title)
        plt.xlabel('Number of flights')
        plt.yticks(yticks, ylabels)

    # annote bars with % proportion, doing this way gives flexibility we an print proportion of one bar another
    grand = []

    # print text outside the bar, determine gap between bar and text dynamically based on binsize
    if binsize >= 500000:
        gap = 0.5 * binsize
    if binsize >= 200000:
        gap = 0.15 * binsize
    else:
        gap = 0.15 * binsize

    for i, p in enumerate(ax2.patches):
        prop = None
        # there are 2 bars for each feature. those with index 0-19 are the onetime bards, and 20-39 are the delay bars   
        if i >= len(df):
            # this is for smaller delay bars
            index = i - len(df)

            # print text inside the bar
            gap = -abs(gap)

            color = 'white'
            weight = 'bold'
            size = 6

            if orient == 'v':
                xytext = (0, 6)
                val = p.get_width() / grand_total
            else:
                xytext = (0, -8)
                val = p.get_height() / grand_total

            # calculate proportion of delay / on_time
            val = val / grand[index]
        else:
            # logic for the biggest bar, in this case ontime
            index = i

            gap = abs(gap)
            color = 'black'
            weight = 'ultralight'
            size = 6

            if orient == 'v':
                val = p.get_width() / grand_total
                #                 space = len(str(val))+3
                xytext = (0, 6)
            elif rotate:
                xytext = (0, 8)
                val = p.get_height() / grand_total
            else:
                xytext = (0, 3)
                val = p.get_height() / grand_total

            # save proportion of on_time bar to reuse for proportion calculations in delay bars
            grand.append(val)

        if orient == 'v':
            ax2.annotate("{:.2%}".format(val),
                         (p.get_x() + p.get_width() + gap, p.get_y() + 0.6),
                         ha='center', va='center',
                         xytext=xytext,
                         textcoords='offset points',
                         size=size,
                         weight=weight,
                         rotation=rotation,
                         color=color)

        else:
            ax2.annotate("{:.2%}".format(val),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=xytext,
                         textcoords='offset points',
                         size=size,
                         weight=weight,
                         rotation=rotation,
                         color=color)

    plt.title('DELAYED vs ON-TIME flights by {}'.format(title))
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', title='Flight Status')
    plt.tight_layout()
    plt.show()


def cat_heatmap(df, reason, center=0):
    """ heat map with standard formatting """
    g = sns.heatmap(df, center=center, cmap='Spectral', linewidths=0.003, linecolor='lightgrey', square=True,
                    mask=df < 1, annot=True, fmt=".0f",
                    cbar_kws={"orientation": "vertical", "pad": 0.03, "shrink": 0.5})

    # put xlabels on top
    plt.title('{}'.format(reason.upper()))
    plt.xlabel('Origin Airport')
    plt.ylabel('Carrier')
