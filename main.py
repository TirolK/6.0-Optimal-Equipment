import PySimpleGUI as sg
import sys
import math

def calc(DH_min, DET_min, CRIT_min, SS_min, DH_limit, CRIT_limit, DET_limit, SS_limit, Status_max, fixed_ss, dot_rate, GCD_rate, DH_0):
  DH_max = 0
  DET_max = 0
  CRIT_max = 0
  SS_max = 0

  step = 12
  
  if (DH_0):
    DH_cut = Status_max
  else:
    DH_cut = 0
  
  damage_max = 0
  for DH in range(0, min([Status_max-DH_cut,DH_limit])+1,step):
    for DET in range(0, min([Status_max-DH,DET_limit])+1, step):
      for CRIT in range(0, min([Status_max-DH-DET,CRIT_limit])+1, step):
        if (fixed_ss): 
          SS = 0
        else:
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

def limit_calc(weapon,head,body,hand,leg,foot,ear,neck,arm,finger1,finger2):
  over_status = 0
  DH_limit = 0
  CRIT_limit = 0
  DET_limit = 0
  SS_limit = 0
  # weapon
  DH_limit   += min(max(weapon[0:3])-weapon[0], weapon[4]) + over_status
  CRIT_limit += min(max(weapon[0:3])-weapon[1], weapon[4]) + over_status
  DET_limit  += min(max(weapon[0:3])-weapon[2], weapon[4]) + over_status
  SS_limit   += min(max(weapon[0:3])-weapon[3], weapon[4]) + over_status
  # head
  DH_limit   += min(max(head[0:3])-head[0], head[4]) + over_status
  CRIT_limit += min(max(head[0:3])-head[1], head[4]) + over_status
  DET_limit  += min(max(head[0:3])-head[2], head[4]) + over_status
  SS_limit   += min(max(head[0:3])-head[3], head[4]) + over_status
  #body
  DH_limit   += min(max(body[0:3])-body[0], body[4]) + over_status
  CRIT_limit += min(max(body[0:3])-body[1], body[4]) + over_status
  DET_limit  += min(max(body[0:3])-body[2], body[4]) + over_status
  SS_limit   += min(max(body[0:3])-body[3], body[4]) + over_status
  #hand
  DH_limit   += min(max(hand[0:3])-hand[0], hand[4]) + over_status
  CRIT_limit += min(max(hand[0:3])-hand[1], hand[4]) + over_status
  DET_limit  += min(max(hand[0:3])-hand[2], hand[4]) + over_status
  SS_limit   += min(max(hand[0:3])-hand[3], hand[4]) + over_status
  #leg
  DH_limit   += min(max(leg[0:3])-leg[0], leg[4]) + over_status
  CRIT_limit += min(max(leg[0:3])-leg[1], leg[4]) + over_status
  DET_limit  += min(max(leg[0:3])-leg[2], leg[4]) + over_status
  SS_limit   += min(max(leg[0:3])-leg[3], leg[4]) + over_status
  #foot
  DH_limit   += min(max(foot[0:3])-foot[0], foot[4]) + over_status
  CRIT_limit += min(max(foot[0:3])-foot[1], foot[4]) + over_status
  DET_limit  += min(max(foot[0:3])-foot[2], foot[4]) + over_status
  SS_limit   += min(max(foot[0:3])-foot[3], foot[4]) + over_status
  #ear
  DH_limit   += min(max(ear[0:3])-ear[0], ear[4]) + over_status
  CRIT_limit += min(max(ear[0:3])-ear[1], ear[4]) + over_status
  DET_limit  += min(max(ear[0:3])-ear[2], ear[4]) + over_status
  SS_limit   += min(max(ear[0:3])-ear[3], ear[4]) + over_status
  #neck
  DH_limit   += min(max(neck[0:3])-neck[0], neck[4]) + over_status
  CRIT_limit += min(max(neck[0:3])-neck[1], neck[4]) + over_status
  DET_limit  += min(max(neck[0:3])-neck[2], neck[4]) + over_status
  SS_limit   += min(max(neck[0:3])-neck[3], neck[4]) + over_status
  #arm
  DH_limit   += min(max(arm[0:3])-arm[0], arm[4]) + over_status
  CRIT_limit += min(max(arm[0:3])-arm[1], arm[4]) + over_status
  DET_limit  += min(max(arm[0:3])-arm[2], arm[4]) + over_status
  SS_limit   += min(max(arm[0:3])-arm[3], arm[4]) + over_status
  #finger1
  DH_limit   += min(max(finger1[0:3])-finger1[0], finger1[4]) + over_status
  CRIT_limit += min(max(finger1[0:3])-finger1[1], finger1[4]) + over_status
  DET_limit  += min(max(finger1[0:3])-finger1[2], finger1[4]) + over_status
  SS_limit   += min(max(finger1[0:3])-finger1[3], finger1[4]) + over_status
  #finger2
  DH_limit   += min(max(finger2[0:3])-finger2[0], finger2[4]) + over_status
  CRIT_limit += min(max(finger2[0:3])-finger2[1], finger2[4]) + over_status
  DET_limit  += min(max(finger2[0:3])-finger2[2], finger2[4]) + over_status
  SS_limit   += min(max(finger2[0:3])-finger2[3], finger2[4]) + over_status

  return DH_limit, CRIT_limit, DET_limit, SS_limit

def main(argv):
  sg.theme('DarkBlue14')
  
  layout = [[sg.Text('装備のステータス')],
            [sg.Text('',size=(5,1)), sg.Text("DH",size=(4,1)), sg.Text("CRIT",size=(5,1)), sg.Text("DET",size=(4,1)), sg.Text("SS",size=(4,1)), sg.Text("Materia",size=(8,1)),
             sg.Text('',size=(9,1)), sg.Text("DH",size=(4,1)), sg.Text("CRIT",size=(5,1)), sg.Text("DET",size=(4,1)), sg.Text("SS",size=(4,1)), sg.Text("Materia",size=(8,1))
            ],

            [sg.Text(' 武器:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #0
             sg.InputText(size=(5,1),default_text="0"), #1
             sg.InputText(size=(5,1),default_text="0"), #2
             sg.InputText(size=(5,1),default_text="0"), #3
             sg.InputText(size=(5,1),default_text="72"),#4
             sg.Text("",size=(5,1)),
             sg.Text('耳:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #5
             sg.InputText(size=(5,1),default_text="0"), #6
             sg.InputText(size=(5,1),default_text="0"), #7
             sg.InputText(size=(5,1),default_text="0"), #8
             sg.InputText(size=(5,1),default_text="36"),#9
            ],
            
            [sg.Text(' 頭:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #10
             sg.InputText(size=(5,1),default_text="0"), #11
             sg.InputText(size=(5,1),default_text="0"), #12
             sg.InputText(size=(5,1),default_text="0"), #13
             sg.InputText(size=(5,1),default_text="72"),#14
             sg.Text("",size=(5,1)),
             sg.Text('首:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #15
             sg.InputText(size=(5,1),default_text="0"), #16
             sg.InputText(size=(5,1),default_text="0"), #17
             sg.InputText(size=(5,1),default_text="0"), #18
             sg.InputText(size=(5,1),default_text="36"),#19
            ],

            [sg.Text(' 胴:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #20
             sg.InputText(size=(5,1),default_text="0"), #21
             sg.InputText(size=(5,1),default_text="0"), #22
             sg.InputText(size=(5,1),default_text="0"), #23
             sg.InputText(size=(5,1),default_text="72"),#24
             sg.Text("",size=(5,1)),
             sg.Text('腕:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #25
             sg.InputText(size=(5,1),default_text="0"), #26
             sg.InputText(size=(5,1),default_text="0"), #27
             sg.InputText(size=(5,1),default_text="0"), #28
             sg.InputText(size=(5,1),default_text="36"),#29
            ],

            [sg.Text(' 手:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #30
             sg.InputText(size=(5,1),default_text="0"), #31
             sg.InputText(size=(5,1),default_text="0"), #32
             sg.InputText(size=(5,1),default_text="0"), #33
             sg.InputText(size=(5,1),default_text="72"),#34
             sg.Text("",size=(5,1)),
             sg.Text('指:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #35
             sg.InputText(size=(5,1),default_text="0"), #36
             sg.InputText(size=(5,1),default_text="0"), #37
             sg.InputText(size=(5,1),default_text="0"), #38
             sg.InputText(size=(5,1),default_text="36"),#39
            ],

            [sg.Text(' 脚:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #40
             sg.InputText(size=(5,1),default_text="0"), #41
             sg.InputText(size=(5,1),default_text="0"), #42
             sg.InputText(size=(5,1),default_text="0"), #43
             sg.InputText(size=(5,1),default_text="72"),#44
             sg.Text("",size=(5,1)),
             sg.Text('指:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #45
             sg.InputText(size=(5,1),default_text="0"), #46
             sg.InputText(size=(5,1),default_text="0"), #47
             sg.InputText(size=(5,1),default_text="0"), #48
             sg.InputText(size=(5,1),default_text="36"),#49
            ],

            [sg.Text(' 足:',size=(5,1)), 
             sg.InputText(size=(5,1),default_text="0"), #50
             sg.InputText(size=(5,1),default_text="0"), #51
             sg.InputText(size=(5,1),default_text="0"), #52
             sg.InputText(size=(5,1),default_text="0"), #53
             sg.InputText(size=(5,1),default_text="72"),#54
            ],

            [sg.Text('')],

            [sg.Text('食事で追加されるサブステータス')],
            [sg.Text(' DH:  ',size=(5,1)), sg.InputText(size=(10,1),default_text="0")], #55
            [sg.Text(' DET: ',size=(5,1)), sg.InputText(size=(10,1),default_text="0")], #56
            [sg.Text(' CRIT:',size=(5,1)), sg.InputText(size=(10,1),default_text="0")], #57
            [sg.Text(' SS:  ',size=(5,1)), sg.InputText(size=(10,1),default_text="0")], #58

            [sg.Text('')],

            [sg.Text('マテリアで追加できるサブステータスの量:'), sg.InputText(size=(10,1),default_text="00")], #59
            # [sg.Text('マテリアの各ステータス上限値:'), sg.InputText(size=(10,1),default_text="230")],
            [sg.Text('')],
            [sg.Checkbox("SSの値を固定する", default=True)], #60
            [sg.Text('')],
            [sg.Text('全火力に対するDoTの割合: '), sg.InputText(size=(10,1),default_text="0.1619")], #61
            [sg.Text('全火力に対するウェポンスキルの割合(上記のDoT攻撃は含まない): '), sg.InputText(size=(10,1),default_text="0.758693912")], #62
            [sg.Text('')],
            [sg.Checkbox('DHを排除する', default=False)], #63
            [sg.Text('')],
            [sg.Button('Calc',size=(60,3))],
            [sg.Text('加算分最適値（括弧内はマテリアのみ）:'), sg.Text(key='-result-')],
            [sg.Text(' DH:  '), sg.Text(key='-result_dh-')],
            [sg.Text(' DET: '), sg.Text(key='-result_det-')],
            [sg.Text(' CRIT:'), sg.Text(key='-result_crit-')],
            [sg.Text(' SS:  '), sg.Text(key='-result_ss-')],
            [sg.Text(' ダメージ倍率(期待値)'), sg.Text(key='-result_damage-')]
  ]
  
  window = sg.Window('6.0 Optimal Equipment', layout)
  
  while (True):
    event, values = window.read()
    if (event == sg.WIN_CLOSED):
      break
    elif (event == 'Calc'):
      weapon =  [int(values[0]),int(values[1]),int(values[2]),int(values[3]),int(values[4])]
      head =    [int(values[5]),int(values[6]),int(values[7]),int(values[8]),int(values[9])]
      body =    [int(values[10]),int(values[11]),int(values[12]),int(values[13]),int(values[14])]
      hand =    [int(values[15]),int(values[16]),int(values[17]),int(values[18]),int(values[19])]
      leg =     [int(values[20]),int(values[21]),int(values[22]),int(values[23]),int(values[24])]
      foot =    [int(values[25]),int(values[26]),int(values[27]),int(values[28]),int(values[29])]
      ear =     [int(values[30]),int(values[31]),int(values[32]),int(values[33]),int(values[34])]
      neck =    [int(values[35]),int(values[36]),int(values[37]),int(values[38]),int(values[39])]
      arm =     [int(values[40]),int(values[41]),int(values[42]),int(values[43]),int(values[44])]
      finger1 = [int(values[45]),int(values[46]),int(values[47]),int(values[48]),int(values[49])]
      finger2 = [int(values[50]),int(values[51]),int(values[52]),int(values[53]),int(values[54])]
      
      meal = [int(values[55]),int(values[56]),int(values[57]),int(values[58])]

      DH_min =   weapon[0]+head[0]+body[0]+hand[0]+leg[0]+foot[0]+ear[0]+neck[0]+arm[0]+finger1[0]+finger2[0]+meal[0]
      CRIT_min = weapon[1]+head[1]+body[1]+hand[1]+leg[1]+foot[1]+ear[1]+neck[1]+arm[1]+finger1[1]+finger2[1]+meal[1]
      DET_min =  weapon[2]+head[2]+body[2]+hand[2]+leg[2]+foot[2]+ear[2]+neck[2]+arm[2]+finger1[2]+finger2[2]+meal[2]
      SS_min =   weapon[3]+head[3]+body[3]+hand[3]+leg[3]+foot[3]+ear[3]+neck[3]+arm[3]+finger1[3]+finger2[3]+meal[3]

      DH_limit, CRIT_limit, DET_limit, SS_limit = limit_calc(weapon,head,body,hand,leg,foot,ear,neck,arm,finger1,finger2)

      Status_max = int(values[59])
      fixed_ss = values[60]
      dot_rate = float(values[61])
      GCD_rate = float(values[62])
      DH_0 = values[63]

      result = calc(DH_min, DET_min, CRIT_min, SS_min, DH_limit, CRIT_limit, DET_limit, SS_limit, Status_max, fixed_ss, dot_rate, GCD_rate, DH_0)
      window['-result_dh-'].update(str(result[0])+str(" ("+str(result[0]-DH_min)+")"))
      window['-result_det-'].update(str(result[1])+str(" ("+str(result[1]-DET_min)+")"))
      window['-result_crit-'].update(str(result[2])+str(" ("+str(result[2]-CRIT_min)+")"))
      window['-result_ss-'].update(str(result[3])+str(" ("+str(result[3]-SS_min)+")"))
      window['-result_damage-'].update(math.floor(result[4]*10000.0)/10000.0)
  window.close()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
  