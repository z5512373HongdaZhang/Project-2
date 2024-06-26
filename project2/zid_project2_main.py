""" zid_project2_main.py

"""
# ----------------------------------------------------------------------------
# Part 1: Read the documentation for the following methods:
#   – pandas.DataFrame.mean
#   - pandas.Series.concat
#   – pandas.Series.count
#   – pandas.Series.dropna
#   - pandas.Series.index.to_period
#   – pandas.Series.prod
#   – pandas.Series.resample
#   - ......
# Hint: you can utilize modules covered in our lectures, listed above and any others.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Part 2: import modules inside the project2 package
# ----------------------------------------------------------------------------
# Create import statements so that the module config.py and util.py (inside the project2 package)
# are imported as "cfg", and "util"
#
import config as cfg
import util
import numpy as np




# We've imported other needed scripts and defined aliases. Please keep using the same aliases for them in this project.
import zid_project2_etl as etl
import zid_project2_characteristics as cha
import zid_project2_portfolio as pf

import pandas as pd


# -----------------------------------------------------------------------------------------------
# Part 3: Follow the workflow in portfolio_main function
#         to understand how this project construct total volatility long-short portfolio
# -----------------------------------------------------------------------------------------------
def portfolio_main(tickers, start, end, cha_name, ret_freq_use, q):
    """
    Constructs equal-weighted portfolios based on the specified characteristic and quantile threshold.
    We focus on total volatility investment strategy in this project 2.
    We name the characteristic as 'vol'

    This function performs several steps to construct portfolios:
    1. Call `aj_ret_dict` function from etl script to generate a dictionary containing daily and
       monthly returns.
    2. Call `cha_main` function from cha script to generate a DataFrame containing stocks' monthly return
       and characteristic, i.e., total volatility, info.
    3. Call `pf_main` function from pf script to construct a DataFrame with
       equal-weighted quantile and long-short portfolio return series.

    Parameters
    ----------
    tickers : list
        A list including all tickers (can include lowercase and/or uppercase characters) in the investment universe

    start  :  str
        The inclusive start date for the date range of the price table imported from data folder
        For example: if you enter '2010-09-02', function in etl script will include price
        data of stocks from this date onwards.
        And make sure the provided start date is a valid calendar date.

    end  :  str
        The inclusive end date for the date range, which determines the final date
        included in the price table imported from data folder
        For example: if you enter '2010-12-20', function in etl script will encompass data
        up to and including December 20, 2010.
        And make sure the provided start date is a valid calendar date.

    cha_name : str
        The name of the characteristic. Here, it should be 'vol'

    ret_freq_use  :  list
        It identifies that which frequency returns you will use to construct the `cha_name`
        in zid_project2_characteristics.py.
        Set it as ['Daily',] when calculating stock total volatility here.

    q : int
        The number of quantiles to divide the stocks into based on their characteristic values.


    Returns
    -------
    dict_ret : dict
        A dictionary with two items, each containing a dataframe of daily and monthly returns
        for all stocks listed in the 'tickers' list.
        This dictionary is the output of `aj_ret_dict` in etl script.
        See the docstring there for a description of it.

    df_cha : df
        A DataFrame with a Monthly frequency PeriodIndex, containing rows for each year-month
        that include the stocks' monthly returns for that period and the characteristics,
        i.e., total volatility, from the previous year-month.
        This df is the output of `cha_main` function in cha script.
        See the docstring there for a description of it.

    df_portfolios : df
        A DataFrame containing the constructed equal-weighted quantile and long-short portfolios.
        This df is the output of `pf_cal` function in pf script.
        See the docstring there for a description of it.

    """

    # --------------------------------------------------------------------------------------------------------
    # Part 4: Complete etl scaffold to generate returns dictionary and to make ad_ret_dic function works
    # --------------------------------------------------------------------------------------------------------
    dict_ret = etl.aj_ret_dict(tickers, start, end)

    # ---------------------------------------------------------------------------------------------------------
    # Part 5: Complete cha scaffold to generate dataframe containing monthly total volatility for each stock
    #         and to make char_main function work
    # ---------------------------------------------------------------------------------------------------------
    df_cha = cha.cha_main(dict_ret, cha_name,  ret_freq_use)

    # -----------------------------------------------------------------------------------------------------------
    # Part 6: Read and understand functions in pf scaffold. You will need to utilize functions there to
    #         complete some of the questions in Part 7
    # -----------------------------------------------------------------------------------------------------------
    df_portfolios = pf.pf_main(df_cha, cha_name, q)

    util.color_print('Portfolio Construction All Done!')

    return dict_ret, df_cha, df_portfolios


# ----------------------------------------------------------------------------
# Part 7: Complete the auxiliary functions
# ----------------------------------------------------------------------------
def get_avg(df: pd.DataFrame, year):
    """ Returns the average value of all columns in the given df for a specified year.

    This function will calculate the column average for all columns
    from a data frame `df`, for a given year `year`.
    The data frame `df` must have a DatetimeIndex or PeriodIndex index.

    Missing values will not be included in the calculation.

    Parameters
    ----------
    df : data frame
        A Pandas data frame with a DatetimeIndex or PeriodIndex index.

    year : int
        The year as a 4-digit integer.

    Returns
    -------
    ser
        A series with the average value of columns for the year `year`.

    Example
    -------
    For a data frame `df` containing the following information:

        |            | tic1 | tic2  |
        |------------+------+-------|
        | 1999-10-13 | -1   | NaN   |
        | 1999-10-14 | 1    | 0.032 |
        | 2020-10-15 | 0    | -0.02 |
        | 2020-10-16 | 1    | -0.02 |

        >> res = get_avg(df, 1999)
        >> print(res)
        tic1      0.000
        tic2      0.032
        dtype: float64

    """

    df_year = df[df.index.year == year]
    df_mean = df_year.mean()
    return df_mean


def get_cumulative_ret(df):
    """ Returns cumulative returns for input DataFrame.

    Given a df with return series, this function will return the
    buy and hold return for the whole period.

    Parameters
    ----------
    df : DataFrame
        A Pandas DataFrame containing monthly portfolio returns
        with a PeriodIndex index.

    Returns
    -------
    df
        A df with the cumulative returns for portfolios, ignoring missing observations.

    Notes
    -----
    The buy and hold cumulative return will be computed as follows:

        (1 + r1) * (1 + r2) *....* (1 + rN) - 1
        where r1, ..., rN represents monthly returns

    """

    cumulative_ret = (1 + df).prod() - 1
    return cumulative_ret

# ----------------------------------------------------------------------------
# Part 8: Answer questions
# ----------------------------------------------------------------------------
# NOTES:
#
# - THE SCRIPTS YOU NEED TO SUBMIT ARE
#   zid_project2_main.py, zid_project2_etl.py, and zid_project2_characteristics.py
#
# - Do not create any other functions inside the scripts you need to submit unless
#   we ask you to do so.
#
# - For this part of the project, only the answers provided below will be
#   marked. You are free to create any function you want (IN A SEPARATE
#   MODULE outside the scripts you need to submit).
#
# - All your answers should be strings. If they represent a number, include 4
#   decimal places unless otherwise specified in the question description
#
# - Here is an example of how to answer the questions below. Consider the
#   following question:
#
#   Q0: Which ticker included in config.TICMAP starts with the letter "C"?
#   Q0_answer = '?'
#
#   You should replace the '?' with the correct answer:
#   Q0_answer = 'CSCO'
#
#
#     To answer the questions below, you need to run portfolio_main function in this script
#     with the following parameter values:
#     tickers: all tickers included in the dictionary config.TICMAP,
#     start: '2000-12-29',
#     end: '2021-08-31',
#     cha_name: 'vol'.
#     ret_freq_use: ['Daily',],
#     q: 3
#     Please name the three output files as DM_Ret_dict, Vol_Ret_mrg_df, EW_LS_pf_df.
#     You can utilize the three output files and auxiliary functions to answer the questions.


# Q1: Which stock in your sample has the lowest average daily return for the
#     year 2008 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q1_ANSWER = 'nvda'


# Q2: What is the daily average return of the stock in question 1 for the year 2008.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q2_ANSWER = '-0.0042'


# Q3: Which stock in your sample has the highest average monthly return for the
#     year 2019 (ignoring missing values)? Your answer should include the
#     ticker for this stock.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q3_ANSWER = 'aapl'


# Q4: What is the average monthly return of the stock in question 3 for the year 2019.
#     Use the output dictionary, DM_Ret_dict, and auxiliary function in this script
#     to do the calculation.
Q4_ANSWER = '0.0566'


# Q5: What is the average monthly total volatility for stock 'TSLA' in the year 2010?
#     Use the output dataframe, Vol_Ret_mrg_df, and auxiliary function in this script
#     to do the calculation.
Q5_ANSWER = '0.0426'


# Q6: What is the ratio of the average monthly total volatility for stock 'V'
#     in the year 2008 to that in the year 2018? Keep 1 decimal places.
#     Use the output dataframe, Vol_Ret_mrg_df, and auxiliary function in this script
#     to do the calculation.
Q6_ANSWER = '0.4'


# Q7: How many effective year-month for stock 'TSLA' in year 2010. An effective year-month
#     row means both monthly return in 'tsla' column and total volatility in 'tsla_vol'
#     are not null.
#     Use the output dataframe, Vol_Ret_mrg_df, to do the calculation.
#     Answer should be an integer
Q7_ANSWER = '5'


# Q8: How many rows and columns in the EW_LS_pf_df data frame?
#     Answer should be two integer, the first represent number of rows and the two numbers need to be
#     separated by a comma.

Q8_ANSWER = '235,4'


# Q9: What is the average equal weighted portfolio return of the quantile with the
#     lowest total volatility for the year 2019?
#     Use the output dataframe, EW_LS_pf_d, and auxiliary function in this script
#     to do the calculation.
Q9_ANSWER = '0.0182'


# Q10: What is the cumulative portfolio return of the total volatility long-short portfolio
#      over the whole sample period?
#      Use the output dataframe, EW_LS_pf_d, and auxiliary function in this script
#     to do the calculation.
Q10_ANSWER = '1.5980'

# ----------------------------------------------------------------------------
# Part 9: Add t_stat function
# ----------------------------------------------------------------------------
# We've outputted EW_LS_pf_df file and save the total volatility long-short portfolio
# in 'ls' column from Part 8.

# Please add an auxiliary function called ‘t_stat’ below.
# You can design the function's parameters and output table.
# But make sure it can be used to output a DataFrame including three columns:
# 1.ls_bar, the mean of 'ls' columns in EW_LS_pf_df
# 2.ls_t, the t stat of 'ls' columns in EW_LS_pf_df
# 3.n_obs, the number of observations of 'ls' columns in EW_LS_pf_df

# Notes:
# Please add the function in zid_project2_main.py.
# The name of the function should be t_stat and including docstring.
# Please replace the '?' of ls_bar, ls_t and n_obs variables below
# with the respective values of the 'ls' column in EW_LS_pf_df from Part 8,
# keep 4 decimal places if it is not an integer:
ls_bar = '0.0073'
ls_t = '1.3847'
n_obs = '235'
# ls_bar = '0.0073'
# ls_t = '1.3847'
# n_obs = '235'


# <ADD THE t_stat FUNCTION HERE>
def t_stat(portfolio_df):
    """
    Calculate the t-statistic for the long-short portfolio volatility.

    Args:
        portfolio_df (pd.DataFrame): DataFrame containing the long-short portfolio data.

    Returns:
        pd.DataFrame: A DataFrame with three columns:
            - 'ls_bar': Mean of the 'ls' column
            - 'ls_t': T-statistic for the 'ls' column
            - 'n_obs': Number of observations in the 'ls' column
    """
    ls_volatility = portfolio_df['ls']

    ls_mean = np.mean(ls_volatility)
    ls_std = np.std(ls_volatility,ddof=1)

    n = len(ls_volatility)
    t_statistic = ls_mean / (ls_std / np.sqrt(n))
    ls_mean_rounded = round(ls_mean, 4)
    t_statistic_rounded = round(t_statistic, 4)

    t_stat_df = pd.DataFrame({
        'ls_bar': [ls_mean_rounded],
        'ls_t': [t_statistic_rounded],
        'n_obs': [n]
    })

    return t_stat_df

# Example usage:
if __name__ == "__main__":
    # Load your EW_LS_pf_df data (assuming it's already available)
    # Replace the following line with your actual data loading code
    main = portfolio_main(cfg.TICMAP, '2000-12-29', '2021-08-31', 'vol', ['Daily'], 3)
    EW_LS_pf_df = main[2]
    portfolio_data = EW_LS_pf_df

    # Calculate the t-statistic
    t_stat_result = t_stat(portfolio_data)
    print(t_stat_result)
# ----------------------------------------------------------------------------
# Part 10: share your team's project 2 git log
# ----------------------------------------------------------------------------
# In week6 slides, we introduce Git and show how to work collaboratively on Git.
# You are not necessary to use your UNSW email to register the git account.
# But when you set up your username, you will follow the format zid...FirstNameLastName.
#
# Please follow the instruction there to work with your teammates. The team leader
# will need to create a Project 2 Repo on GitHub and grant teammates access to the Repo.
# For teammates, you will need to clone the repo and then coding as a team.
#
# The team will need to generate a git log from git terminal.
# You can use 'cd <...>' direct your terminal into the project 2 repo directory,
# then export the git log:
# git log --pretty=format:"%h%x09%an%x09%ad%x09%s" >teamX.txt
# Here is an example output:
# .......
# dae0fa9	zid1234 Sarah Xiao	Mon Feb 12 16:33:22 2024 +1100	commit and push test
# fa26a62	zid1234 Sarah Xiao	Mon Feb 12 16:32:02 2024 +1100	commit and push test
# 800bf27	zid5678 David Lee	Mon Feb 12 16:12:30 2024 +1100	for testing
# .......
#
# Please replace the """?""" with your team's project 2 git log:
git_log = """
0bb6a76	z5512373HongdaZhang	Fri Apr 19 14:20:54 2024 +1000	Merge remote-tracking branch 'origin/main'
3b6858b	z5512373HongdaZhang	Fri Apr 19 14:20:38 2024 +1000	Presentation update
b7bfec0	z5512373HongdaZhang	Fri Apr 19 14:12:57 2024 +1000	Delete toolkit_config.py
9ddf786	z5512373HongdaZhang	Fri Apr 19 14:05:04 2024 +1000	Presentation link update
0ee0f74	Ziheng Rao	Thu Apr 18 16:39:18 2024 +1000	for testing
a8fb59a	Ziheng Rao	Thu Apr 18 11:42:12 2024 +1000	part 8
ea12bd9	z5512074DanWu	Sun Apr 14 23:17:19 2024 +1000	fill
0742d36	z5512074DanWu	Sun Apr 14 22:56:18 2024 +1000	fill
9ba5f41	z5512074DanWu	Sun Apr 14 22:53:42 2024 +1000	fill
529104e	z5512373HongdaZhang	Sun Apr 14 14:24:13 2024 +1000	Q10 update
627867e	z5512373HongdaZhang	Sun Apr 14 14:23:02 2024 +1000	Q9 update
d40111e	z5512373HongdaZhang	Sun Apr 14 13:57:11 2024 +1000	Q10
1c9f0af	z5512373HongdaZhang	Sun Apr 14 13:53:34 2024 +1000	Merge remote-tracking branch 'origin/main'
551ab1e	z5512373HongdaZhang	Sun Apr 14 13:53:10 2024 +1000	Q9
a7ee237	z5498046QianyuZhou	Sun Apr 14 13:29:50 2024 +1000	Q9
91abd28	z5498046QianyuZhou	Sun Apr 14 13:16:42 2024 +1000	Q8
e912574	Ziheng Rao	Sat Apr 13 19:18:48 2024 +1000	Merge remote-tracking branch 'origin/main' into main
fb33711	Ziheng Rao	Sat Apr 13 19:18:09 2024 +1000	part 8
1825a91	z5512074DanWu	Fri Apr 12 23:27:43 2024 +1000	simplified merge_tables
e9abfd1	z5512074DanWu	Fri Apr 12 22:41:07 2024 +1000	Merge remote-tracking branch 'origin/main'
7cb8020	z5512074DanWu	Fri Apr 12 22:40:43 2024 +1000	T-test
ffae8be	z5512373HongdaZhang	Fri Apr 12 22:22:57 2024 +1000	Q9
1949ba0	z5498046QianyuZhou	Fri Apr 12 22:19:59 2024 +1000	Merge remote-tracking branch 'origin/main'
f0fc498	z5498046QianyuZhou	Fri Apr 12 22:19:39 2024 +1000	Q8
543a29b	z5512074DanWu	Fri Apr 12 22:16:45 2024 +1000	test
834ed40	z5512074DanWu	Fri Apr 12 22:15:24 2024 +1000	Merge remote-tracking branch 'origin/main'
303ae85	z5512074DanWu	Fri Apr 12 22:14:42 2024 +1000	to_period(M)
d130075	z5512074DanWu	Fri Apr 12 22:11:06 2024 +1000	to_period(M)
2103c0f	z5498046QianyuZhou	Fri Apr 12 22:09:22 2024 +1000	modify cha
ad583d2	z5512074DanWu	Fri Apr 12 22:06:04 2024 +1000	to_period(M)
6ac572d	z5512074DanWu	Fri Apr 12 21:54:54 2024 +1000	to_period(M)
a7ca129	z5512074DanWu	Fri Apr 12 21:52:28 2024 +1000	to_period(M)
915003d	z5512074DanWu	Fri Apr 12 21:51:27 2024 +1000	to_period(M)
2705eac	z5512074DanWu	Fri Apr 12 21:32:24 2024 +1000	to_period(M)
fce335e	z5524321ShengfaSun	Fri Apr 12 20:12:01 2024 +1000	PARTIAL Q9
72c5a6a	z5524321ShengfaSun	Fri Apr 12 20:09:56 2024 +1000	comments on 5.2
a7f5d8a	z5524321ShengfaSun	Fri Apr 12 16:39:12 2024 +1000	Merge remote-tracking branch 'origin/main'
e39ab22	z5512074DanWu	Fri Apr 12 13:44:48 2024 +1000	Modify Q1 to Q4
4c0dad6	z5512074DanWu	Fri Apr 12 13:33:17 2024 +1000	Modify Q1 to Q4
1dcd771	z5524321ShengfaSun	Thu Apr 11 22:31:55 2024 +1000	Merge remote-tracking branch 'origin/main'
2e212ed	z5498046QianyuZhou	Thu Apr 11 22:21:21 2024 +1000	8.Q7
b4263b6	z5524321ShengfaSun	Thu Apr 11 21:15:24 2024 +1000	Merge remote-tracking branch 'origin/main'
259254c	Ziheng Rao	Thu Apr 11 21:12:40 2024 +1000	part 8
5f255f9	Ziheng Rao	Thu Apr 11 20:32:37 2024 +1000	part 8
68de599	z5524321ShengfaSun	Thu Apr 11 19:38:32 2024 +1000	Merge remote-tracking branch 'origin/main'
2521a8b	Ziheng Rao	Thu Apr 11 19:21:31 2024 +1000	part 8
bdd72ce	z5524321ShengfaSun	Thu Apr 11 17:01:41 2024 +1000	comments on 5.2
0c0c577	z5524321ShengfaSun	Thu Apr 11 16:48:43 2024 +1000	Merge remote-tracking branch 'origin/main'
145cbaf	z5524321ShengfaSun	Thu Apr 11 16:47:32 2024 +1000	fixing
e3281af	Ziheng Rao	Thu Apr 11 16:19:28 2024 +1000	Merge remote-tracking branch 'origin/main' into main
0a9cb65	z5512074DanWu	Thu Apr 11 16:12:03 2024 +1000	Comments
7e5701f	Ziheng Rao	Thu Apr 11 16:00:55 2024 +1000	Merge remote-tracking branch 'origin/main' into main
246f615	Ziheng Rao	Thu Apr 11 15:59:34 2024 +1000	part 8
798157e	Ziheng Rao	Thu Apr 11 15:44:44 2024 +1000	Part 7
2a62fd5	z5512074DanWu	Thu Apr 11 15:30:38 2024 +1000	auxiliary functions
a18109c	z5512074DanWu	Thu Apr 11 15:26:01 2024 +1000	auxiliary functions
6484304	z5512074DanWu	Thu Apr 11 14:57:28 2024 +1000	merge_tables
1e9351f	z5512074DanWu	Thu Apr 11 12:06:45 2024 +1000	Merge remote-tracking branch 'origin/main'
e0f76db	z5512074DanWu	Thu Apr 11 11:58:46 2024 +1000	Modified vol_cal
55305e4	Ziheng Rao	Thu Apr 11 09:16:12 2024 +1000	输入
2320f86	Ziheng Rao	Thu Apr 11 02:36:05 2024 +1000	1
fd07e5a	Ziheng Rao	Thu Apr 11 02:30:57 2024 +1000	Merge remote-tracking branch 'origin/main' into main
7033c0b	z5512074DanWu	Thu Apr 11 00:35:12 2024 +1000	Merge remote-tracking branch 'origin/main'
ca05eab	z5524321ShengfaSun	Thu Apr 11 00:32:19 2024 +1000	characteristics updated
b29cc1e	z5524321ShengfaSun	Thu Apr 11 00:27:35 2024 +1000	characteristics updated
567ac46	z5512074DanWu	Thu Apr 11 00:10:54 2024 +1000	5.1
26c6487	z5498046QianyuZhou	Wed Apr 10 21:25:00 2024 +1000	4doublecheck
f4c7fcc	z5512373HongdaZhang	Wed Apr 10 21:11:43 2024 +1000	test new
638f547	Hongda Zhang	Wed Apr 10 20:44:43 2024 +1000	Part4 Complete
12d8729	z5512373HongdaZhang	Wed Apr 10 20:40:33 2024 +1000	test
96148ef	Hongda Zhang	Wed Apr 10 20:38:17 2024 +1000	test
9a4d25b	Hongda Zhang	Wed Apr 10 19:51:52 2024 +1000	4.5 develop
ae3d781	z5498046QianyuZhou	Wed Apr 10 19:36:50 2024 +1000	4.4develop
77c0811	z5498046QianyuZhou	Wed Apr 10 19:35:39 2024 +1000	4.3develop
863401b	Hongda Zhang	Wed Apr 10 18:24:23 2024 +1000	4.3 code
62c507d	z5498046QianyuZhou	Wed Apr 10 18:07:30 2024 +1000	4.2develop
28f9f53	z5498046QianyuZhou	Wed Apr 10 17:44:44 2024 +1000	4.2 code
5fd5065	z5498046QianyuZhou	Wed Apr 10 17:43:59 2024 +1000	test new
b5d2667	Ziheng Rao	Wed Apr 10 17:17:01 2024 +1000	1
85c3328	Hongda Zhang	Wed Apr 10 13:28:51 2024 +1000	Part 2 import
cd9a9e9	z5524321ShengfaSun	Wed Apr 10 12:41:15 2024 +1000	Merge remote-tracking branch 'origin/main'
26ff229	z5524321ShengfaSun	Wed Apr 10 12:40:57 2024 +1000	char
549f910	z5498046QianyuZhou	Wed Apr 10 12:38:13 2024 +1000	Merge remote-tracking branch 'origin/main'
3e07146	z5512074DanWu	Wed Apr 10 12:37:36 2024 +1000	Merge remote-tracking branch 'origin/main'
3f64c92	z5498046QianyuZhou	Wed Apr 10 12:37:34 2024 +1000	test new
e8eb8b1	z5512074DanWu	Wed Apr 10 12:37:02 2024 +1000	test
f8f11b6	zid5498046QianyuZhou	Wed Apr 10 12:32:06 2024 +1000	test
a7c8bf1	z5512373HongdaZhang	Wed Apr 10 12:12:16 2024 +1000	Add files via upload
f741e95	z5512373HongdaZhang	Wed Apr 10 11:32:31 2024 +1000	Add files via upload
0690165	z5512373HongdaZhang	Wed Apr 10 11:31:12 2024 +1000	Delete project2.zip
3d12dc9	z5512373HongdaZhang	Wed Apr 10 11:30:40 2024 +1000	Add files via upload
"""

# ----------------------------------------------------------------------------
# Part 11: project 2 mini-presentation
# ----------------------------------------------------------------------------
# In this part, you are going to record and present a strictly less than 15 minutes long presentation.
# You should seek to briefly describe:
# 1.	What are the null and alternative hypotheses that the project 2 is testing
# 2.	What’s the methodology of the portfolio construction
#       and how is it implemented in Project 2 codebase?
# 3.	What inferences can we draw from the output of Part 9,
#       including the average return and t-stats of the long-short portfolio?
# 4.	Do you think the results are reliable? Why or why not?
# 5.	Is there any further work you would like to pursue based on Project 2?
#       Share your to-do list.
#
# For this mini-presentation, it is up to the group to decide whether all the members
# are in the presentation video or not.
# Please use Zoom to record it. The final submission should be a zoom recording link.

# Please replace the '?' with your team's presentation video zoom link:
Presentation_zoom_link = 'https://drive.google.com/file/d/1m6E6Jy9IMuL_n3sjjTDiKqJz24iemnHN/view?usp=sharing'
Password_of_your_video = 'NO PASSWORD'


def _test_get_avg():
    """ Test function for `get_avg`
    """
    # Made-up data
    ret = pd.Series({
        '2019-01-01': 1.0,
        '2019-01-02': 2.0,
        '2020-10-02': 4.0,
        '2020-11-12': 4.0,
    })
    df = pd.DataFrame({'some_tic': ret})
    df.index = pd.to_datetime(df.index)

    msg = 'This is the test data frame `df`:'
    util.test_print(df, msg)

    res = get_avg(df,  2019)
    to_print = [
        "This means `res =get_avg(df, year=2019) --> 1.5",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


def _test_get_cumulative_ret():
    """ Test function for `get_ann_ret`

    To construct this example, suppose first that holding the stock for 400
    trading days gives a total return of 1.5 (so 50% over 400 trading days).

    The annualised return will then be:

        (tot_ret)**(252/N) - 1 = 1.5 ** (252/400) - 1 = 0.2910

    Create an example data frame with 400 copies of the daily yield, where

        daily yield = 1.5 ** (1/400) - 1

    """
    # Made-up data
    idx_m = pd.to_datetime(['2019-02-28',
                            '2019-03-31',
                            '2019-04-30',]).to_period('M')
    stock1_m = [0.063590, 0.034290, 0.004290]
    stock2_m = [None, 0.024390, 0.022400]
    monthly_ret_df = pd.DataFrame({'stock1': stock1_m, 'stock2': stock2_m, }, index=idx_m)
    monthly_ret_df.index.name = 'Year_Month'
    msg = 'This is the test data frame `monthly_ret_df`:'
    util.test_print(monthly_ret_df, msg)

    res = get_cumulative_ret(monthly_ret_df)
    to_print = [
        "This means `res =get_cumulative_ret(monthly_ret_df)",
        f"The value of `res` is {res}",
    ]
    util.test_print('\n'.join(to_print))


if __name__ == "__main__":
    pass






