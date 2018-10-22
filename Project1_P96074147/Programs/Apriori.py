import csv
def load_dataset():
    
    # 以csv加載數據集 並且轉成陣列回傳
    with open(r'C:\Users\P96074147\Desktop\Data mining HW1\dataset\cites-wildlife-trade-database\comptab_2018-01-29 16_00_comma_separated3.csv') as csvfile:

    # 讀取CSV檔案內容
      rows = csv.reader(csvfile)    
      dataset = []
    # 以迴圈輸出每一列
      for row in rows:
          dataset.append (row)
    return dataset

def is_apriori(Ck_item, Lksub1):
    
    # 判斷頻繁候選k-itemset是否滿足Apriori屬性
    # Ck_item：Ck中頻繁的候選k-itemset包含所有頻繁候選k項集
    # Lk-1：一個包含所有頻繁候選（k-1）-itemsets的集合
    # 回傳=>真：滿足Apriori屬性/假：不滿足Apriori屬性
    
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

def create_C1(dataset):
    
    # 通過掃描數據集建立frequent itemsets 1-itemset = C1
    # 參數=>dataset：transactions列表 每個transactions都包含幾個items
    # 回傳=>C1：包含所有頻繁候選1項集的集合

    C1 = set()
    for t in dataset:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


def create_Ck(Lksub1, k):

    # 建立Ck：一個包含所有頻繁候選k-itemset的集合
    # 通過LK-1本身的連接操作
    # Lksub1：Lk-1，一個包含所有頻繁候選（k-1）-itemsets的集合
    # k：頻繁項集的項目編號
    # Ck：包含所有頻繁候選k-itemset的集合

    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck

def generate_L(dataset, k, min_support):

    # 生成所有頻繁項集
    # dataset：每筆資料包含幾個項目
    # k：所有頻繁項集的最大項目數
    # min_support：Minimun Support
    # support_data：關鍵是頻繁項集和值是支持的
    # 回傳=>L：LK的列表/support_data：關鍵是頻繁項集和值是支持的
 
    support_data = {}
    C1 = create_C1(dataset)
    L1 = generate_Lk_by_Ck(dataset, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(dataset, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data

def generate_Lk_by_Ck(dataset, Ck, min_support, support_data):

    # 通過執行Ck的刪除策略生成Lk
    # dataset：每筆資料包含幾個項目
    # Ck：包含所有頻繁候選k-itemset的集合
    # min_support：Minimun Support
    # support_data：關鍵是頻繁項集和值是支持的
    # 回傳=>Lk：包含所有頻繁k-itemset的集合

    Lk = set()
    item_count = {}
    for t in dataset:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(dataset))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk

def generate_big_rules(L, support_data, min_conf):

    # 從頻繁項目集生成規則
    # L：LK的列表
    # support_data：關鍵是頻繁項集和值是支持的
    # min_conf：最小信心值
    # 回傳=>big_rule_list：包含所有規則的列表

    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list


if __name__ == "__main__":

    dataset = load_dataset()
    L, support_data = generate_L(dataset, k=5, min_support=0.15)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.7)
    for Lk in L:
        print ("="*50)
        print ("frequent " + "-itemsets\t\tsupport")
        print ("="*50)
        for freq_set in Lk:
            print (freq_set, support_data[freq_set])

    print ("Big Rules")
    for item in big_rules_list:
        if item[2] = 1.0:
            print (item[0], "=>", item[1], "conf: ", item[2])
