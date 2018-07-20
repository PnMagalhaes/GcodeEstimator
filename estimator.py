print("###-GCODE-ESTIMATOR-###")

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
                    print(k + str(line[k]) + ' ',end="")
        print('')