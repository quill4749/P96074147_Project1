# python3
# -*- coding: utf-8 -*-

import fp_growth_py3 as fpg
import csv

  # 以csv加載數據集 並且轉成陣列回傳
with open(r'C:\Users\P96074147\Desktop\Data mining HW1\dataset\cites-wildlife-trade-database\comptab_2018-01-29 16_00_comma_separated3.csv', newline='') as csvfile:

  # 讀取 CSV 檔案內容
      rows = csv.reader(csvfile)	
      dataset = []
  # 以迴圈輸出每一列
      for row in rows:
          dataset.append (row)


if __name__ == '__main__':

    # 調用find_frequent_itemsets()生成頻繁項集
    # param minimum_support：設置的最小支持度，若支持度大於等於minimum_support，保留此頻繁項集，否則刪除
    # param include_support：回傳结果是否包含支持度，若為True，回傳结果包含itemset和support，否則只回傳itemset

    f_itemset = fpg.find_frequent_itemsets(dataset, minimum_support=750, include_support=True)
    print(type(f_itemset))
    result = []
    for itemset, support in f_itemset:
        result.append((itemset, support))

    result = sorted(result, key=lambda i: i[0]) 
    for itemset, support in result:
        print(str(itemset) + ' ' + str(support))



