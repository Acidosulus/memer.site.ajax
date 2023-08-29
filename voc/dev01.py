
import os



#должна получить базовый каталог
#ссылку на цепочку подкаталогов подкаталог1|подкаталог2|...|
#
def Get_List_of_Items(type:str, pc_base_path:str) -> list:
	ll_paths = os.listdir(pc_base_path)
	print(ll_paths)
	ll_result = []
	for opath in ll_paths:
		print(pc_base_path ++ opath)
		if os.path.isfile(pc_base_path + opath):
			print(opath)
	return []


lc_base_path  =  "j:\\memer.site\\Storage\\admin\\media"

Get_List_of_Items('volumes', lc_base_path)