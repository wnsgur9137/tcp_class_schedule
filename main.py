import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from socket import *
import numpy as np
import time


def createNewWindow():
    """
    새로운 윈도우 창을 만들 때 사용하는 함수.
    labelExample =
    buttonExample =
    """
    newWindow = tk.Toplevel(root)
    labelExample = tk.Label(newWindow, text = "New Window")
    buttonExample = tk.Button(newWindow, text = "New Window button")

    labelExample.pack()
    buttonExample.pack()


def help_window():
    """
    도움말 윈도우를 만드는 함수.
    helpWindow
    프로그램을 어떻게 사용하는지를 안내하는 윈도우다.
    """
    helpWindow = tk.Toplevel(root)
    helpWindow.title('강의 시간표 검색 프로그램 도움말')
    helpWindow.geometry('400x300')
    lbl_help = ttk.Label(helpWindow, text="도움말")
    lbl_help_content = ttk.Label(helpWindow, text="블라블라블라")

    lbl_help.pack()
    lbl_help_content.pack()


def combo_print():
    """
    학년을 선택함에 따라 맞춰 변하는 과목, 교수님 목록을 변경하기 위한 함수이다.
    subList = 학년에 따른 과목 리스트
    proList = 학년에 따른 교수님 리스트

    4학년을 선택할 시, A반의 이름은 J반으로 변경되며 B반과 C반은 클릭할 수 없어진다.
    """
    global subject_1, subject_2, subject_3, subject_4
    subList = []
    proList = []
    print(grade.get())
    if str(grade.get()) == '4': # 4학년을 선택할 시, A반의 이름은 J반으로 변경되며 B반과 C반은 클릭할 수 없어진다.
        rdo_class_A.config(text="J반", variable=student_class, value=4, state=tk.NORMAL)
        rdo_class_B.config(text="B반", variable=student_class, value=2, state=tk.DISABLED)
        rdo_class_C.config(text="B반", variable=student_class, value=2, state=tk.DISABLED)
    else:
        rdo_class_A.config(text="A반", variable=student_class, value=1, state=tk.NORMAL)
        rdo_class_B.config(text="B반", variable=student_class, value=2, state=tk.NORMAL)
        rdo_class_C.config(text="C반", variable=student_class, value=3, state=tk.NORMAL)

    # 서버 통신
    fileName = str(grade.get()) + '_subject'
    client_socket.send(fileName.encode("UTF-8"))
    print("{0} 서버에 전송".format(str(grade.get())))

    data = client_socket.recv(2048).decode("UTF-8")
    print("{} 서버에서 받음".format(data))

    if data == 'ERROR':
        showMessageBox('recvERROR')
    else:
        if str(grade.get()) == '1':
            subject_1 = subject_data_dic(data)
            for key in subject_1.keys():
                subList.append(key)
            for value in subject_1.values():
                proList.append(value)
        elif str(grade.get()) == '2':
            subject_2 = subject_data_dic(data)
            for key in subject_2.keys():
                subList.append(key)
            for value in subject_2.values():
                proList.append(value)
        elif str(grade.get()) == '3':
            subject_3 = subject_data_dic(data)
            for key in subject_3.keys():
                subList.append(key)
            for value in subject_3.values():
                proList.append(value)
        elif str(grade.get()) == '4':
            subject_4 = subject_data_dic(data)
            for key in subject_4.keys():
                subList.append(key)
            for value in subject_4.values():
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

        subList = newSubList
        proList = newProList

        combo_Sub.config(height=5, values=subList, state="readonly")
        combo_pro.config(height=5, values=proList, state="readonly")
        combo_Sub.set(subList[0])
        combo_pro.set(proList[0])


def subject_data_dic(data):
    """
    리스트를 딕셔너리로 변경해주는 함수
    여러 곳에서 사용할 것 같아 함수로 빼 놓음
    """
    content_list = []
    content_dict = {}
    for line in data.split(','):
        for content in line.split(' '):
            content_list.append(content)
    for i in range(0, len(content_list)-1, 2):
        print(content_list[i], content_list[i + 1])
        content_dict[content_list[i]] = content_list[i + 1]
    return content_dict


def class_start():
    """
    학년과 반을 선택하여 조회하게 되면
    해당 되는 시간표(데이터)를 서버에서 받아온다.
    """
    global grade, student_class
    grade_ = grade.get()
    class_ = student_class.get()

    if grade_ == 0:
        showMessageBox('inputGrade')
    elif class_ == 0:
        showMessageBox('inputClass')

    recvData = ''
    if grade_ == 1:
        recvData += '1-'
    elif grade_ == 2:
        recvData += '2-'
    elif grade_ == 3:
        recvData += '3-'
    elif grade_ == 4:
        recvData += '4-'

    if class_ == 1:
        recvData += 'A'
    elif class_ == 2:
        recvData += 'B'
    elif class_ == 3:
        recvData += 'C'
    elif class_ == 4:
        recvData += 'J'

    client_socket.send(recvData.encode("UTF-8"))
    print('send: {}'.format(recvData.encode("UTF-8")))

    data = client_socket.recv(2048).decode("UTF-8")
    print('recv: {}'.format(data))

    tree_list = schedule_make_list(data)
    print(tree_list)
    #
    # for i in range(len(tree_list)):
    #     print(tree_list[i][0])
    #     try:
    #         print(tree_list[i][4])
    #         print(tree_list[i][5])
    #         print(tree_list[i][6])
    #     except:
    #         pass


    # treelist = [("Tom", 80, 3), ("Bani", 71, 5), ("Boni", 90, 2), ("Dannel", 78, 4), ("Minho", 93, 1)]
    #
    # # 표에 데이터 삽입
    # for i in range(len(treelist)):
    #     treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i) + "번")


def schedule_make_list(data):
    """
    서버에서 받아온 시간표는 문자열이기 때문에,
    이를 리스트로 변경하여 주는 함수이다.
    """
    content_list = []
    for line in data.split(','):
        content_list2 = []
        if line == '':
            break
        content_list2.append(line)
        content_list.append(content_list2)

    tree_list = []
    for line in content_list:
        content_list = []
        dummy_list = line[0]
        for word in dummy_list.split('-'):
            content_list.append(word)
        tree_list.append(tuple(content_list))
    return tree_list


def sub_start():
    """
    과목을 선택하고 조회하게 되면
    해당 과목에 대한 시간표를 서버에서 받아오는 함수
    """
    print('sub_start')
    pass


def pro_start():
    """
    교수님을 선택하고 조회하게 되면
    해당 교수에 대한 시간표를 서버에서 받아오는 함수
    """
    print('pro_start')
    pass


def showMessageBox(message):
    """
    메세지를 출력해주는 함수
    """
    if message == 'inputGrade':
        messagebox.showerror('에러', '학년을 선택해 주십시오.')
    elif message == 'inputClass':
        messagebox.showerror('에러', '반을 선택해 주십시오.')
    elif message == 'recvERROR':
        messagebox.showerror('에러', '해당 파일을 찾을 수 없습니다.')


def exitTkinter():
    """
    프로그램 종료 버튼을 누를 시 실행되는 함수
    """
    choice = messagebox.askyesno('종료', '프로그램을 종료하시겠습니까?')
    if choice:
        root.destroy()


if __name__ == '__main__':

    IP = 'localhost'
    PORT = 9008

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print("서버와 연결 확인\n\tIP: {0}\n\tPORT: {1}".format(IP, PORT))


    # region main(root) tkinter
    root = tk.Tk()
    root.title("강의 시간표 검색 프로그램")
    root.geometry('800x800')
    root.resizable(False, False)

    btnExit = ttk.Button(root, text="종료", command=exitTkinter)
    # endregion


    # region 전역변수
    subject_1 = {}
    subject_2 = {}
    subject_3 = {}
    subject_4 = {}

    grade = tk.IntVar()
    student_class = tk.IntVar()  # 1=A, 2=B, 3=C, 0=ERROR
    # endregion


    # region tab
    nb_tab = ttk.Notebook()
    main_tab = ttk.Frame(nb_tab)
    class_tab = ttk.Frame(nb_tab)
    sub_tab = ttk.Frame(nb_tab)
    pro_tab = ttk.Frame(nb_tab)
    # help_tab = ttk.Frame(nb_tab)
    nb_tab.add(main_tab, text="index")
    nb_tab.add(class_tab, text="반 검색")
    nb_tab.add(sub_tab, text="과목 검색")
    nb_tab.add(pro_tab, text="교수 검색")
    # nb_tab.add(help_tab, text="사용 설명")
    nb_tab.pack(fill='both')
    # endregion


    # region menubar
    m_menubar = tk.Menu(root)
    m_file = tk.Menu(m_menubar, tearoff=0)
    m_menubar.add_cascade(label='', menu=m_file)
    m_file.add_command(label='new Window', command=createNewWindow)

    m_help = tk.Menu(m_menubar, tearoff=0)
    m_menubar.add_cascade(label='도움말', menu=m_help)
    m_help.add_command(label='도움말', command=help_window)
    # endregion


    # region main_tab
    lbl_main_about = ttk.Label(main_tab, text="컴퓨터정보과 3학년 A반 202044021 이준혁")
    lbl_main_content = ttk.Label(main_tab, text="TCP:IP 기말고사 과제물\n시간표 조회 프로그램")
    lbl_main_content2 = ttk.Label(main_tab, text="각 반, 과목, 교수를 검색하여 해당 시간표를 조회하는 프로그램.\n서버 측에서 시간표를 보내주어 클라이언트에서 출력해준다.")

    lbl_main_about.grid(row=0, column=0)
    lbl_main_content.grid(row=1, column=0, sticky=tk.W)
    lbl_main_content2.grid(row=2, column=0, sticky=tk.W, pady=15)
    # endregion


    # region class_tab
    lbl_grade = ttk.Label(class_tab, text="학년 : ")
    rdo_grade_1 = ttk.Radiobutton(class_tab, text="1학년", variable=grade, value=1, command=combo_print, width=5)
    rdo_grade_2 = ttk.Radiobutton(class_tab, text="2학년", variable=grade, value=2, command=combo_print, width=5)
    rdo_grade_3 = ttk.Radiobutton(class_tab, text="3학년", variable=grade, value=3, command=combo_print, width=5)
    rdo_grade_4 = ttk.Radiobutton(class_tab, text="4학년", variable=grade, value=4, command=combo_print, width=5)

    lbl_class = ttk.Label(class_tab, text="반 : ")
    rdo_class_A = ttk.Radiobutton(class_tab, text="A반", variable=student_class, value=1, command=class_start)
    rdo_class_B = ttk.Radiobutton(class_tab, text="B반", variable=student_class, value=2, command=class_start)
    rdo_class_C = ttk.Radiobutton(class_tab, text="C반", variable=student_class, value=3, command=class_start)

    btn_class_start = ttk.Button(class_tab, text="조회", command=class_start)

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


    # region sub_tab
    lbl_sub_grade = ttk.Label(sub_tab, text="학년: ")
    rdo_sub_grade_1 = ttk.Radiobutton(sub_tab, text="1학년", variable=grade, value=1, command=combo_print, width=5)
    rdo_sub_grade_2 = ttk.Radiobutton(sub_tab, text="2학년", variable=grade, value=2, command=combo_print, width=5)
    rdo_sub_grade_3 = ttk.Radiobutton(sub_tab, text="3학년", variable=grade, value=3, command=combo_print, width=5)
    rdo_sub_grade_4 = ttk.Radiobutton(sub_tab, text="4학년", variable=grade, value=4, command=combo_print, width=5)

    lbl_sub_grade.grid(row=0, column=0, sticky=tk.W)
    rdo_sub_grade_1.grid(row=1, column=0)
    rdo_sub_grade_2.grid(row=1, column=1)
    rdo_sub_grade_3.grid(row=1, column=2)
    rdo_sub_grade_4.grid(row=1, column=3)

    combo_Sub = ttk.Combobox(sub_tab)
    subInitList = ['학년을 선택해 주십시오.']
    combo_Sub.config(height=5, values=subInitList, state="readonly")
    combo_Sub.set(subInitList[0])
    combo_Sub.place(x=0, y=45)
    # combo_Sub.grid(row=2, column=0)
    btn_sub_start = ttk.Button(sub_tab, text="조회", command=sub_start)
    btn_sub_start.place(x=325, y=100)
    # endregion


    # region pro_tab
    lbl_pro = ttk.Label(pro_tab, text="교수님: ")
    rdo_pro_grade_1 = ttk.Radiobutton(pro_tab, text="1학년", variable=grade, value=1, command=combo_print, width=5)
    rdo_pro_grade_2 = ttk.Radiobutton(pro_tab, text="2학년", variable=grade, value=2, command=combo_print, width=5)
    rdo_pro_grade_3 = ttk.Radiobutton(pro_tab, text="3학년", variable=grade, value=3, command=combo_print, width=5)
    rdo_pro_grade_4 = ttk.Radiobutton(pro_tab, text="4학년", variable=grade, value=4, command=combo_print, width=5)

    lbl_pro.grid(row=0, column=0, columnspan=4, sticky=tk.W)
    rdo_pro_grade_1.grid(row=1, column=0)
    rdo_pro_grade_2.grid(row=1, column=1)
    rdo_pro_grade_3.grid(row=1, column=2)
    rdo_pro_grade_4.grid(row=1, column=3)

    combo_pro = ttk.Combobox(pro_tab)
    proInitList = ['교수님을 선택해 주십시오.']
    combo_pro.config(height=5, values=proInitList, state="readonly")
    combo_pro.set(proInitList[0])
    combo_pro.place(x=0, y=45)
    # combo_pro.grid(row=2, column=0)
    btn_pro_start = ttk.Button(pro_tab, text="조회", command=pro_start)
    btn_pro_start.place(x=325, y=100)
    # endregion


    # region treeview 시간표
    treeview = ttk.Treeview(root, columns=["one", "two", "three", "four", "five"],
                            displaycolumns=["one", "two", "three", "four", "five"], height=18)
    treeview.pack()

    # 각 컬럼 설정, 컬러 ㅁ이름, 컬럼 넓이, 정렬
    treeview.column("#0", width=200, anchor="center")
    treeview.heading("#0", text="시간", anchor="center")

    treeview.column("#1", width=100, anchor="center")
    treeview.heading("one", text="월", anchor="center")

    treeview.column("#2", width=100, anchor="center")
    treeview.heading("two", text="화", anchor="center")

    treeview.column("#3", width=100, anchor="center")
    treeview.heading("three", text="수", anchor="center")

    treeview.column("#4", width=100, anchor="center")
    treeview.heading("four", text="목", anchor="center")

    treeview.column("#5", width=100, anchor="center")
    treeview.heading("five", text="금", anchor="center")

    # region treeview 기본 베이스
    time_list = []
    init_time = datetime.datetime(100, 1, 1, 8, 55, 00)
    new_time = init_time + datetime.timedelta(minutes=5)
    time_list.append('0교시\t08:00 ~ 08:50')

    for i in range(1, 17):
        init_time += datetime.timedelta(minutes=5)
        end_time = init_time + datetime.timedelta(minutes=50)
        hour = str(init_time.hour)
        minute = str(init_time.minute)
        end_hour = str(end_time.hour)
        end_minute = str(end_time.minute)
        if len(hour) == 1:
            hour = '0' + str(init_time.hour)
        if len(minute) == 1:
            minute = '0' + str(init_time.minute)
        if len(end_hour) == 1:
            end_hour = '0' + str(end_time.hour)
        if len(end_minute) == 1:
            end_minute = '0' + str(end_time.minute)
        time_list.append(str(i)+'교시\t'
                         + hour + ':' + minute + ' ~ '
                         + end_hour + ':' + end_minute)
        init_time += datetime.timedelta(minutes=50)

    array = np.empty((0, 5), str)

    tree_list = []
    for i in range(len(time_list)):
        tree_list.append(('', '', '', '', ''))
        treeview.insert('', 'end', text=time_list[i], values=tree_list[i], iid=str(i) + '번')
    # endregion


    # 날씨
    weather_tab = ttk.Notebook()
    weather_frame = ttk.Frame(weather_tab)
    weather_tab.add(weather_frame, text='날씨')

    print("로딩중입니다...")

    client_socket.send('weather'.encode("UTF-8"))
    print("{0} 서버에 전송".format(str('weather')))

    weather_data = client_socket.recv(2048).decode("UTF-8")
    print("{} 서버에서 받음".format(weather_data))

    weather_data_list_ = weather_data.split(',')
    print('weather_data_list_: ', weather_data_list_)
    weather_data_list = list()
    for data in weather_data_list_:
        if data == '':
            continue
        weather_data_list.append(data.split(':'))
    print('weather_data_list: ', weather_data_list)

    weather_tab.pack(fill='both')
    lbl_weather_title = ttk.Label(weather_frame, text="용형동 날씨: ")
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