import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar 
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')['value']
real_df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
# print(df[(df['value'] <= df['value'].quantile(0.025)) | (df['value'] >= df['value'].quantile(0.975))])
real_df = real_df[(real_df['value'] >= real_df['value'].quantile(0.025)) &
        (real_df['value'] <= real_df['value'].quantile(0.975))
        ]


def draw_line_plot():
    # Draw line plot
    fig , ax = plt.subplots(figsize=(20,5))
    ax.plot( real_df)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_xticks(['2016-07-01','2017-01-01','2017-07-01','2018-01-01','2018-07-01','2019-01-01','2019-07-01','2020-01-01',], ['2016-07','2017-01','2017-07','2018-01','2018-07','2019-01','2019-07','2020-01',])
    # how to automate this (may be convert to datatime then...)


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    #####################
    '''
    كان ثم مشكلة في تصحيح الاختبار رسم الأعمدة إذ يطلب أن يكون عدد الأعمدة 49 وهي عندي 57 والمشكلة هنا أن بداية الجدول من شهر مايو وأنا لما رسمت بالمكتبة المتطورة جعلت هي للأشهر التي قبل ذلك أعمدة فارغة لم أرها على الرسم ورآه المصحح الآلي وتصحيح ذلك أن أستعمل مكتبة التحليل نفسها في الرسم وحساب ذلك أن الأشهر 44 وأن في دليل الرسم الذي يوضح اللون المعطى لكل رسم 4 ومربع أبيض هو خلفية الرسم كله

    مكتبة التحليل pandas
    المكتبة المتطورة sns
    دليل الرسم legend
    '''
    ###############
    # Copy and modify data for monthly bar plot
    df_bar = real_df.copy()
    df_bar['Years'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['Months'] = pd.DatetimeIndex(df_bar.index).month_name()

    df_grouped = df_bar.groupby(['Years', 'Months']).mean().unstack()

    # ترتيب الشهور 
    months_ordered = calendar.month_name[1:]
    df_grouped.columns = (df_grouped.columns.droplevel())
    df_grouped = df_grouped[months_ordered]


    '''
    .unstack()
    هذه الدالة تحول العمود الأخير في الفهرس (وليس في الجدول فانتبه) إلى صف والغرض من ذلك إعداد الجدول ليناسب الرسم بدالة مكتبة التحليل إذ تطلب المكتبة أن يكون الجدول ثاني الأبعاد فتكون صفوف الجدول للمحور الأفقي ويفرق كل مستطيل على اللون حسب أعمدة الجدول المعطى
    مكتبة التحليل pandas

    '''
    # Draw bar plot

    fig = df_grouped.plot(kind='bar').get_figure()
    plt.ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = real_df.copy()
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
