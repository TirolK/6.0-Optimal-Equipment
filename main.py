import PySimpleGUI as sg
import sys


# equipment
DH_min = 0
DET_min = 1077
CRIT_min = 0
SS_min = 0
result = [0,0,0,0]
Status_max = 408

def calc(DH_min, DET_min, CRIT_min, SS_min, Status_max, fixed_ss, dot_rate, GCD_rate, DH_0):
  step = 12
  
  if (DH_0):
    DH_cut = Status_max
  else:
    DH_cut = 0
  
  damage_max = 0
  for DH in range(0, Status_max+1-DH_cut,step):
    for DET in range(0, Status_max-DH+1, step):

      if (fixed_ss): 
        start_CRIT = Status_max-DH-DET
      else:
        start_CRIT = 0

      for CRIT in range(start_CRIT, Status_max-DH-DET+1, step):
        SS = Status_max - DH - DET - CRIT
  
        DH_calc = DH + DH_min
        CRIT_calc = CRIT + CRIT_min
        DET_calc = DET + DET_min
        SS_calc = SS + SS_min
  
        DH_rate = 1+(DH_calc*0.289473684*0.001)*0.25
        CRIT_rate = 1+((5+CRIT_calc*0.105263158*0.1)*0.01)*((1.4+CRIT_calc*0.105263158*0.001)-1)
        DET_rate = 1+DET_calc*0.073684211*0.001
        SS_DoT_rate = 1+SS_calc/14.705*0.001
  
        # print(SS_calc,SS_DoT_rate,(2.5/(2.5-SS_calc/57*0.01)))
        # damage = DH_rate*CRIT_rate*DET_rate
        damage = (dot_rate*SS_DoT_rate + GCD_rate*(2.5/(2.5-SS_calc/57.0*0.01)) + (1.0-dot_rate-GCD_rate))*DH_rate*CRIT_rate*DET_rate
        # print(DH_rate,CRIT_rate,DET_rate)
  
        if(damage_max < damage): 
          damage_max = damage
          DH_max = DH_calc
          DET_max = DET_calc
          CRIT_max = CRIT_calc
          SS_max = SS_calc
        
    # print(DH,DET,CRIT,SS,damage)
    
  return [DH_max,DET_max,CRIT_max,SS_max,damage_max]

def main(argv):
    sg.theme('DarkBlue14')
    
    layout = [  [sg.Text('装備した状態でのサブステータスの表示値（マテリア、食事等は装着しない状態）')],
                [sg.Text(' DH:  '), sg.InputText(size=(10,1),default_text="400")],
                [sg.Text(' DET: '), sg.InputText(size=(10,1),default_text="340")],
                [sg.Text(' CRIT:'), sg.InputText(size=(10,1),default_text="400")],
                [sg.Text(' SS:  '), sg.InputText(size=(10,1),default_text="400")],
                [sg.Text('食事で追加されるサブステータス')],
                [sg.Text(' DH:  '), sg.InputText(size=(10,1),default_text="0")],
                [sg.Text(' DET: '), sg.InputText(size=(10,1),default_text="0")],
                [sg.Text(' CRIT:'), sg.InputText(size=(10,1),default_text="0")],
                [sg.Text(' SS:  '), sg.InputText(size=(10,1),default_text="0")],
                [sg.Text('マテリアで追加できるサブステータスの量:'), sg.InputText(size=(10,1),default_text="0")],
                [sg.Text('')],
                [sg.Checkbox("SSの値を固定する", default=True)],
                [sg.Text('')],
                [sg.Text('全火力に対するDoTの割合: '), sg.InputText(size=(10,1),default_text="0.1619")],
                [sg.Text('全火力に対するウェポンスキルの割合(上記のDoT攻撃は含まない): '), sg.InputText(size=(10,1),default_text="0.758693912")],
                [sg.Text('')],
                [sg.Checkbox('DHを排除する', default=False)],
                [sg.Text('')],
                [sg.Button('Calc',size=(60,3))],
                [sg.Text('最適解（括弧内はマテリアのみ）:'), sg.Text(key='-result-')],
                [sg.Text(' DH:  '), sg.Text(key='-result_dh-')],
                [sg.Text(' DET: '), sg.Text(key='-result_det-')],
                [sg.Text(' CRIT:'), sg.Text(key='-result_crit-')],
                [sg.Text(' SS:  '), sg.Text(key='-result_ss-')],
                [sg.Text(' ダメージ倍率(期待値)'), sg.Text(key='-result_damage-')]
    ]
    
    window = sg.Window('6.0 Optimal Equipment', layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Calc':
            DH_min = int(values[0]) + int(values[4]) - 400
            DET_min = int(values[1]) + int(values[5]) - 340
            CRIT_min = int(values[2]) + int(values[6]) - 400
            SS_min = int(values[3]) + int(values[7]) - 400
            Status_max = int(values[8])
            fixed_ss = values[9]
            dot_rate = float(values[10])
            GCD_rate = float(values[11])
            DH_0 = values[12]
            result = calc(DH_min, DET_min, CRIT_min, SS_min, Status_max, fixed_ss, dot_rate, GCD_rate, DH_0)
            window['-result_dh-'].update(str(result[0]+400)+str(" ("+str(result[0]-DH_min)+")"))
            window['-result_det-'].update(str(result[1]+340)+str(" ("+str(result[1]-DET_min)+")"))
            window['-result_crit-'].update(str(result[2]+400)+str(" ("+str(result[2]-CRIT_min)+")"))
            window['-result_ss-'].update(str(result[3]+400)+str(" ("+str(result[3]-SS_min)+")"))
            window['-result_damage-'].update(result[4])
    window.close()



if __name__ == '__main__':
    sys.exit(main(sys.argv))
  