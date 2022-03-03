import math
import numpy as np
profile=""
import pandas as pd
tablea=pd.read_csv('./Rula_score/TableA.csv')
tableb=pd.read_csv('./Rula_score/TableB.csv')
tablec=pd.read_csv('./Rula_score/TableC.csv')
tablea1=pd.read_csv('./Reba_score/TableA.csv')
tableb1=pd.read_csv('./Reba_score/TableB.csv')
tablec1=pd.read_csv('./Reba_score/TableC.csv')

def rula_risk(point_score, wrist, trunk, upper_Shoulder, lower_Limb, neck, wrist_twist, legs, muscle_use, force_load_a, force_load_b, upper_body_muscle):

    rula={}
    rula['score']='NULL'
    rula['risk']='NULL'
    if wrist!=0 and  trunk!=0 and upper_Shoulder!=0 and lower_Limb!=0 and neck!=0 and wrist_twist!=0:
        #Table A:
        col_name=str(wrist)+'WT'+str(wrist_twist)
        # print("upper_Shoulder",upper_Shoulder)
        # print("LOWER:",lower_Limb)
        tablea_val=tablea[(tablea['UpperArm']==upper_Shoulder) & (tablea['LowerArm']==lower_Limb)]
        tablea_val=tablea_val[col_name].values[0]
    
        point_score['posture_score_a']=str(tablea_val)
        tablea_val=tablea_val+muscle_use+force_load_a
        point_score['wrist_and_arm_score']=str(tablea_val)

        #Table B:
        col_name=str(trunk)+str(legs)
        tableb_val=tableb[(tableb['Neck']==neck)]
        tableb_val=tableb_val[col_name].values[0]
        point_score['posture_score_b']=str(tableb_val)
        tableb_val=tableb_val+force_load_b+upper_body_muscle
        point_score['neck_trunk_leg_score']=str(tableb_val)

        #Table C
        if tablea_val>=8:
            tablea_val=8
        if tableb_val>=7:
            tableb_val=7
        col_name=str(tableb_val)
        tablec_val=tablec[(tablec['Score']==tablea_val)]
        tablec_val=tablec_val[col_name].values[0]

        if tablec_val==1 or tablec_val==2:
            rula['score']=str(tablec_val)
            rula['risk']='Negligible'
        elif tablec_val==3 or tablec_val==4:
            rula['score']=str(tablec_val)
            rula['risk']='Low risk'
        elif tablec_val==5 or tablec_val==6:
            rula['score']=str(tablec_val)
            rula['risk']='Medium risk'
        elif tablec_val>6:
            rula['score']=str(tablec_val)
            rula['risk']='Very high risk'
    # print(rula)
    return rula, point_score

def reba_risk(point_score, wrist, trunk, upper_Shoulder, lower_Limb, neck, legs, force_load_a, coupling_score, activity_score):

    reba={}
    reba['score']='NULL'
    reba['risk']='NULL'

    if wrist!=0 and trunk!=0 and upper_Shoulder!=0 and lower_Limb!=0 and neck!=0 and legs!=0:
        #Tabel A:
        col_name=str(neck)+str(legs)
        tablea_val=tablea1[(tablea1['Trunk']==trunk)]
        tablea_val=tablea_val[col_name].values[0]
        point_score['posture_score_a']=str(tablea_val)
        tablea_val=tablea_val+force_load_a
        point_score['wrist_and_arm_score']=str(tablea_val)

        #Table B:
        col_name=str(lower_Limb)+str(wrist)
        tableb_val=tableb1[(tableb1['upper_Shoulder']==upper_Shoulder)]
        tableb_val=tableb_val[col_name].values[0]
        point_score['posture_score_b']=str(tableb_val)
        tableb_val=tableb_val+coupling_score
        point_score['score_BE']=str(tableb_val)

        #Table C:
        col_name=str(tableb_val)
        tablec_val=tablec1[(tablec1['Score']==tablea_val)]
        tablec_val=tablec_val[col_name].values[0]
        point_score['table_C']=str(tablec_val)
        tablec_val=tablec_val+activity_score

        if tablec_val==1:
            reba['score']=str(tablec_val)
            reba['risk']='Negligible'
        elif tablec_val==3 or tablec_val==2:
            reba['score']=str(tablec_val)
            reba['risk']='Low risk'
        elif tablec_val>=4 and tablec_val<=7:
            reba['score']=str(tablec_val)
            reba['risk']='Medium risk'
        elif tablec_val>=8 and tablec_val<=10:
            reba['score']=str(tablec_val)
            reba['risk']='High risk'
        elif tablec_val>=11:
            reba['score']=str(tablec_val)
            reba['risk']='Very high risk'
    # print(reba,point_score)
    return reba, point_score

def reba_score(angle_dict, pose, profile):
    R_Ear = pose[8]
    L_Ear = pose[7]
    R_Shoulder = pose[12]
    R_Elbow = pose[14]
    L_Shoulder = pose[11]
    L_Elbow = pose[13]
    point_score={}

    if profile:
    
        if profile=='Left' or profile=='Front':
            sholder = np.array(L_Elbow[0] - L_Shoulder[0])
            elbow = np.array(L_Elbow[1] - L_Shoulder[1])
            angle1=np.arctan2(elbow, sholder) * 180 / np.pi
            val=angle1
            angle1=abs(90-angle1)

            if angle1 >90:
                angle1=val+270

            if str(angle1) !='nan':
                if angle1 > 0 and angle1 <=20:
                    upper_Shoulder=1
                elif angle1 >20 and angle1 <=45:
                    upper_Shoulder=2
                elif angle1 >45 and angle1 <=90:
                    upper_Shoulder=3
                elif angle1 >90:
                    upper_Shoulder=4
            else:
                upper_Shoulder=1
        
        elif profile=='Right':
            sholder = np.array(R_Elbow[0] - R_Shoulder[0])
            elbow = np.array(R_Elbow[1] - R_Shoulder[1])
            angle1=np.arctan2(elbow, sholder) * 180 / np.pi
            val=angle1
            angle1=abs(90-angle1)

            if angle1 >90:
                angle1=val+270

            if str(angle1) !='nan':
                if angle1 > 0 and angle1 <=20:
                    upper_Shoulder=1
                elif angle1 >20 and angle1 <=45:
                    upper_Shoulder=2
                elif angle1 >45 and angle1 <=90:
                    upper_Shoulder=3
                elif angle1 >90:
                    upper_Shoulder=4
            else:
                upper_Shoulder=1

        point_score['upper_arm']=upper_Shoulder
        u_s_adjustmet=0
        point_score['upper_arm_adjustment']=u_s_adjustmet
        upper_Shoulder=upper_Shoulder+u_s_adjustmet
        
        if profile=='Left' or profile=='Front':
            angle2=angle_dict['left_elbow']
        elif profile=='Right':
            angle2=angle_dict['right_elbow']

        if str(angle2) !='NULL':
            angle2=abs(180-int(angle2))
            if angle2 >=0 and angle2 <30:
                lower_Limb=2
            elif angle2 >=30 and angle2 <60: 
                lower_Limb=1
            elif angle2>=60:
                lower_Limb=2
        else:
            lower_Limb=1

        point_score['lower_arm']=lower_Limb
        l_l_adjustement=0
        point_score['lower_arm_adjustment']=l_l_adjustement
        lower_Limb=l_l_adjustement+lower_Limb

        if profile=='Left' or profile=='Front':
            angle3=angle_dict['left_wrist']
        elif profile=='Right':
            angle3=angle_dict['right_wrist']
        
        if str(angle3) !='NULL':
            angle3=abs(int(angle3))
            if angle3<=100:
                wrist=1
            elif angle3 >100:
                wrist=2
        else:
            wrist=1

        point_score['wrist']=wrist
        w_adjustment=0
        point_score['wrist_adjustment']=w_adjustment
        wrist=wrist+w_adjustment
        
        angle4=angle_dict['neck']
        
        if str(angle4)!='NULL':
            angle4=abs(int(angle4))
            angle4=int(angle4)
            if angle4 >0 and angle4 <30:
                neck=1
            elif angle4 >=30 and angle4<45:
                neck=2
            elif angle4 >=45:
                neck=2
            else:
                neck=0
        else:
            neck=1

        point_score['neck']=neck
        n_adjustment=0
        point_score['neck_adjustment']=n_adjustment
        neck=neck+n_adjustment

        angle5=angle_dict['trunk']
        if str(angle5) !='NULL':
            angle5=int(angle5)
            if angle5 <= 0:
                trunk=1
            elif angle5 >0 and angle5 <=100:
                trunk=2
            elif angle5 >100 and angle5 <=150:
                trunk=3
            elif angle5 >150 and angle5<=200:
                trunk=4
            elif angle5 > 200:
                trunk=2
        else:
            trunk=1

        point_score['trunk']=trunk
        t_adjustment=0
        point_score['trunk_adjustment']=t_adjustment
        trunk=trunk+t_adjustment    

        angle6_r=angle_dict['right_knee']
        angle6_l=angle_dict['left_knee']

        point_score['legs_adjustment']=0

        if str(angle6_l) !='NULL' and str(angle6_r) !='NULL':
            angle6_l=int(angle6_l)
            angle6_r=int(angle6_r)
            ang=abs(angle6_r-angle6_l)
            if ang<=20:
                legs=1
            else:
                legs=2
            point_score['legs']=legs

            if profile=='Right':
                if angle6_r>=80 and angle6_r<=100:
                    legs=legs+1
                    point_score['legs_adjustment']=1
                elif angle6_r<80 and angle6_r>100:
                    legs=legs+2
                    point_score['legs_adjustment']=2
            elif profile=='Left' or profile=='Front':
                if angle6_l>=80 and angle6_l<=100:
                    legs=legs+1
                    point_score['legs_adjustment']=1
                elif angle6_l<80 or angle6_l>100:
                    legs=legs+2
                    point_score['legs_adjustment']=2
        else:
            legs=1
            point_score['legs']=legs
            point_score['legs_adjustment']=0
        # if profile=='Left' or profile=='Front':
            # print(angle1,angle2,angle3,angle4,angle5,angle6_l)
        # else:
            # print(angle1,angle2,angle3,angle4,angle5,angle6_r)
        force_load_a=0
        point_score['force_load_a']=force_load_a
        coupling_score=0
        point_score['coupling_score']=coupling_score
        activity_score=0
        point_score['activity_score']=activity_score
        try:
            reba, point_score=reba_risk(point_score, wrist, trunk, upper_Shoulder, lower_Limb, neck, legs, force_load_a, coupling_score, activity_score)
            reba['point_score']=point_score
            
        except Exception as e:
            reba={}
            reba['score']='NULL'
            reba['risk']='NULL'
            reba['point_score']={}

    else:
        reba={}
        reba['score']='NULL'
        reba['risk']='NULL'
        reba['point_score']={}

    return reba

def rula_score(angle_dict, pose,profile):
    
    Nose = pose[0]
    L_Neck = pose[11]
    R_Neck = pose[12]
    R_Shoulder = pose[12]
    R_Elbow = pose[14]
    R_Wrist = pose[16]
    L_Shoulder = pose[11]
    L_Elbow = pose[13]
    L_Wrist = pose[15]
    R_Hip = pose[24]
    L_Hip = pose[23]
    R_Knee = pose[26]
    R_Ankle = pose[28]
    L_Knee = pose[25]
    L_Ankle = pose[27]
    R_Eye=pose[5]
    L_Eye=pose[2]
    R_Ear = pose[8]
    L_Ear = pose[7]
    L_Foot = pose[31]
    R_Foot = pose[32]
    R_Palm = pose[20]
    L_Palm = pose[19]
    point_score={}
    if profile:

        if profile=='Right' or profile=='Left' or profile=='Front':
            sholder = np.array((L_Elbow[0]+R_Elbow[0])/2 - (L_Shoulder[0]+R_Shoulder[0])/2)
            elbow = np.array((L_Elbow[1]+R_Elbow[1])/2 - (L_Shoulder[1]+R_Shoulder[0])/2)
            angle1 = np.arctan2(elbow, sholder) * 180 / np.pi
            val=angle1
            angle1=abs(90-angle1)
            
            if angle1 >90:
                angle1=val+270
            if str(angle1) !='nan':
                if angle1 > 0 and angle1 <=30:
                    upper_Shoulder=1
                elif angle1 >30 and angle1 <=50:
                    upper_Shoulder=2
                elif angle1 >50 and angle1 <=90:
                    upper_Shoulder=3
                elif angle1 >90:
                    upper_Shoulder=4
            else:
                upper_Shoulder=1
        point_score['upper_arm']=upper_Shoulder
        u_s_adjustmet=0
        point_score['upper_arm_adjustment']=u_s_adjustmet
        upper_Shoulder=upper_Shoulder+u_s_adjustmet
        
        if profile=='Left' or profile=='Front':
            angle2=angle_dict['left_elbow']
        elif profile=='Right':
            angle2=angle_dict['right_elbow']
        if str(angle2) !='NULL':
            angle2=int(angle2)
            l_l_adjustement=0
            point_score['lower_arm_adjustment']=l_l_adjustement
            if angle2 > 80 and angle2 <=100:
                lower_Limb=1
                point_score['lower_arm']=lower_Limb

            elif angle2 >130: 
                lower_Limb=2
                point_score['lower_arm']=lower_Limb
               
            elif angle2>100 and angle2<=130:
                lower_Limb=3
                point_score['lower_arm']=lower_Limb
        
        else:
            lower_Limb=1
            point_score['lower_arm']=lower_Limb
            l_l_adjustement=0
            point_score['lower_arm_adjustment']=l_l_adjustement

        if profile=='Left' or profile=='Front':
            angle3=angle_dict['left_wrist']
        elif profile=='Right':
            angle3=angle_dict['right_wrist']


        if str(angle3) !='NULL':
            angle3=abs(int(angle3))
            if angle3 > 0 and angle3<=80:
                wrist=1
            elif angle3 >=80 and angle3 <=140:
                wrist=2
            elif angle3 >140:
                wrist=3
        else:
            wrist=1

        point_score['wrist']=wrist
        w_adjustment=0
        point_score['wrist_adjustment']=w_adjustment
        wrist=wrist+w_adjustment

        angle4=angle_dict['neck']
        if str(angle4)!='NULL':
            angle4=abs(int(angle4))
            
            if angle4 > 0 and angle4 <=30:
                neck=1
            elif angle4 >30 and angle4 <=45:
                neck=2
            elif angle4 >45:
                neck=3
            elif angle4 >=55:
                neck=4
            else:
                neck=1
        else:
            neck=1

        point_score['neck']=neck
        n_adjustment=0
        point_score['neck_adjustment']=n_adjustment
        neck=neck+n_adjustment

        angle5=angle_dict['trunk']
        if str(angle5) !='NULL':
            angle5=abs(int(angle5))
            if angle5 < 90:
                trunk=1
            elif angle5 >90 and angle5 <=150:
                trunk=2
            elif angle5 >150 and angle5<=200:
                trunk=3
            elif angle5 <200:
                trunk=4
            else:
                trunk=1
        else:
            trunk=1

        point_score['trunk']=trunk
        t_adjustment=0
        point_score['trunk_adjustment']=t_adjustment
        trunk=trunk+t_adjustment

        wrist_twist=2
        point_score['wrist_twist']=wrist_twist
        
        legs=2
        point_score['legs']=legs
        # print(angle1,angle2,angle3,angle4,angle5)
        muscle_use=0
        force_load_a=0
        force_load_b=0
        upper_body_muscle=0
        point_score['muscle_use_a']=muscle_use
        point_score['force_load_a']=force_load_a
        point_score['force_load_b']=force_load_b
        point_score['muscle_use_b']=upper_body_muscle
        try:
            rula, point_score=rula_risk(point_score, wrist, trunk, upper_Shoulder, lower_Limb, neck, wrist_twist, legs, muscle_use, force_load_a, force_load_b, upper_body_muscle)
            rula['point_score']=point_score
        
        except Exception as e:
            rula={}
            rula['score']='NULL'
            rula['risk']='NULL'
            rula['point_score']={}

    else:
        rula={}
        rula['score']='NULL'
        rula['risk']='NULL'
        rula['point_score']={}

    return rula

def angle_calc(pose):
    Nose = pose[0]
    L_Neck = pose[11]
    R_Neck = pose[12]
    R_Shoulder = pose[12]
    R_Elbow = pose[14]
    R_Wrist = pose[16]
    L_Shoulder = pose[11]
    L_Elbow = pose[13]
    L_Wrist = pose[15]
    R_Hip = pose[24]
    L_Hip = pose[23]
    R_Knee = pose[26]
    R_Ankle = pose[28]
    L_Knee = pose[25]
    L_Ankle = pose[27]
    R_Eye=pose[5]
    L_Eye=pose[2]
    R_Ear = pose[8]
    L_Ear = pose[7]
    L_Foot = pose[31]
    R_Foot = pose[32]
    R_Palm = pose[20]
    L_Palm = pose[19]
    # print("R_Eye:",R_Eye,"L_Eye:",L_Eye)
    # print("R_Ear:",R_Ear,"L_Ear:",L_Ear)
    # print("R_Neck:",R_Neck,"L_Neck:",L_Neck)
    # print("R_Elbow:",R_Elbow,"L_Elbow:",L_Elbow)
    # print("R_Wrist:",R_Wrist,"L_Wrist:",L_Wrist)
    # print("R_Hip:",R_Hip,"L_Hip:",L_Hip)
    # print("R_Knee:",R_Knee,"L_Knee:",L_Knee)
    # print("R_Ankle:",R_Ankle,"L_Ankle:",L_Ankle)
    # print("R_Foot:",R_Foot,"L_Foot:",L_Foot)
    # print("R_Palm:",R_Palm,"L_Palm:",L_Palm)
    left=0
    right=0
    front=0
    if abs(round(R_Elbow[3],2)-round(L_Elbow[3],2))<=0.2:
        front+=1
    elif round(R_Elbow[3],2)>round(L_Elbow[3],2)+0.2:
        right+=1
    else:
        left+=1
    if abs(round(R_Wrist[3],2)-round(L_Wrist[3],2))<=0.2:
        front+=1
    elif round(R_Wrist[3],2)>round(L_Wrist[3],2):
        right+=1
    else:
        left+=1
    if abs(round(R_Knee[3],2)-round(L_Knee[3],2))<=0.2:
        front+=1
    elif round(R_Knee[3],2)>round(L_Knee[3],2):
        right+=1
    else:
        left+=1
    if abs(round(R_Ankle[3],2)-round(L_Ankle[3],2))<=0.2:
        front+=1
    elif round(R_Ankle[3],2)>round(L_Ankle[3],2):
        right+=1
    else:
        left+=1
    if abs(round(R_Foot[3],2)-round(L_Foot[3],2))<=0.2:
        front+=1
    elif round(R_Foot[3],2)>round(L_Foot[3],2):
        right+=1
    else:
        left+=1
    if abs(round(R_Palm[3],2)-round(L_Palm[3],2))<0.2:
        front+=1
    elif round(R_Palm[3],2)>round(L_Palm[3],2):
        right+=1
    else:
        left+=1
    # print(left,right,front)
    if left < right:
        if right > front:
            profile="Right"
        else:
            profile="Front"
    elif right < left:
        if left > front:
            profile="Left"
        else:
            profile="Front"
    else:
        profile="Front"
    # print(profile)
    not_indentified=[]
    score={}
    side_profile=''
    angle_dict={}
    
    if profile: 
        #Right_Elbow
        try:
            sc=min(R_Wrist[2],R_Elbow[2],R_Shoulder[2])
            score['right_elbow']=round(sc*100)
            angle1 = abs(math.degrees(math.atan2(R_Wrist[1]-R_Elbow[1], R_Wrist[0]-R_Elbow[0]) - math.atan2(R_Shoulder[1]-R_Elbow[1], R_Shoulder[0]-R_Elbow[0])))
            angle_dict['right_elbow']=int(angle1)
        except Exception as e:
            angle_dict['right_elbow']='NULL'        
        #Left_elbow
        try:
            sc=min(L_Wrist[2],L_Elbow[2],L_Shoulder[2])
            score['left_elbow']=round(sc*100)
            angle2 = abs(math.degrees(math.atan2(L_Wrist[1]-L_Elbow[1], L_Wrist[0]-L_Elbow[0]) - math.atan2(L_Shoulder[1]-L_Elbow[1], L_Shoulder[0]-L_Elbow[0])))
            angle_dict['left_elbow']=int(angle2)
        except Exception as e:
            angle_dict['left_elbow']='NULL'

        #Right_knee
        try:
            sc=min(R_Ankle[2],R_Hip[2],R_Knee[2])
            score['right_knee']=round(sc*100)
            angle3=abs(np.arctan2((R_Foot[1]-R_Knee[1]), (R_Foot[0]-R_Knee[0])) * 180 / np.pi)
            # angle3 = math.degrees(math.atan2(R_Foot[1]-R_Knee[1], R_Foot[0]-R_Knee[0]) - math.atan2(R_Hip[1]-R_Knee[1], R_Hip[0]-R_Knee[0]))
            angle_dict['right_knee']=int(angle3)
        except Exception as e:
            angle_dict['right_knee']='NULL'

        #left_knee
        try:
            sc=min(L_Ankle[2], L_Hip[2], L_Knee[2])
            score['left_knee']=round(sc*100)
            angle4=abs(np.arctan2((L_Foot[1]-L_Knee[1]), (L_Foot[0]-L_Knee[0])) * 180 / np.pi)
            # angle4 = math.degrees(math.atan2(L_Ankle[1]-L_Knee[1], L_Ankle[0]-L_Knee[0]) - math.atan2(L_Hip[1]-L_Knee[1], L_Hip[0]-L_Knee[0]))
            angle4=int(angle4)
            angle_dict['left_knee']=angle4
        except Exception as e:
            angle_dict['left_knee']='NULL'

        #right_ankle
        try:
            sc=min(R_Ankle[2], R_Foot[2])
            score['right_ankle']=round(sc*100)        
            angle5=np.arctan2((R_Foot[1]-R_Ankle[1]), (R_Foot[0]-R_Ankle[0])) * 180 / np.pi
            angle_dict['right_ankle']=int(angle5)
        except Exception as e:
            angle_dict['right_ankle']='NULL'
        
        #left_ankle
        try:
            sc=min(L_Ankle[2], L_Foot[2])
            score['left_ankle']=round(sc*100)
            angle6=np.arctan2((L_Foot[1]-L_Ankle[1]), (L_Foot[0]-L_Ankle[0])) * 180 / np.pi
            angle_dict['left_ankle']=int(angle6)
        except Exception as e:
            angle_dict['left_ankle']='NULL'
      
        #right_wrist
        try:
            sc=min(R_Palm[2], R_Wrist[2])
            score['right_wrist']=round(sc*100)
            angle6=abs(np.arctan2((R_Palm[1]-R_Wrist[1]), (R_Palm[0]-R_Wrist[0])) * 180 / np.pi)
            angle_dict['right_wrist']=int(angle6)
        except Exception as e:
            angle_dict['right_wrist']='NULL'

        #left_wrist
        try:
            sc=min(L_Palm[2], L_Wrist[2], L_Elbow[2])
            score['left_wrist']=round(sc*100)
            angle7=abs(np.arctan2((L_Palm[1]-L_Wrist[1]), (L_Palm[0]-L_Wrist[0])) * 180 / np.pi)
            angle_dict['left_wrist']=int(angle7)
        except Exception as e:
            angle_dict['left_wrist']='NULL'
        #trunk
        Neck=[]
        Neck.append((L_Neck[0]+R_Neck[0])/2)
        Neck.append((L_Neck[1]+R_Neck[1])/2)
        Neck.append((L_Neck[2]+R_Neck[2])/2)
        try:
            if (L_Hip[0]!=0 or L_Hip[1]!=0) and (Neck[0]!=0 or Neck[1]!=0):
                angle9=math.degrees(math.atan2(Neck[1]-L_Hip[1], Neck[0]-L_Hip[0]) - math.atan2(R_Knee[1]-L_Hip[1], R_Knee[0]-L_Hip[0]))
                sc=min(L_Hip[2],Neck[2])
                score['trunk']=round(sc*100)
                angle9=-angle9
                angle_dict['trunk']=int(angle9)
            else:
                angle_dict['trunk']='NULL'
        except Exception as e:
            angle_dict['trunk']='NULL'

        #hip
        try:
            if profile=='Left' or profile=='Right':
                if (R_Hip[0]!=0 or R_Hip[1]!=0) and (R_Knee[0]!=0 or R_Knee[1]!=0):
                    if R_Hip[2]<0.15 or R_Knee[2]<0.15:
                        not_indentified.append('hip')
                    sc=min(R_Hip[2],R_Knee[2])
                    score['hip']=round(sc*100)
                    angle11=math.degrees(math.atan2(50-R_Hip[1], R_Hip[0]-R_Hip[0]) - math.atan2(R_Knee[1]-R_Hip[1], R_Knee[0]-R_Hip[0]))                     
                    angle_dict['hip']=abs(int(angle11))
                else:
                    angle_dict['hip']='NULL'
            elif profile=='Front':
                if (L_Hip[0]!=0 or L_Hip[1]!=0) and (L_Knee[0]!=0 or L_Knee[1]!=0):
                    if L_Hip[2]<0.15 or L_Knee[2]<0.15:
                        not_indentified.append('hip')
                    sc=min(L_Hip[2],L_Knee[2])
                    score['hip']=round(sc*100)
                    angle11=math.degrees(math.atan2(50-L_Hip[1], L_Hip[0]-L_Hip[0]) - math.atan2(L_Knee[1]-L_Hip[1], L_Knee[0]-L_Hip[0]))
                    if angle11<0:
                        angle_dict['hip']=360+int(angle11)
                    else:
                        angle_dict['hip']=abs(int(angle11))
                else:
                    angle_dict['hip']='NULL'
        except Exception as e:
            angle_dict['hip']='NULL'
        #neck
        try:
            neck = math.degrees(np.arctan2(Neck[0],Neck[1]))
            angle_dict['neck']=int(neck)
        except Exception as e:
            angle_dict['neck']='NULL'
    # print(angle_dict)
    rula = rula_score(angle_dict,pose,profile)
    reba = reba_score(angle_dict,pose,profile)
    return (rula['score'],reba['score'])
    
