# Import các thư viện cần thiết
from underthesea import word_tokenize, sent_tokenize
import regex as re
import os
import sys
import time


def fileWordTokenize(fileName):
    file_input = open(fileName, "r+", encoding="utf-8")
    read_file = file_input.read()  # Đọc nội dung của File

    # Tách nội dung File theo từng dòng vô list
    list_string = read_file.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa

    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'ABSTRACT':
            list_string[sen1] = 'TÓM TẮT'
        # if content[sen] == 'NGƯỜI GIỚI THIỆU':
        #     content[sen] = 'TÀI LIỆU THAM KHẢO'

    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN' or value == 'TÀI LIỆU THAM KHẢO':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'ABSTRACT':
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    # print(listUpper)
    # Begin lấy ra và xử lý và lấy ra tiêu đề
    title_index_listUpper = listUpper.index('TÓM TẮT')
    if title_index_listUpper == 2:
        get_title = listWord[0]
    elif title_index_listUpper == 4:
        title_list = listUpper[0:3]
        get_title = ' '.join(title_list)
    else:
        title_list = listUpper[0:2]
        get_title = ' '.join(title_list)

    title = get_title  # Lấy ra tên tiêu đề bài báo
    # End lấy ra và xử lý tiêu đề

    # Begin Lấy nội dung từ Giới thiệu đến Kết luận
    tomtat_listUpper = listUpper.index('TÓM TẮT')
    # print(tomtat_listUpper) #vị trí từ TÓM TẮT trong danh sách từ viết hoa
    gioithieu_listUpper = listUpper[tomtat_listUpper + 1]
    # print(gioithieu_listUpper) #
    gioiThieu = listWord.index(gioithieu_listUpper)
    # print(gioiThieu) #vị trí từ GIỚI THIỆU trong gioithieu_listUpper

    # Lấy ra tài liệu tham khảo nếu ko có LCT
    if flag == 1:
        content = listWord[gioiThieu+1:]
    else:
        tailieu_listUpper = listUpper[len(listUpper) - 1]
        tailieu = listWord.index(tailieu_listUpper)
        content = listWord[gioiThieu:tailieu]

    # Begin Kết hợp từ Giới thiệu đến Kết luận
    contentJoin = ' '.join(content)  # Ghép lại thành 1 text duy nhất từ list
    contentSplit = contentJoin.split(' ')
    # print(contentJoin) # => 'Tôi là sinh viên'
    # print(contentSplit)# => ['Tôi', 'là','sinh','viên']
    # End Kết hợp từ Giới thiệu đến Kết luận

    # Begin Xóa đi số và công thức
    content_math = []
    for w in contentSplit:
        re_w_one = re.sub(
            r'[\d,():=/.^°\-_¬∧∨∃∅&@+%;■*Ωλπω∈βαηρ〖〗⃗\[\]⁡{}∑▒█φθ ̂>γ&#@<!?~`´⊆<=>±→∅–"┤├│∀≤≥|√ŷ∩∪×\'‖┬∏ε¯⁻−↔ξ⊂μ⋯δïф∇∙∫ϱ↦∞ωψ∞∆∬σ″²⟦⟧∙∂≠≔⋅ζ ⁄ç•≮∉\⇔∃ º⌉⌈〉〈□$]', ' ', w)
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', re_w_one)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            content_math.append(re_w_two)
    # print(content_math)
    # End Xóa đi số và công thức

    # Begin loại bỏ tiếp các phần còn thừa
    content_string_two = ' '.join(content_math)
    word_split = content_string_two.split(' ')
    # print(word_split)
    listWord_split = []
    for word in word_split:
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', word)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            listWord_split.append(word)
    # print(listWord_split)
    # End loại bỏ tiếp các phần còn thừa

    # Begin Đưa hết về lower
    content_string_three = ' '.join(filter(str.isalpha, listWord_split))
    content_lower = content_string_three.lower()
    # End Đưa hết về lower

    # Begin tách từ
    content_process = word_tokenize(content_lower, format="text") # ['tu_1 tu_2 tu_3 ...']
    content_process_split = content_process.split(' ')  # ['tu_1','tu_2','...']
    # # End tách từ

    # Begin tách câu content_TungCau
    # content_TungCau = sent_tokenize(contentJoin)
    # # print(content_TungCau) # tách câu chưa bỏ công thức ['cau1','cau2','...']
    # # End tách câu

    # # Begin tách câu content_CaBai
    # content_CaBai = sent_tokenize(content_string_three)
    # print(content_CaBai) # gom lại thành 1 mang lọc bỏ công thức ['content']
    # End tách câu

    # Begin Xóa Stopword
    stopwords = open("VI_StopWord.txt", "r+", encoding="utf-8")
    stopwords_read = stopwords.read()
    stopwords_split = stopwords_read.split('\n')
    content_stopword = []
    for n in content_process_split:
        if n in stopwords_split:
            pass
        else:
            content_stopword.append(n)
    # End Xóa Stopword

    # # Begin Final content
    contentFinal = ' '.join(content_stopword)
    # contentFinal = content_stopword
    # End Final content
    # contentFinal = content_process_split
    # print(content_stopword)
    return title, contentFinal, contentJoin, contentSplit, content_stopword, content_process


# openFile = r"./data/File convert/A-TN/09-TN_NGUYEN VAN DAT(76-80).txt"
# fileProcessing = fileWordTokenize(openFile)
# print("Tên bài báo: ", fileProcessing[0])
# print("Nội dung bài báo sau khi tách từ: ", fileProcessing[1])

# fileName = r"./data/03-AV-TRAN NGOC BICH(16-21)019.txt"
# fileProcessing = fileWordTokenize(fileName)
# print("Tên bài báo: ", fileProcessing[0])
# print("Nội dung bài báo sau khi tách từ: ", fileProcessing[1])

# Begin xử lý tách từ theo thư mục chỉ định
# FJoin = os.path.join
# path = u'./data/File convert/A-TN/'
# files = [FJoin(path, file) for file in os.listdir(path)]
# print("Số lượng File: ", len(files))
# start_time = time.time()
# for file in files:
#     print('\nsĐang xử lý File: ', file)
#     loadFile = file
#     fileProcessing = fileWordTokenize(loadFile)
#     print("Tên bài báo: ", fileProcessing[0])
#     print("Xử lý xong !")
#     # print("Nội dung bài báo sau khi tách từ: ", fileProcessing[1])


# print("\nTổng thời gian xử lý %s giây" % (time.time() - start_time))
# End xử lý tách từ theo thư mục chỉ định


# path = 'db/word/06-TS-LE QUOC VIET(42-47)142.txt'
# print(fileWordTokenize(path)[1])