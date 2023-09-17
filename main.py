"""
Cogstruction: Optimizing cog arrays in Legends of Idleon
    Copyright (C) 2021 Michael P. Lane

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    2023/09/17 add GUI 
"""
import sys
import os

from constants import NUM_COGS_HORI, NUM_COGS_VERT, TOTAL_COORDS

import random
import numpy as np

from learning_algo import Iteration_Controller,learning_algo
from file_readers import read_cog_datas,read_empties_datas,read_flaggies_datas
from cog_factory import cog_factory
from cog_array_stuff import Empties_Set

import PySimpleGUI as sg
import webbrowser
import pandas as pd

import re

import base64

import datetime


#icon_path = get_icon_path("icon.png")
#print("Icon",icon_path)
#icon_data=open(icon_path,"rb")
#icon_data=base64.b64encode(icon_data.read())
#print(icon_data)
icon_data='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'

#print("start")
#print(sys.argv[0])
#print(__name__)
PWD=os.path.dirname(sys.argv[0])
#print(PWD)
txdata,keys=[],[]


def get_icon_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

def add_Coord(empties,cog_datas):
    cogs_goemetry = Empties_Set(empties).coords_list
    temp=list2mat(cogs_goemetry)
    cogs_goemetry=mat2list(temp)

    for i in range(len(cog_datas)-len(cogs_goemetry)):
        cogs_goemetry.append((i,None))
    #print(len(cogs_goemetry),len(cog_datas))

    #cog_dataframe=[data for data in cog_datas]
    cog_dataframe=pd.DataFrame(cog_datas)
    cog_dataframe["Pre-Coords"]=cogs_goemetry
    temp=[]
    for data in cog_dataframe.values.tolist():
        data={key:i for key,i in zip(cog_dataframe.keys(),data)}
        temp.append(data)
        #print(data)
    return temp,cog_dataframe
def mat2list(mat):
    out=[]
    y,x=mat.shape
    #print(x,y)
    for i in range(y-1,-1,-1):
        for j in range(x-1):
            #print(j,i)
            if(mat[i,j]!=0):
                out.append((j,i))
    return out
def list2mat(coord_list):
    out=np.zeros((NUM_COGS_VERT,NUM_COGS_HORI))
    #print(out)
    for t in coord_list:
        out[t.y,t.x]=1
    #print(out)
    return out
def creat_check_box(Initial_value,Characters):
    #print(URLs)
    if(len(Characters)!=0):
        check_box_list=[[name,t,id] for name,t,id in zip(Characters,Initial_value,Characters)]
        check_boxes=[[(sg.Checkbox(k,default=t,key=txt,enable_events=True,expand_x=True,expand_y=True))] for k,t,txt in check_box_list]
        check_boxes=sg.Column(check_boxes,scrollable=True,size=(100,300),expand_x=True,expand_y=True)
    else:
       check_boxes=sg.text("No data,please check CSV file",expand_x=True,expand_y=True) 
    return check_boxes

def active_sub_window(Check,Characters):
    # ------------ サブウィンドウ作成 ------------
    if(Characters is not None):
        if(len(Characters)!=0): 
            check_box=creat_check_box(Check,Characters)
        else:
            check_box=sg.Text("I have NOT fouded Character...",key="-T-MISS-",expand_x=True,expand_y=True)
    else:
        check_box=sg.Text("I have NOT fouded Character...",key="-T-MISS-",expand_x=True,expand_y=True)

    frame3=sg.Frame("Select Items",
        [
            [
                check_box
            ],
            [
                sg.Button(button_text='ok', font=('メイリオ',8), size=(12,1),enable_events=-True, key="-B-ITEMS-OK-"),
                sg.Button(button_text='Cancel', font=('メイリオ',8), size=(12,1),enable_events=-True, key="-B-ITEMS-CANCEL-")
            ]
        ] 
        ,expand_x=True,expand_y=True
    )
    sub_window = sg.Window("Sub window", [[frame3]]
                           , finalize=True
                           , resizable=True
                           #, size=(400, 300)
                           , titlebar_icon=icon_data
                           , icon=icon_data
                           )

    sub_window.set_icon(pngbase64=icon_data)
    while True:
        event, values = sub_window.read()
        #print("sub",event,values)
        if (event == sg.WIN_CLOSED or event == "Exit"):
            values=None
            break
        elif(event=="-B-ITEMS-CANCEL-"):
            values=None
            break           
        # OKが押された場合
        elif(event == "-B-ITEMS-OK-"):
            break
        #クローズボタンの処理
        if event is None:
            print('exit')
            values=None
            break   #exit loopk
    sub_window.close()
    return values


def write_Text(datas,f_name,OverWrite=True):
    if(OverWrite):
        f=open(f_name, 'w+',encoding='utf-8', errors='ignore')  # ファイルを読み書き両用でオープン        
    else:
        f=open(f_name, 'a+',encoding='utf-8', errors='ignore')  # ファイルを読み書き両用でオープン
    #print(urls)
    datas=datas.split("\n")
    for data in datas:
        #print("Add...",data)
        f.write("%s\r\n"%data)  # ファイル書き込み

if __name__ == "__main__":
    random.seed(133742069)

    inv_build_weight = 7000.0
    inv_flaggy_weight = 2000.0
    inv_exp_weight = 3.0
    pop_size = 2000
    num_restarts = 1
    prob_cross_breed = 0.5
    prob_one_point_mutation = 0.25
    prob_two_point_mutation = 0.25
    num_mutations = 800
    factor_base = 2
    max_factor = 4
    max_multiplier = 16
    req_running_total = 0.01
    max_running_total_len = 10
    min_generations = 100
    max_generations = 400

    cog_datas_filename =os.path.join(PWD,"cog_datas.csv")
    empties_datas_filename = os.path.join(PWD,"empties_datas.csv")
    flaggies_datas_filename = os.path.join(PWD,"flaggies_datas.csv")
    output_filename = os.path.join(PWD,"output.txt")

    fontset = ('Courier New', 16, 'underline')

    fontsize_text=10
    col_layout=sg.Frame("",[[
                sg.Column(
                    [
                        [
                            sg.Text("Cogstruction Data:")
                        ],
                        [
                            sg.Multiline(default_text=""
                                        ,font=('Meiryo UI',fontsize_text)
                                        ,size=(20,21)
                                        ,auto_size_text=True
                                        ,horizontal_scroll = True
                                        ,expand_x=True,expand_y=True
                                        ,key="-TX-COG-")
                        ],
                        [
                            sg.Button(button_text='Write COG', font=('メイリオ',fontsize_text-2), size=(12,1), key="-B-COGFILE-")
                        ]
                    ]
                    ,expand_x=True,expand_y=True
                )
                ,sg.Column(
                    [
                        [
                            sg.Text("Cogstruction Empties:")
                        ],
                        [
                            sg.Multiline(default_text=""
                                            ,font=('Meiryo UI',fontsize_text)
                                            ,size=(20,21)
                                            ,auto_size_text=True
                                            ,horizontal_scroll = True
                                            ,expand_x=True,expand_y=True
                                            ,key="-TX-EMP-")
                        ],
                        [
                                sg.Button(button_text='Write EMP', font=('メイリオ',fontsize_text-2), size=(12,1), key="-B-EMPFILE-"),
                        ]
                    ]
                ,expand_x=True,expand_y=True
                )
            ]
        ]
        ,expand_x=True,expand_y=True
    )
    frame2=sg.Frame("",
        [
            [
                sg.Frame("",
                    [
                        [
                            sg.Text("配置から除外するキャラ？"),
                            sg.Button(button_text='推し', font=('メイリオ',fontsize_text-2), size=(12,1), key="-B-SELECT-CHARA-")
                        ],
                        [   
                            sg.Text("",key="-T-CHECK-ERR-"),
                        ],
                        [
                            # テキストレイアウト
                            sg.Text("計算はじまる？\t\t"),
                            sg.Button(button_text='押忍', font=('メイリオ',fontsize_text-2), size=(12,1), key="-B-START-")   
                        ],
                        [
                            sg.Text("10分はかかるかも"),
                            sg.Text("計算状況・・・",key="STATUS"),
                        ],
                    ]
                ,expand_x=True, expand_y=True
                ,border_width=0
                ),
                sg.Frame("結果",
                    [
                        [
                            sg.Text("実行結果がここに表示されます\n\n",font=('メイリオ',fontsize_text),key="-T-RES-")
                        ]
                    ]
                ,expand_x=True, expand_y=True
                )
            ],            
        ]
        ,expand_x=True, expand_y=True
        ,border_width=0
        )

    #フレーム1(データ書き込み、他)
    frame1 = sg.Frame('',
        [
            [
                sg.Text("⇩クリックでジャンプします",font=('メイリオ',fontsize_text))
            ],
            [
                sg.Text("https://idleontoolbox.com/account/world-3/construction",enable_events=True, font=fontset, key="URL https://idleontoolbox.com/account/world-3/construction")
            ],
            [
                col_layout
            ],
            [
                frame2
            ],
            [
                sg.Text("Progress Bar:"),
                sg.ProgressBar(max_generations, orientation='h',size=(40,10),expand_x=True,key='-PROG-')
            ]
       ]
        #,size=(320,180) #幅,高さ
        ,expand_x=True, expand_y=True
    )
    layout =[
        [
            frame1
        ]
    ]
    window = sg.Window("Cogstruction"
                    , layout
                    , finalize=True
                    , resizable=True
                    , titlebar_icon=icon_data
                    , icon=icon_data
                    )
    
    window.set_icon(pngbase64=icon_data)
    Check=None
    cog_datas = None
    empties = None
    empties_set = None
    cogs = None
    cogs_goemetry = None
    while True:

        event, values = window.read()
        #print(event, values)

        if event == sg.WINDOW_CLOSED:
            break
        elif event.startswith("URL "):
            url = event.split(' ')[1]
            #print("アクセスするURL: ", url)
            webbrowser.open(url)
        elif event =="-B-COGFILE-":
            #print(values["-TX-COG-"])
            write_Text(values["-TX-COG-"],cog_datas_filename)
        elif event =="-B-EMPFILE-":
            #print(values["-TX-EMP-"])
            write_Text(values["-TX-EMP-"],empties_datas_filename)
        elif event=="-B-SELECT-CHARA-":
            cog_datas = read_cog_datas(cog_datas_filename)
            empties = read_empties_datas(empties_datas_filename)
            cog_datas,cog_dataframe=add_Coord(empties,cog_datas)
            #print([[cog_data["cog type"],*cog_data["args"]] for cog_data in cog_datas])
            #print(cog_datas)

            
            #print(temp[0])
            #print(cog_dataframe)
            #print(cog_dataframe.to_dict())
            #print(cog_factory(temp))
            #print(temp[0])
            #print(cog_dataframe[cog_dataframe["cog type"]=="Character"].values.tolist())
            charactesr_name=[data[-1] for data in cog_dataframe[cog_dataframe["cog type"]=="Character"]["args"].values.tolist()]
            chara_coords=[data for data in cog_dataframe[cog_dataframe["cog type"]=="Character"]["Pre-Coords"].values.tolist()]
            #print(chara_coords)
            #print(cog_dataframe)
            #print((Check is None))
            if (Check is None):
                #print("reset")
                Check=[True if t[1] is not None else False for t in chara_coords]
            res=active_sub_window(Check,charactesr_name)               
            #print(res)

            if(res is not None):
                Check=[t for t in res.values()] 
                Label=[data for data,t in res.items() if t]
                #print(Label)
                post_datas=[]
                for data in cog_datas:
                    #print(data)
                    if(data["cog type"]=="Character"):
                        #print(data)
                        add_data=[data for name in Label if(data["args"][3]==name)]
                        if(len(add_data)!=0):
                            post_datas.append(data) 
                    else:
                        post_datas.append(data)
                #print(post_data)
                cog_datas=post_datas
                if((len(cog_datas)+len(empties)-96)<0):
                    window["-T-CHECK-ERR-"].update("除外するキャラが多すぎます!あと%d人必要"%(96-len(cog_datas)-len(empties)))
                else:
                    window["-T-CHECK-ERR-"].update("OK")
            else:
                    window["-T-CHECK-ERR-"].update("中断ed")
            


        elif event =="-B-START-":
            window["STATUS"].update("計算中だよ")
            window.refresh()
            A = np.array([
                [1.,1.,1.],
                [inv_build_weight,-inv_flaggy_weight,0.],
                [0.,inv_flaggy_weight,-inv_exp_weight]
            ])
            b = np.array([1.,0.,0.])
            build_weight, flaggy_weight, exp_weight = np.linalg.solve(A, b)

            controller = (Iteration_Controller()
                .set_restart_info(num_restarts)
                .set_generation_info(min_generations,max_generations,max_running_total_len,req_running_total)
                .set_mutation_info(num_mutations)
                .set_breeding_scheme_info(prob_cross_breed,prob_one_point_mutation,prob_two_point_mutation)
            )
            if(cog_datas is None):
                cog_datas = read_cog_datas(cog_datas_filename)
            if(empties is None):
                empties = read_empties_datas(empties_datas_filename)
                cog_datas,cog_dataframe=add_Coord(empties,cog_datas)
            empties_set = Empties_Set(empties)
            cogs = cog_factory(cog_datas)
            #print(cogs)
            #print("emp.",empties)
            #print("set.",empties_set)
            #print("set.",empties_set.coords_list)

             
            best = learning_algo(
                cogs,
                empties_set,
                set(),
                pop_size,
                lambda cog: cog.standard_obj_fxn(build_weight,flaggy_weight,exp_weight),
                factor_base,
                max_factor,
                max_multiplier,
                controller,
                window
            )
            #print(best[0])

            #print("Writing best cog array to %s" % output_filename)
            with open(output_filename, "w") as fh:
                fh.write(str(best[0]))
            window["STATUS"].update("計算ed.best cog array to %s" %(output_filename))
                       
    
    window.close()
    print("end")