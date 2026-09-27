import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar 
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
# print(df[(df['value'] <= df['value'].quantile(0.025)) | (df['value'] >= df['value'].quantile(0.975))])
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig , ax = plt.subplots(figsize=(20,5))
    ax.plot( df)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_xticks(['2016-07-01','2017-01-01','2017-07-01','2018-01-01','2018-07-01','2019-01-01','2019-07-01','2020-01-01',], ['2016-07','2017-01','2017-07','2018-01','2018-07','2019-01','2019-07','2020-01',])
    # how to automate this (may be convert to datatime then...)


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_copy = df.copy()
    df_copy['Years'] = pd.DatetimeIndex(df_copy.index).year
    df_copy['Months'] = pd.DatetimeIndex(df_copy.index).month
    df_bar = df_copy.groupby(['Years', 'Months']).mean()
    # print(df_bar.info())
    # Draw bar plot
    fig, ax = plt.subplots()
    # palette = sns.color_palette("Set3", 10)
    # طرق لجعل الأشهر بالأسماء لا الأرقام
    # تغيير عمود الشهور من الأرقام إلى الأسماء بطريقين
        # DatetimeIndex

    df_copy['Months'] = pd.DatetimeIndex(df_copy.index).month_name()
    df_bar = df_copy.groupby(['Years', 'Months']).mean()
    # print(df_copy)
    ax1= sns.barplot(df_bar, x='Years', y='value', hue='Months',hue_order=list(calendar.month_name[1:]) ,ax=ax, palette='muted')
    plt.ylabel("Average Page Views")
    # num_bars = len(ax1.containers[0])
    # print(f"Number of bars: {num_bars}")

        # mapping


    # تعديل label of legend
    '''
    ax = sns.barplot(df_bar, x='Years', y='value', hue='Months', palette='bright')
    print(df_bar)
    ax.set_ylabel('Average Page Views')
    # ax.legend(list(calendar.month_name)[1:])
    handles, lables = ax.get_legend_handles_labels()
    title = ax.get_legend().get_title().get_text()
    # print('_'*20, title)
    new_labels = list(calendar.month_name)[1:]
    plt.legend(
        handles=handles, 
        title=title, 
        labels=new_labels
    )

    # حل رابع محتمل
    # هل يمكن إعطاء هذه الخاصية شيئا ليس في العمود المعطى لأمها  hue_order
    # أمها: hue
    '''
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    # print(df_box) # أعاد فهرسة السطور مع حفظ الفهرس القديمة
    # print(df_box.info())
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # print(df_box)

    # Draw box plots (using Seaborn)
    fig , ax = plt.subplots(1,2,figsize=(12,6))
    # sns.boxplot(df_box , ax=ax[0]) # إذا أعطيته الجدول كاملا رسم لكل عمود مربعا 
    plt.tight_layout(pad=3)

    sns.boxplot(df_box, x='year', hue='year', y='value', palette='deep' , legend=False, ax=ax[0])
    # print(list(calendar.month_abbr))
    ax[0].set_xlabel('Year')
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_ylabel('Page Views')
    
    
    sns.boxplot(df_box, x='month', hue='month', y='value', palette='husl', legend=False, order=list(calendar.month_abbr[1:]), ax=ax[1])
    ax[1].set_xlabel('Month')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_ylabel('Page Views')


    # plt.ylabel('Page Views') # لا يغير كل العناوين 



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
