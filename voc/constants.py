

def load_list_to_dic(pc_path:str):
    print('Loading dictionary')
    ll_eng = []
    ll_rus = []
    try:
        fl = open(pc_path,'r')
        lines = [i.replace('\t','\n')    for i in    fl.read().splitlines()]
        fl.close()
        ln_counter = 0
        for line in lines:
            ln_counter += 1
            if ln_counter % 2 != 0:
                ll_eng.append(line)
            else:
                ll_rus.append(line)
    except: print('Error with', pc_path)
    return [ll_eng,ll_rus]




ll_dictionary = load_list_to_dic('ENRUS.TXT')