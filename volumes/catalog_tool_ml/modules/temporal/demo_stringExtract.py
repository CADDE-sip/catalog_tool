
# %%
#import extract_temporal
from extract_temporal import extract_temporal_from_text

# %%
#extract_temporal_JapaneseYear("令和２年、平成26年、昭和55年。")
extract_temporal_from_text("平成26年、昭和55年,令和２年、")

# %%
#extract_temporal_standardYear("2034年、１９８９年、１２３４年。")
extract_temporal_from_text("2034年、１９８９年、１２３４年。")
# %%
#extract_temporal_FisJapaneseYear("令和２年度、平成26年度、昭和55年度。")
extract_temporal_from_text("令和２年度、平成26年度、昭和55年度。")
# %%
#extract_temporal_FisStandardYear("2034年度、１９８９年度、１２３４年度。")
extract_temporal_from_text("2034年度、１９８９年度、１２３４年度。")
# %%
#extract_temporal_JapaneseYearMonth("令和２年2月、平成26年3月、昭和55年11月。")
extract_temporal_from_text("令和２年2月、平成26年3月、昭和55年11月。")
# %%
#extract_temporal_StandardYearMonth("2034年2月、１９８９年3月、１２３４年11月。")
extract_temporal_from_text("2034年2月、１９８９年3月、１２３４年11月。")
# %%
#extract_temporal_JapaneseYearMonthDay("令和２年2月28日、平成26年3月15日、昭和55年11月30日。")
extract_temporal_from_text("令和２年2月28日、平成26年3月15日、昭和55年11月30日。")

# %%
#extract_temporal_StandardYearMonthDay("2034年2月28日、１９８９年3月5日、１２３４年11月30日。")
extract_temporal_from_text("2034年2月28日、１９８９年3月5日、１２３４年11月30日。")


# %%
demo_title = "平成２３年（2011年）東京都産業連関表。平成元年になにか。\
    2020年度。平成15年3月のデータ。2012年4月。\
    令和元年度のデータもあるよ\
    2020年3月19日とか令和元年11月9日とかも\
    ２０２０年５月23日はふくまれないかな"
extract_temporal_from_text(demo_title)
# %%
demo_title = "平成はふくまれないかな"
extract_temporal_from_text(demo_title)
# %%
