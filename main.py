# 컴퓨터정보과 3학년 A반 202044021 이준혁
# TCP:IP 기말고사 과제물
# 시간표 출력 및 날씨 정보 제공 프로그램

import datetime                 # 시간 계산을 위한 datetime 라이브러리
import tkinter as tk            # GUI 를 위한 tkinter 라이브러리
from tkinter import ttk         # 디자인을 위한 tkinter의 ttk
from tkinter import messagebox  # 메세지 출력을 위한 tkinter의 messagebox
from socket import *            # TCP 통신을 위한 socket 라이브러리
import numpy as np              # 배열 생성 및 수정을 위한 numpy 라이브러리
import time                     # time.sleep() 사용을 위한 라이브러리

def help_window():
    """
    도움말 윈도우를 만드는 함수.
    helpWindow
    프로그램을 어떻게 사용하는지를 안내하는 윈도우다.
    """
    helpWindow = tk.Toplevel(root)
    helpWindow.title('강의 시간표 검색 프로그램 도움말')
    helpWindow.geometry('400x400')
    lbl_help = ttk.Label(helpWindow, text="도움말")
    lbl_help_content = ttk.Label(helpWindow, text="컴퓨터정보과 3학년 A반 202044021 이준혁\n"
                                                  "TCP/IP 기말고사 과제물 시간표 조회 프로그램\n"
                                                  "각 반을 검색하여 해당 시스템으 조회하는 프로그램이다.\n"
                                                  "서버 측에서 시간표와 날씨 정보를 보내주어 클라이언트 측에서 출력한다.")

    lbl_help.pack()
    lbl_help_content.pack()


def combo_print():
    """
    학년을 선택함에 따라 맞춰 변하는 과목, 교수님 목록을 변경하기 위한 함수이다.
    subList = 학년에 따른 과목 리스트
    proList = 학년에 따른 교수님 리스트

    4학년을 선택할 시, A반의 이름은 J반으로 변경되며 B반과 C반은 클릭할 수 없어진다.
    """
    # 전역변수 수정을 위한 global
    # subject_1, subject_2, subject_3, subject_4는 각 학년의 과목이다.
    global subject_1, subject_2, subject_3, subject_4
    subList = []    # 과목 리스트
    proList = []    # 교수 리스트
    print(grade.get())
    if str(grade.get()) == '4': # 4학년을 선택할 시, A반의 이름은 J반으로 변경되며 B반과 C반은 클릭할 수 없어진다.
        rdo_class_A.config(text="J반", variable=student_class, value=4, state=tk.NORMAL)     # A반 -> J반 변경
        rdo_class_B.config(text="B반", variable=student_class, value=2, state=tk.DISABLED)   # B반 비활성화
        rdo_class_C.config(text="B반", variable=student_class, value=2, state=tk.DISABLED)   # C반 비활성화
    else:   # 1, 2, 3 학년 선택 시
        rdo_class_A.config(text="A반", variable=student_class, value=1, state=tk.NORMAL)     # J반 -> A반
        rdo_class_B.config(text="B반", variable=student_class, value=2, state=tk.NORMAL)     # B반 활성화
        rdo_class_C.config(text="C반", variable=student_class, value=3, state=tk.NORMAL)     # C반 활성화

    # 서버 통신
    fileName = str(grade.get()) + '_subject'        # 파일 이름
    client_socket.send(fileName.encode("UTF-8"))    # 파일 이름 전송
    print("{0} 서버에 전송".format(str(grade.get())))

    data = client_socket.recv(2048).decode("UTF-8") # 파일 내용 수신
    print("{} 서버에서 받음".format(data))

    if data == 'ERROR': # ERROR을 수신받을 경우 에러 메세지 박스 출력
        showMessageBox('recvERROR')
    else:
        if str(grade.get()) == '1':             # 1학년 선택 시
            subject_1 = subject_data_dic(data)  # subject_1에 1학년 과목 정보 저장
            for key in subject_1.keys():        # subject_1의 키 값(과목)을 subList에 저장
                subList.append(key)
            for value in subject_1.values():    # subject_1의 값(교수님 성함)을 proList에 저장
                proList.append(value)
        elif str(grade.get()) == '2':           # 2학년 선택 시
            subject_2 = subject_data_dic(data)  # subject_2에 2학년 과목 정보 저장
            for key in subject_2.keys():        # subject_2의 키 값(과목)을 subList에 저장
                subList.append(key)
            for value in subject_2.values():    # subject_2의 값(교수님 성함)을 proList에 저장
                proList.append(value)
        elif str(grade.get()) == '3':           # 3학년 선택 시
            subject_3 = subject_data_dic(data)  # subject_3에 3학년 과목 정보 저장
            for key in subject_3.keys():        # subject_3의 키 값(과목)을 subList에 저장
                subList.append(key)
            for value in subject_3.values():    # subject_3의 값(교수님 성함)을 proList에 저장
                proList.append(value)
        elif str(grade.get()) == '4':           # 4학년 선택 시
            subject_4 = subject_data_dic(data)  # subject_4에 4학년 과목 정보 저장
            for key in subject_4.keys():        # subject_4의 키 값(과목)을 subList에 저장
                subList.append(key)
            for value in subject_4.values():    # subject_4의 값(교수님 성함)을 proList에 저장
                proList.append(value)

        # 중복 제거
        newSubList = []
        for v in subList:
            if v not in newSubList:
                newSubList.append(v)
        newProList = []
        for v in proList:
            if v not in newProList:
                newProList.append(v)

        # region 추후 진행할 내용
        # subList = newSubList
        # proList = newProList

        # combo_Sub.config(height=5, values=subList, state="readonly" )
        # combo_pro.config(height=5, values=proList, state="readonly")
        # combo_Sub.set(subList[0])
        # combo_pro.set(proList[0])
        # endregion


def subject_data_dic(data):
    """
    서버 측에서 수신받은 정보(문자열)를 변환(딕셔너리)해주는 함수
    리스트를 딕셔너리로 변경해주는 함수
    여러 곳에서 사용할 것 같아 함수로 빼 놓음
    """
    content_list = []   # List
    content_dict = {}   # Dict
    for line in data.split(','):    # ','로 문자열 분리
        for content in line.split(' '): # ' ' 띄어쓰기로 문자열 분리
            content_list.append(content)    # 분리한 문자열 저장
    for i in range(0, len(content_list)-1, 2):  # 리스트를 딕셔너리로 변환
        print(content_list[i], content_list[i + 1])
        content_dict[content_list[i]] = content_list[i + 1]
    return content_dict # 변환한 딕셔너리 반환


def class_start():
    """
    학년과 반을 선택하여 조회하게 되면
    해당 되는 시간표(데이터)를 서버에서 받아온다.
    """
    global grade, student_class # 전역 변수 grade(학년), student_class(반)을 수정하기 위한 global
    grade_ = grade.get()            # radio 버튼으로 입력한 값(학년)을 가져온다.
    class_ = student_class.get()    # radio 버튼으로 입력한 값(반)을 가져온다.

    if grade_ == 0:     # 학년을 선택하지 않은 경우
        showMessageBox('inputGrade')    # 학년을 선택하라는 메세지 출력
    elif class_ == 0:   # 반을 선택하지 않은 경우
        showMessageBox('inputClass')    # 반을 선택하라는 메세지 출력
    else:
        sendData = ''           # 서버에 전송할 문자열
        if grade_ == 1:         # 1학년인 경우
            sendData += '1-'
        elif grade_ == 2:       # 2학년인 경우
            sendData += '2-'
        elif grade_ == 3:       # 3학년인 경우
            sendData += '3-'
        elif grade_ == 4:       # 4학년인 경우
            sendData += '4-'

        if grade_ == 4:         # 4학년인 경우 J반 밖에 없으므로(프로젝트 제외) J반 추가 입력
            sendData += 'J'
        else:
            if class_ == 1:     # A반인 경우
                sendData += 'A'
            elif class_ == 2:   # B반인 경우
                sendData += 'B'
            elif class_ == 3:   # C반인 경우
                sendData += 'C'

        client_socket.send(sendData.encode("UTF-8"))    # 서버에 전송
        print('send: {}'.format(sendData.encode("UTF-8")))

        recvData = client_socket.recv(2048).decode("UTF-8") # 수신 정보
        print('recv: {}'.format(recvData))

        # 시간표 출력
        schedule_tree_list = schedule_make_list(recvData)

        for i in range(len(schedule_tree_list)):    # 각 데이터를 시간에 맞게 시간표에 출력한다.
            treeview.item(str(i) + '번', values=schedule_tree_list[i])


def schedule_make_list(data):
    """
    서버에서 받아온 문자열 형태의 시간표를
    treeview로 출력하기 위한 형태(리스트, 튜플)로 변경해 주는 함수.
    """
    content_list = list()   # 1차로 문자열을 리스트로 변환
    for line in data.split(','):    # ',' 기준으로 분리
        content_list2 = list()
        if line == '':  # 공백일 경우 종료.
            break
        content_list2.append(line)  # 분리한 문자열을 리스트에 저장.
        content_list.append(content_list2)  # 분리한 문자열의 리스트를 append(2차원 리스트)

    conv_list = list()  # 각 데이터를 계산하기 쉽게 변환 ex) 월 -> 0, 화 -> 1
    for line in content_list:
        content_list = []
        dummy_list = line[0]
        for word in dummy_list.split('-'): # '-'를 기준으로 문자열 분리
            if word == '월':     # 월요일
                word = 0
            elif word == '화':   # 화요일
                word = 1
            elif word == '수':   # 수요일
                word = 2
            elif word == '목':   # 목요일
                word = 3
            elif word == '금':   # 금요일
                word = 4
            try:    # 만약 word의 값이 교시를 나타낼 경우 '교시'를 제거한다.
                word = word.replace('교시', '')
            except: # 교시가 아닌 과목명, 교수님 성함 등일 경우 위 try문을 건너뛴다.
                pass
            content_list.append(word)   # 변환한 값을 list에 삽입한다.
        conv_list.append(content_list)  # 2차원 리스트로 만들어 준다.

    conv2_list = list() # treeview 형식에 맞게 변환한 list
    for c_list in conv_list:        # 계산하기 쉽게 변환한 리스트
        c_list_len = len(c_list)    # 리스트의 길이만큼 for문을 수행하기 위한 변수
        circle = c_list_len - 4     # 강의 시간를 제외한 값을 사용하기 위함
        i = 4                       # 강의 시간만을 사용하기 위함
        for _ in range(circle):
            dummy_list = list()
            dummy_list.append(c_list[0])    # 강의 요일 삽입
            dummy_list.append(c_list[1])    # 강의명 삽입
            dummy_list.append(c_list[2])    # 강의 장소 삽입
            dummy_list.append(c_list[3])    # 강의 교수님 삽입
            dummy_list.append(c_list[i])    # 강의 시간 삽입 (for문으로 시간마다 삽입)
            i += 1
            conv2_list.append(dummy_list)   # 위에서 삽입한 내용을 conv2_list에 삽입.

    schedule_tree_list = list() # treeview 형식에 맞는 리스트
    for i in range(len(time_list)): # 0교시 ~ 16교시
        schedule_tree_list.append(['', '', '', '', '']) # 빈 리스트 생성

    for c2_list in conv2_list:  # codeline 205줄의 리스트(형식에 맞게 변환한 리스트)를 삽입
        schedule_tree_list[int(c2_list[4])][int(c2_list[0])] = c2_list[1]

    return schedule_tree_list   # 형식에 맞게 변환된 리스트를 반환한다.

# region 추후 진행할 내용
# def sub_start():
#     """
#     과목을 선택하고 조회하게 되면
#     해당 과목에 대한 시간표를 서버에서 받아오는 함수
#     """
#     print('sub_start')
#     pass
#
#
# def pro_start():
#     """
#     교수님을 선택하고 조회하게 되면
#     해당 교수에 대한 시간표를 서버에서 받아오는 함수
#     """
#     print('pro_start')
#     pass
# endregion


def showMessageBox(message):
    """
    메세지를 출력해주는 함수
    """
    if message == 'inputGrade':     # 학년을 입력하지 않은 경우
        messagebox.showerror('에러', '학년을 선택해 주십시오.')
    elif message == 'inputClass':   # 반을 입력하지 않은 경우
        messagebox.showerror('에러', '반을 선택해 주십시오.')
    elif message == 'recvERROR':    # 전송/수신 관련 에러일 경우
        messagebox.showerror('에러', '해당 파일을 찾을 수 없습니다.')


def exitTkinter():
    """
    프로그램 종료 버튼을 누를 시 실행되는 함수
    """
    choice = messagebox.askyesno('종료', '프로그램을 종료하시겠습니까?')   # 프로그램 종료 여부 확인
    if choice:  # 확인 버튼 시 실행
        root.destroy()  # GUI 종료


if __name__ == '__main__':

    IP = 'localhost'    # IP(127.0.0.1)
    PORT = 9008         # PORT(9008)

    client_socket = socket(AF_INET, SOCK_STREAM)    # IPv4, TCP 통신 선언
    client_socket.connect((IP, PORT))               # 서버와 연결
    print("서버와 연결 확인\n\tIP: {0}\n\tPORT: {1}".format(IP, PORT))


    # region main(root) tkinter
    root = tk.Tk()  # GUI 생성
    root.title("강의 시간표 검색 프로그램")
    root.geometry('800x800')
    root.resizable(False, False)    # GUI 사이즈 변경 불가능하게 설정.

    btnExit = ttk.Button(root, text="종료", command=exitTkinter)  # 종료 버튼 생성
    # endregion


    # region 전역변수
    subject_1 = {}  # 1학년 과목 정보를 담을 딕셔너리 {과목:교수님}
    subject_2 = {}  # 2학년 과목 정보를 담을 딕셔너리
    subject_3 = {}  # 3학년 과목 정보를 담을 딕셔너리
    subject_4 = {}  # 4학년 과목 정보를 담을 딕셔너리

    grade = tk.IntVar() # 학년 정보를 담을 변수
    student_class = tk.IntVar()  # 1=A, 2=B, 3=C, 0=ERROR
    # endregion


    # region tab
    nb_tab = ttk.Notebook()         # 탭 제작
    main_tab = ttk.Frame(nb_tab)    # 메인 탭(정보)
    class_tab = ttk.Frame(nb_tab)   # 반 시간표
    # sub_tab = ttk.Frame(nb_tab)   # 과목 시간표
    # pro_tab = ttk.Frame(nb_tab)   # 교수님 시간표
    # help_tab = ttk.Frame(nb_tab)  # 도움말 탭 (메뉴바로 이동)
    nb_tab.add(main_tab, text="index")      # 메인 탭
    nb_tab.add(class_tab, text="반 검색")     # 반 시간표 검색 탭

    # region 추후 진행할 내용
    # nb_tab.add(sub_tab, text="과목 검색")    # 과목 시간표 검색 탭
    # nb_tab.add(pro_tab, text="교수 검색")    # 교수 시간표 검색 탭
    # endregion

    # nb_tab.add(help_tab, text="사용 설명")   # 도움말 탭(메뉴바로 이동)
    nb_tab.pack(fill='both')    # 탭 pack
    # endregion


    # region menubar
    m_menubar = tk.Menu(root)   # 메뉴바 생성
    m_help = tk.Menu(m_menubar, tearoff=0)  # 도움말 메뉴 생성
    m_menubar.add_cascade(label='도움말', menu=m_help) # 도움말 삽입
    m_help.add_command(label='도움말', command=help_window)    # 도움말 클릭할 시 help_window() 실행
    # endregion


    # region main_tab
    # 메인텝에 들어갈 레이블 생성
    lbl_main_about = ttk.Label(main_tab, text="컴퓨터정보과 3학년 A반 202044021 이준혁")
    lbl_main_content = ttk.Label(main_tab, text="TCP:IP 기말고사 과제물\n시간표 조회 프로그램")
    lbl_main_content2 = ttk.Label(main_tab, text="각 반을 검색하여 해당 시간표를 조회하는 프로그램.\n서버 측에서 시간표를 보내주어 클라이언트에서 출력해준다.")

    lbl_main_about.grid(row=0, column=0)
    lbl_main_content.grid(row=1, column=0, sticky=tk.W)
    lbl_main_content2.grid(row=2, column=0, sticky=tk.W, pady=15)
    # endregion


    # region class_tab
    # 학년 선택 radio 버튼
    lbl_grade = ttk.Label(class_tab, text="학년 : ")
    rdo_grade_1 = ttk.Radiobutton(class_tab, text="1학년", variable=grade, value=1, command=combo_print, width=5)
    rdo_grade_2 = ttk.Radiobutton(class_tab, text="2학년", variable=grade, value=2, command=combo_print, width=5)
    rdo_grade_3 = ttk.Radiobutton(class_tab, text="3학년", variable=grade, value=3, command=combo_print, width=5)
    rdo_grade_4 = ttk.Radiobutton(class_tab, text="4학년", variable=grade, value=4, command=combo_print, width=5)

    # 반 선택 radio 버튼
    lbl_class = ttk.Label(class_tab, text="반 : ")
    rdo_class_A = ttk.Radiobutton(class_tab, text="A반", variable=student_class, value=1)
    rdo_class_B = ttk.Radiobutton(class_tab, text="B반", variable=student_class, value=2)
    rdo_class_C = ttk.Radiobutton(class_tab, text="C반", variable=student_class, value=3)

    # 조회 버튼
    btn_class_start = ttk.Button(class_tab, text="조회", command=class_start)

    # 레이블, 라디오 버튼, 조회 버튼 삽입
    lbl_grade.grid(row=0, column=0, sticky=tk.W)
    rdo_grade_1.grid(row=1, column=0, sticky=tk.W)
    rdo_grade_2.grid(row=1, column=1, sticky=tk.W)
    rdo_grade_3.grid(row=1, column=2, sticky=tk.W)
    rdo_grade_4.grid(row=1, column=3, sticky=tk.W)
    lbl_class.grid(row=3, column=0, sticky=tk.W)
    rdo_class_A.grid(row=4, column=0, sticky=tk.W)
    rdo_class_B.grid(row=4, column=1, sticky=tk.W)
    rdo_class_C.grid(row=4, column=2, sticky=tk.W)
    # btn_class_start.grid(row=5, column=10, sticky=tk.E)
    btn_class_start.place(x=325, y=100)
    # endregion

    # region 추후 진행할 내용
    # region sub_tab
    # lbl_sub_grade = ttk.Label(sub_tab, text="학년: ")
    # rdo_sub_grade_1 = ttk.Radiobutton(sub_tab, text="1학년", variable=grade, value=1, command=combo_print, width=5)
    # rdo_sub_grade_2 = ttk.Radiobutton(sub_tab, text="2학년", variable=grade, value=2, command=combo_print, width=5)
    # rdo_sub_grade_3 = ttk.Radiobutton(sub_tab, text="3학년", variable=grade, value=3, command=combo_print, width=5)
    # rdo_sub_grade_4 = ttk.Radiobutton(sub_tab, text="4학년", variable=grade, value=4, command=combo_print, width=5)
    #
    # lbl_sub_grade.grid(row=0, column=0, sticky=tk.W)
    # rdo_sub_grade_1.grid(row=1, column=0)
    # rdo_sub_grade_2.grid(row=1, column=1)
    # rdo_sub_grade_3.grid(row=1, column=2)
    # rdo_sub_grade_4.grid(row=1, column=3)
    #
    # combo_Sub = ttk.Combobox(sub_tab)
    # subInitList = ['학년을 선택해 주십시오.']
    # combo_Sub.config(height=5, values=subInitList, state="readonly")
    # combo_Sub.set(subInitList[0])
    # combo_Sub.place(x=0, y=45)
    # # combo_Sub.grid(row=2, column=0)
    # btn_sub_start = ttk.Button(sub_tab, text="조회", command=sub_start)
    # btn_sub_start.place(x=325, y=100)
    # # endregion
    #
    # # region pro_tab
    # lbl_pro = ttk.Label(pro_tab, text="학년: ")
    # rdo_pro_grade_1 = ttk.Radiobutton(pro_tab, text="1학년", variable=grade, value=1, command=combo_print, width=5)
    # rdo_pro_grade_2 = ttk.Radiobutton(pro_tab, text="2학년", variable=grade, value=2, command=combo_print, width=5)
    # rdo_pro_grade_3 = ttk.Radiobutton(pro_tab, text="3학년", variable=grade, value=3, command=combo_print, width=5)
    # rdo_pro_grade_4 = ttk.Radiobutton(pro_tab, text="4학년", variable=grade, value=4, command=combo_print, width=5)
    #
    # lbl_pro.grid(row=0, column=0, columnspan=4, sticky=tk.W)
    # rdo_pro_grade_1.grid(row=1, column=0)
    # rdo_pro_grade_2.grid(row=1, column=1)
    # rdo_pro_grade_3.grid(row=1, column=2)
    # rdo_pro_grade_4.grid(row=1, column=3)
    #
    # combo_pro = ttk.Combobox(pro_tab)
    # proInitList = ['학년을 선택해 주십시오.']
    # combo_pro.config(height=5, values=proInitList, state="readonly")
    # combo_pro.set(proInitList[0])
    # combo_pro.place(x=0, y=45)
    # # combo_pro.grid(row=2, column=0)
    # btn_pro_start = ttk.Button(pro_tab, text="조회", command=pro_start)
    # btn_pro_start.place(x=325, y=100)
    # endregion
    # endregion

    # region treeview 시간표
    # 시간표 생성
    treeview = ttk.Treeview(root, columns=["one", "two", "three", "four", "five"],
                            displaycolumns=["one", "two", "three", "four", "five"], height=18)
    treeview.pack()

    # 각 컬럼 설정, 컬러 ㅁ이름, 컬럼 넓이, 정렬
    treeview.column("#0", width=200, anchor="center")
    treeview.heading("#0", text="시간", anchor="center")

    treeview.column("#1", width=120, anchor="center")
    treeview.heading("one", text="월", anchor="center")

    treeview.column("#2", width=120, anchor="center")
    treeview.heading("two", text="화", anchor="center")

    treeview.column("#3", width=120, anchor="center")
    treeview.heading("three", text="수", anchor="center")

    treeview.column("#4", width=120, anchor="center")
    treeview.heading("four", text="목", anchor="center")

    treeview.column("#5", width=120, anchor="center")
    treeview.heading("five", text="금", anchor="center")

    # region treeview 기본 베이스
    # 빈 시간표 생성 (초기 출력)
    time_list = []
    init_time = datetime.datetime(100, 1, 1, 8, 55, 00)
    new_time = init_time + datetime.timedelta(minutes=5)
    time_list.append('0교시\t08:00 ~ 08:50')

    for i in range(1, 17):  # 시간 삽입
        init_time += datetime.timedelta(minutes=5)  # 쉬는 시간 5분
        end_time = init_time + datetime.timedelta(minutes=50)   # 종료 시간은 시작 시간의 50분을 추가한다.
        hour = str(init_time.hour)
        minute = str(init_time.minute)
        end_hour = str(end_time.hour)
        end_minute = str(end_time.minute)
        if len(hour) == 1:  # 시작 시간을 두 자리 수로 변환 ex) 9시 -> 09시
            hour = '0' + str(init_time.hour)
        if len(minute) == 1:    # 시작 시간의 분을 두 자리 수로 변환 ex) 5분 -> 05분
            minute = '0' + str(init_time.minute)
        if len(end_hour) == 1:  # 종료 시간 두 자리 수로 변환
            end_hour = '0' + str(end_time.hour)
        if len(end_minute) == 1:    # 종료 시간의 분을 두 자리 수로 변환
            end_minute = '0' + str(end_time.minute)
        time_list.append(str(i)+'교시\t'  # 문자열 생성
                         + hour + ':' + minute + ' ~ '
                         + end_hour + ':' + end_minute)
        init_time += datetime.timedelta(minutes=50)

    array = np.empty((0, 5), str)

    tree_list = []  # treeview 형식의 리스트
    for i in range(len(time_list)):
        tree_list.append(('', '', '', '', ''))  # 리스트에 공백의 튜플 삽입
        treeview.insert('', 'end', text=time_list[i], values=tree_list[i], iid=str(i) + '번')
    # endregion

    # 날씨
    weather_tab = ttk.Notebook()    # 날씨 데이터를 출력할 탭 생성
    weather_frame = ttk.Frame(weather_tab)
    weather_tab.add(weather_frame, text='날씨')

    print("로딩중입니다...")  # 날씨 데이터를 받아오는 시간 동안 로딩중이라는 콘솔 안내문 출력

    client_socket.send('weather'.encode("UTF-8"))   # 날씨 데이터를 받기 위해 weather 문자열 전송
    print("{0} 서버에 전송".format(str('weather')))

    weather_data = client_socket.recv(2048).decode("UTF-8") # 수신받은 날씨 데이터 정보
    print("{} 서버에서 받음".format(weather_data))

    weather_data_list_ = weather_data.split(',')    # 날씨 데이터 정보 문자열을 ','로 분리
    print('weather_data_list_: ', weather_data_list_)
    weather_data_list = list() # 출력에 사용할 데이터
    for data in weather_data_list_: # 날씨 데이터 정보를 한번 더 분리 하기 위한 반복문
        if data == '':  # 공백일 경우 넘긴다.
            continue
        weather_data_list.append(data.split(':'))   # ':'로 문자열 한 번 더 분리
    print('weather_data_list: ', weather_data_list)

    # 날씨 정보 출력
    weather_tab.pack(fill='both')
    lbl_weather_title = ttk.Label(weather_frame, text="용현동 날씨: ")
    lbl_weather_sky = ttk.Label(weather_frame, text="하늘: ")
    lbl_weather_sky_value = ttk.Label(weather_frame, text=weather_data_list[2][1])
    lbl_weather_tmp = ttk.Label(weather_frame, text="온도: ")
    lbl_weather_tmp_value = ttk.Label(weather_frame, text=weather_data_list[3][1] + '℃')
    lbl_weather_hum = ttk.Label(weather_frame, text="습도: ")
    lbl_weather_hum_value = ttk.Label(weather_frame, text=weather_data_list[4][1] + '%')
    lbl_weather_rain = ttk.Label(weather_frame, text="강수량: ")
    lbl_weather_rain_value = ttk.Label(weather_frame, text=weather_data_list[1][1])
    lbl_weather_pty = ttk.Label(weather_frame, text="강수 형태: ")
    lbl_weather_pty_value = ttk.Label(weather_frame, text=weather_data_list[0][1])

    lbl_weather_title.grid(row=0, column=0, columnspan=1)
    lbl_weather_sky.grid(row=1, column=0)
    lbl_weather_sky_value.grid(row=1, column=1)
    lbl_weather_tmp.grid(row=2, column=0)
    lbl_weather_tmp_value.grid(row=2, column=1)
    lbl_weather_hum.grid(row=3, column=0)
    lbl_weather_hum_value.grid(row=3, column=1)
    lbl_weather_rain.grid(row=4, column=0)
    lbl_weather_rain_value.grid(row=4, column=1)
    lbl_weather_pty.grid(row=5, column=0)
    lbl_weather_pty_value.grid(row=5, column=1)
    # endregion

    # 종료버튼
    btnExit.pack()

    # tkinter 시작
    root.config(menu=m_menubar)
    root.mainloop()

    # Window (GUI)가 종료되면 서버에 exit 문자열을 전송하게 되고, 서버는 이를 통해 현재 클라이언트와 통신을 끊는다.
    client_socket.send(str('exit').encode("UTF-8"))
    print("{0} 서버에 전송".format(str('exit')))

    # 클라이언트 소켓을 종료한다.
    client_socket.close()
    print("client 종료")