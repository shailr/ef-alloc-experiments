filename_pre = "nash_allocs_random_uv_1"

def readdat(directory):
    Us = []
    Vs = []
    As = []
    
    for filenum in range(10):
        # print(directory + filename_pre + str(filenum))

        with open(directory + filename_pre + str(filenum), 'r') as file:
            for c in range(100):
                line = file.readline().split()
                # print(line)
                u_size = (int(line[0]), int(line[1]))
                utemp = []
                for i in range(u_size[0]):
                    utemp.append([float(x) for x in file.readline().split()])
                Us.append(utemp)
                # print(utemp)

                line = file.readline().split()
                # print(line)
                v_size = (int(line[0]), int(line[1]))
                vtemp = []
                for i in range(v_size[0]):
                    vtemp.append([float(x) for x in file.readline().split()])
                Vs.append(vtemp)
                # print(vtemp)

                line = file.readline().split()
                # print(line)
                alloc_size = (int(line[0]), int(line[1]))
                alloctemp = []
                for i in range(alloc_size[0]):
                    alloctemp.append([int(x) for x in file.readline().split()])
                As.append(alloctemp)
                # print(alloctemp)

                line = file.readline()
                # print(line)
    return (Us, Vs, As)