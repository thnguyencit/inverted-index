import os
import shutil
import tachcau
import tachtu
path = "dbtonghop/D-PL/"
# path = "db/test2/"
dirDoc = os.listdir(path)

# đếm câu, từ
list_dir = []
total_sen = 0
total_word = 0
for i in range(len(dirDoc)):
	fileContent_sen = tachcau.fileWordTokenize(path+dirDoc[i])[0]
	fileContent_word = tachtu.fileWordTokenize(path+dirDoc[i])[3]
	# print(fileContent)
	total_sen += len(fileContent_sen)
	total_word += len(fileContent_word)
	# db_cau.append(fileContent)
# print(db)

# with open('dbthucnghiem/kichban1/SoLuongCauTu_test.txt', 'w', encoding='utf_8') as f:
# 	f.write("Tổng số lượng câu trong " + path + " là " + str(total_sen))
# 	f.write("\nTổng số lượng từ trong " + path + " là " + str(total_word))

print("Tổng số lượng câu trong " + path + " là " + str(total_sen))
print("\nTổng số lượng từ trong " + path + " là " + str(total_word))
