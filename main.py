import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from socket import *

def createNewWindow():
    newWindow = tk.Toplevel(root)
    labelExample = tk.Label(newWindow, text = "New Window")
    buttonExample = tk.Button(newWindow, text = "New Window button")

    labelExample.pack()
    buttonExample.pack()


def help_window():
    helpWindow = tk.Toplevel(root)
    helpWindow.title('강의 시간표 검색 프로그램 도움말')
    helpWindow.geometry('400x300')
    lbl_help = ttk.Label(helpWindow, text="도움말")
    lbl_help_content = ttk.Label(helpWindow, text="블라블라블라")

    lbl_help.pack()
    lbl_help_content.pack()


def class_start():
    pass


def sub_start():
    pass


def print_subject():
    global subject_1, subject_2, subject_3, subject_4
    subList = []

    # 서버 통신
    client_socket.send(str(grade.get()).encode("UTF-8"))
    print("{0} 서버에 전송".format(str(grade.get())))

    data = client_socket.recv(2048).decode("UTF-8")
    print("{} 서버에서 받음".format(data))

    if str(grade.get()) == '1':
        subject_1 = subject_data_dic(data)
        print('subject_1: ' ,subject_1)
        for keys in subject_1.keys():
            print('keys: ', keys, type(keys))
            subList.append(keys)
        print('subject_1: {}'.format(subject_1))
    elif str(grade.get()) == '2':
        subject_2 = subject_data_dic(data)
        for keys in subject_2.keys():
            subList.append(keys)
    elif str(grade.get()) == '3':
        subject_3 = subject_data_dic(data)
        for keys in subject_3.keys():
            print('keys: ', keys, type(keys))
            subList.append(keys)
    elif str(grade.get()) == '4':
        subject_4 = subject_data_dic(data)
        for keys in subject_4.keys():
            print('keys: ', keys, type(keys))
            subList.append(keys)

    print('subject_1: ', subject_1)
    print('subject_1.keys(): ', subject_1.keys())
    combo_Sub.config(height=5, values=subList, state="readonly")


def subject_data_dic(data):
    content_list = []
    content_dict = {}
    for line in data.split(','):
        for content in line.split(' '):
            content_list.append(content)
    for i in range(0, len(content_list)-1, 2):
        print(content_list[i], content_list[i + 1])
        content_dict[content_list[i]] = content_list[i + 1]
    return content_dict


def pro_start():
    pass


def exitTkinter():
    choice = messagebox.askyesno('종료', '프로그램을 종료하시겠습니까?')
    if choice == True:
        client_socket.send(str('exit').encode("UTF-8"))
        print("{0} 서버에 전송".format(str('exit')))
        root.destroy()


if __name__ == '__main__':

    IP = 'localhost'
    PORT = 9008

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print("서버와 연결 확인\n\tIP: {0}\n\tPORT: {1}".format(IP, PORT))

    # region 전역변수
    subject_1 = {}
    subject_2 = {}
    subject_3 = {}
    subject_4 = {}
    # endregion


    # region main(root) tkinter
    root = tk.Tk()
    root.title("강의 시간표 검색 프로그램")
    root.geometry('600x300')

    btnExit = ttk.Button(root, text="종료", command=exitTkinter)
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
    grade = tk.IntVar()
    lbl_grade = ttk.Label(class_tab, text="학년 : ")
    rdo_grade_1 = ttk.Radiobutton(class_tab, text="1학년", variable=grade, value=1)
    rdo_grade_2 = ttk.Radiobutton(class_tab, text="2학년", variable=grade, value=2)
    rdo_grade_3 = ttk.Radiobutton(class_tab, text="3학년", variable=grade, value=3)
    rdo_grade_4 = ttk.Radiobutton(class_tab, text="4학년", variable=grade, value=4)

    lbl_class = ttk.Label(class_tab, text="반 : ")
    student_class = tk.IntVar() # 1=A, 2=B, 3=C, 0=ERROR
    rdo_class_A = ttk.Radiobutton(class_tab, text="A반", variable=student_class, value=1)
    rdo_class_B = ttk.Radiobutton(class_tab, text="B반", variable=student_class, value=2)
    rdo_class_C = ttk.Radiobutton(class_tab, text="C반", variable=student_class, value=3)

    btn_class_start = ttk.Button(class_tab, text="조회", command=class_start)

    lbl_grade.grid(row=0, column=0)
    rdo_grade_1.grid(row=1, column=0)
    rdo_grade_2.grid(row=1, column=1)
    rdo_grade_3.grid(row=1, column=2)
    rdo_grade_4.grid(row=1, column=3)
    lbl_class.grid(row=3, column=0)
    rdo_class_A.grid(row=4, column=0)
    rdo_class_B.grid(row=4, column=1)
    rdo_class_C.grid(row=4, column=2)
    btn_class_start.grid(row=5, column=10, sticky=tk.E)
    # endregion


    # region sub_tab
    lbl_sub_grade = ttk.Label(sub_tab, text="학년: ")
    rdo_sub_grade_1 = ttk.Radiobutton(sub_tab, text="1학년", variable=grade, value=1, command=print_subject)
    rdo_sub_grade_2 = ttk.Radiobutton(sub_tab, text="2학년", variable=grade, value=2, command=print_subject)
    rdo_sub_grade_3 = ttk.Radiobutton(sub_tab, text="3학년", variable=grade, value=3, command=print_subject)
    rdo_sub_grade_4 = ttk.Radiobutton(sub_tab, text="4학년", variable=grade, value=4, command=print_subject)

    lbl_sub_grade.grid(row=0, column=0)
    rdo_sub_grade_1.grid(row=1, column=0)
    rdo_sub_grade_2.grid(row=1, column=1)
    rdo_sub_grade_3.grid(row=1, column=2)
    rdo_sub_grade_4.grid(row=1, column=3)

    combo_Sub = ttk.Combobox(sub_tab)
    subInitList = ['학년을 선택해 주십시오.']
    combo_Sub.config(height=5, values=subInitList, state="readonly")
    combo_Sub.set(subInitList[0])
    combo_Sub.grid(row=2, column=0)
    # endregion


    # region pro_tab
    lbl_pro = ttk.Label(pro_tab, text="교수님: ")
    rdo_pro_grade_1 = ttk.Radiobutton(pro_tab, text="1학년", variable=grade, value=1, command=print_subject)
    rdo_pro_grade_2 = ttk.Radiobutton(pro_tab, text="2학년", variable=grade, value=2, command=print_subject)
    rdo_pro_grade_3 = ttk.Radiobutton(pro_tab, text="3학년", variable=grade, value=3, command=print_subject)
    rdo_pro_grade_4 = ttk.Radiobutton(pro_tab, text="4학년", variable=grade, value=4, command=print_subject)

    lbl_pro.grid(row=0, column=0, columnspan=4)
    rdo_pro_grade_1.grid(row=1, column=0)
    rdo_pro_grade_2.grid(row=1, column=1)
    rdo_pro_grade_3.grid(row=1, column=2)
    rdo_pro_grade_4.grid(row=1, column=3)

    combo_pro = ttk.Combobox(pro_tab)
    proInitList = ['교수님을 선택해 주십시오.']
    combo_pro.config(height=5, values=proInitList, state="readonly")
    combo_pro.set(proInitList[0])
    combo_pro.grid(row=2, column=0)
    # endregion


    # region main pack
    nb_tab.pack(fill='both')
    btnExit.pack()
    # endregion


    # tkinter 시작
    root.config(menu=m_menubar)
    root.mainloop()

    client_socket.close()
    print("client 종료")