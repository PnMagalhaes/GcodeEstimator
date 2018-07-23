import math
print("###-GCODE-ESTIMATOR-###")

E_last_pos = 0.0
E_curr_pos = 0.0
E_extr_wit = 0.0    #Extruder extruded with

F_curr = 0.01          #current feedrate
F_next = 100          #next feedrate
F_update = False

X_last_pos = 0.0
X_curr_pos = 0.0
X_next_pos = 0.0
Y_last_pos = 0.0
Y_curr_pos = 0.0
Y_next_pos = 0.0
Z_curr_pos = 0.0
Z_next_pos = 0.0
Z_layer_d = 0.0
XY_dist = 0.0

elapsed_time = 0.0
elapsed_time_del = 0.0
deltaX = 0.0
delta_F = 1.0
deltaY = 0.0

a = 500             #aceleration = 500mm/s2
#open file
with  open("Cubo_Med_20.gcode","r") as file:
    lines = []                                  #dictionary to save lines
    for line in file:
        curr_line = {}
        for command in line.split():
            #read only the lines that contains valid commands
            if len(command)>0 and command[0] != ';':
                try:
                    #valid command -> save
                    if command[1:].isdigit():
                        curr_line[command[0]] = int(command[1:])
                    else:
                        curr_line[command[0]] = float(command[1:])
                except Exception as e:
                    print("erro_____________________________________________________________________________")
            else:
                break
        #if line is not empty
        if curr_line != {}:
            lines.append(curr_line)
    #Check the lines
    for line in lines:
        for command in ['G','X','Y','Z','E','F']:
            for k in line.keys():
                if command == k.upper():
                    #print(k + str(line[k]) + ' ',end="")
                    a=2
        
    
    #calculation of the filament with in mm
    for line in lines:
        for k in line.keys():
            E_curr_pos = line[k]
            if k.upper()=='E':
                E_curr_pos = line[k]
                #print(k + str(line[k]) )
                if   line[k] > E_last_pos:
                    #extrusion
                    E_extr_wit = E_extr_wit + (E_curr_pos - E_last_pos)
                    E_last_pos = E_curr_pos
                elif line[k] < E_last_pos:
                    #retraction
                    E_extr_wit = E_extr_wit - (E_last_pos - E_curr_pos)
                    E_last_pos = E_curr_pos
                    a = 2
                else:
                    #stoped
                    a = 1
    print("Total amount ou filament in mm:",E_extr_wit)

    #distance calculation in XYZ axis
    for line in lines:
        for k in line.keys():
            if k.upper() == 'X':
                #new X next position
                X_next_pos = line[k]            
                #print(X_next_pos)
            elif k.upper() == 'Y':
                #new Y next position
                Y_next_pos = line[k]
            elif k.upper() == 'Z':
                #Layer change 
                Z_next_pos = line[k]               
                Z_layer_d = Z_next_pos-Z_curr_pos
            elif k.upper() == 'F':
                #new feedrate
                F_next = line[k]/60
                
        
        d_XY = math.sqrt( (X_next_pos-X_curr_pos)**2 + (Y_next_pos-Y_curr_pos)**2 )
       
        if abs(d_XY) < 3:
            #distancia a percorrer < 2mm
            vf = math.sqrt(F_curr**2 + a*d_XY)
            elapsed_time_del = 2*(vf-F_curr)/a
        else:
            elapsed_time_del = d_XY/F_next
        
        elapsed_time = elapsed_time + elapsed_time_del + Z_layer_d/F_next 
        XY_dist = XY_dist + d_XY
        #update X and Y current position
        X_last_pos = X_curr_pos
        X_curr_pos = X_next_pos
        Y_curr_pos = Y_next_pos
        Z_curr_pos = Z_next_pos
        F_curr     = F_next
        F_update = False
    print("elapsed time in min",elapsed_time/60)