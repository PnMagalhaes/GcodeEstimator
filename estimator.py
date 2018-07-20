print("###-GCODE-ESTIMATOR-###")

E_last_pos = 0.0
E_curr_pos = 0.0
E_extr_wit = 0.0    #Extruder extruded with


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