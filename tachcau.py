from underthesea import word_tokenize
import regex as re
import os
import sys
import time
import docx2txt
from re import sub
from collections import Counter
from underthesea import sent_tokenize
import ast
from collections import Counter


def StrList(text):
    words = text.replace("', '", '#').replace("['", '').replace("']", '')
    return words.split("#")


def listToString(s):
    str1 = " "
    return (str1.join(s))


def fileWordTokenize(fileName):
    file_input = open(fileName, "r+", encoding="utf-8")
    read_file = file_input.read()  # Đọc nội dung của File
    # print(read_file)
    # Tách nội dung File theo từng dòng vô list
    list_string = read_file.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa

    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'ABSTRACT':
            list_string[sen1] = 'TÓM TẮT'

    # if content[sen] == 'NGƯỜI GIỚI THIỆU':
    #     content[sen] = 'TÀI LIỆU THAM KHẢO'=
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
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
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
    # print(fileName)
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
    # print(tomtat_listUpper)
    gioithieu_listUpper = listUpper[tomtat_listUpper + 1]
    # print(gioithieu_listUpper)
    gioiThieu = listWord.index(gioithieu_listUpper)
    # print(gioiThieu)

    # Lấy ra tài liệu tham khảo nếu ko có LCT
    if flag == 1:
        content = listWord[gioiThieu+1:]
    else:
        tailieu_listUpper = listUpper[len(listUpper) - 1]
        tailieu = listWord.index(tailieu_listUpper)
        content = listWord[gioiThieu:tailieu]

    # print(content)
    # xóa số
    delete_number = []
    for sen1 in content:
        n = re.sub(r'\b\d+\b', " ", sen1)
        delete_number.append(n)

    # print(delete_number)


    # xóa dấu
    delete_punctuation = []
    for sen2 in delete_number:
        dau = r"""[,|*|:]"""
        sp = re.sub(dau, "", sen2)
        if sp == '' or sp == ' ' or len(sp) <= 2:
            pass
        else:
            delete_punctuation.append(sp)

    # print(delete_punctuation)

    # xóa dấu
    delete_punctuation1 = []
    for sen3 in delete_punctuation:
        f = re.sub(r"((?<=^)|(?<= )).((?=$)|(?= ))", "", sen3)
        delete_punctuation1.append(f)

    # print(delete_punctuation1)

    # xóa bảng
    split_table = []
    for sen4 in delete_punctuation1:
        Hinh = r"""[0-9][a-zA-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂưăạảấầẩẫậắằẳẵặẹẻẽếềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵýỷỹ']"""
        text2 = re.sub(Hinh, "", sen4)
        split_table.append(text2)

    # print(split_table)

    # xóa bảng
    split_table1 = []
    for sen5 in split_table:
        Hinh = r"""\S*\d\S*"""
        text2 = re.sub(Hinh, "", sen5)
        split_table1.append(text2)

    # print(split_table1)

    # xóa công thức toán
    content_math = []
    for w in split_table1:
        re_w_one = re.sub(
            r'[\d,():=/^°\-_¬∧∨∃∅&@+%;■*Ωλπω∈βαηρ〖〗⃗\[\]⁡{}∑▒█φθ ̂>γ&#@<!?~`´⊆<=>±→∅–"┤├│∀≤≥|√ŷ∩∪×\'‖┬∏ε¯⁻−↔ξ⊂μ⋯δïф∇∙∫ϱ↦∞ωψ∞∆∬σ″²⟦⟧∙∂≠≔⋅ζ ⁄ç•≮∉\⇔∃ º⌉⌈〉〈□$]', ' ', w)
        re_w_two = re.sub(r'(m)s|\_\w+|cos|khz|^\s+$', '', re_w_one)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
	        content_math.append(re_w_two)
    # print(content_math)  

    # xóa khoảng trắng
    delete_space = []
    for sen6 in content_math:
        m1 = re.sub("    +", "", sen6)
        if m1 == '' or m1 == ' ' or len(m1) <= 2:
            pass
        else:
            m1 = m1.replace("  ", " ")
            delete_space.append(m1.strip())
    # print(delete_space)  


    content_string_one = '. '.join(delete_space) 
    listRes = sent_tokenize(content_string_one) 
    # testlower = list(map(lambda x: x.lower(), listRes)) 
    # print(listRes)

    # tách các kí tự thừa còn lại
    delete_punctuation2 = []
    for sen7 in listRes:
        dau = r"""[,|.|*]"""
        sp = re.sub(dau, "", sen7)
        if sp == '' or sp == ' ' or len(sp) <= 2:
            pass
        else:
            delete_punctuation2.append(sp)

    # lấy ra tiêu đề viết hoa '5 KẾT LUẬN', '1 TÓM TẮT','2 GIỚI THIỆU','3 PHƯƠNG PHÁP',... => 'KẾT LUẬN', 'TÓM TẮT','GIỚI THIỆU','PHƯƠNG PHÁP',...
    demucVietHoa = []
    for subject in listUpper:
        n = re.sub(r'\b\d+\b', " ", subject)
        m1 = re.sub("    +", "", n)
        if m1 == '' or m1 == ' ' or len(m1) <= 2:
            pass
        else:
            m1 = m1.replace("  ", " ")
            demucVietHoa.append(m1.strip())
    # print(demucVietHoa)

    # xóa những tiêu đề: '5 KẾT LUẬN', '1 TÓM TẮT','2 GIỚI THIỆU','3 PHƯƠNG PHÁP',...
    content_final = []
    for sen8 in delete_punctuation2:
        if sen8 in demucVietHoa:
            # print(sen8)
            pass
        else:
            content_final.append(sen8)

    # print(content_final)


    content_string_two = '. '.join(content_final).lower()
    content_process_split = content_string_two.split(' ')



    content_process = word_tokenize(content_string_two, format="text") # ['tu_1 tu_2 tu_3 ...']
    content_process_split = content_process.split(' ')  # ['tu_1','tu_2','...']

	# Begin Xóa Stopword
    stopwords = open("VI_StopWord.txt","r+", encoding="utf-8")
    stopwords_read = stopwords.read()
    stopwords_split = stopwords_read.split('\n')
    content_stopword = []
    for n in content_process_split:
        if n in stopwords_split:
            pass
        else:
            content_stopword.append(n)
    # End Xóa Stopword


    # tách câu
    # print(content_final) # ['Khi các tua bin gió quay tốc độ khác nhau dòng điện tạo ra mỗi tua bin có tần số và góc pha khác nhau nên khi kết hợp tua bin điện áp AC sẽ giảm công suất đầu ra', 'Khi đó việc kết hợp các tua bin điện áp DC sẽ cho ra công suất lớn hơn hiệu suất cao', 'Vì vậy khi kết hợp tua bin gió nên kết hợp điện áp DC để đạt hiệu quả cao nhất']

    # nguyên bài
    # print(content_string_two) # 'Tôi sinh viên đại_học cần_thơ. mot hai Ba bon. bc. hello thạc. eee'

    # tách từ
    # print(content_stopword) # lower # ['tôi', 'sinh_viên', 'đại_học', 'cần_thơ', 'mot', 'hai', 'ba', 'bon', 'bc', 'hello', 'thạc', 'eee']
    content_string_three = '. '.join(content_stopword).lower()

    return content_final, content_string_two, content_stopword, content_string_three


# path = "File convert VN/A-CN/01-CN-NGUYEN THAI SON(1-9)106.txt"
# print(Counter(fileWordTokenize(path)[0]))


