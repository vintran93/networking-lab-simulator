import pygame

task = "\nTasks - All physical cabling is in place and verified. Connectivity between all four switches must be established and operational. All ports are pre-configured as 802.1q trunks.\n\n" \
"1. Configure both SW-1 and SW2 ports e0/1 and e0/2 to permit only the allowed VLANs\n" \
"2. Configure both SW-1 and SW-2 e0/1 ports to send and receive untagged traffic over VLAN99\n"\
"3. Configure both SW-3 and SW-4 ports e0/2 to permit only the allowed VLANs\n"\
"4. Configure both SW-3 and SW-4 ports e0/0 and e0/1 for link aggregation using the industry standard protocol. All ports must immediately negotiate the link aggregation\n"\
"5. Permit only the allowed VLANs on the new link\n"


def start_simulation(task):

    pygame.init()

    print("\nNetorking Lab Simulation Start")
    print(task)

    #SW1
    listA1 = []
    listA3 = []

    #SW2
    listA4 = []
    listA5 = []

    #SW3
    listA6 = []
    listA8 = []

    #SW4
    listA9 = []
    listA10 = []

    listA2 = ["enable", "config t", "int e0/1", "switchport trunk allowed vlan 56, 77, 99", "int e0/2", "switchport trunk allowed vlan 56, 77, 99",
        "exit", "int e0/1", "switchport trunk native vlan 99", "end", "wr" 
    ]

    listA7 = ["enable", "config t", "int range e0-1", "channel-group 34 mode active", "exit", "int po 34",
        "switchport trunk allowed vlan 56, 77, 99", "int e0/2", "switchport trunk allowed vlan 56, 77, 99", "end", "wr" 
    ]

    width = 1000
    height = 750
    screen = pygame.display.set_mode((width, height))
    running = True

    print("Start -->")

    #Picture
    img = pygame.image.load(".venv/images/labsim1.jpg")
    img = pygame.transform.scale(img, (400, 400))

    x = 300
    y = 250


    def compare_SW1():
        while True:
            answer = (input("Enter the configuration for SW1: "))
            listA1.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")
                                
            for element in listA1:
                        print(element)
                                
            for number in listA1:
                if number in listA2:
                    listA3.append(number)

            if choice == "yes":
                if set(listA3) == set(listA2):
                    print("You are correct!")
                    compare_SW2()
                    pygame.quit()
                    exit()  
                    break
                    
                else:
                    print("You are incorrect!")
                    print("End --> ")   
                    pygame.quit()
                    exit()  
                    break  

    def compare_SW2():
        while True:
            answer = (input("Enter the configuration for SW2: "))
            listA4.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")
                                
            for element in listA4:
                        print(element)
                                
            for number in listA4:
                if number in listA2:
                    listA5.append(number)

            if choice == "yes":
                if set(listA5) == set(listA2):
                    print("You are correct!")
                    compare_SW3()
                    pygame.quit()
                    exit()  
                    exit()  
                    break
                    
                else:
                    print("You are incorrect!")
                    print("End --> ")   
                    pygame.quit()
                    exit()  
                    break  
    
    def compare_SW3():
        while True:
            answer = (input("Enter the configuration for SW3: "))
            listA6.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")
                                
            for element in listA6:
                        print(element)
                                
            for number in listA6:
                if number in listA7:
                    listA8.append(number)

            if choice == "yes":
                if set(listA8) == set(listA7):
                    print("You are correct!")
                    compare_SW4()
                    pygame.quit()
                    exit()  
                    break
                    
                else:
                    print("You are incorrect!")
                    print("End --> ")   
                    pygame.quit()
                    exit()  
                    break  
    
    def compare_SW4():
        while True:
            answer = (input("Enter the configuration for SW4: "))
            listA9.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")
                                
            for element in listA9:
                        print(element)
                                
            for number in listA9:
                if number in listA7:
                    listA10.append(number)

            if choice == "yes":
                if set(listA10) == set(listA7):
                    print("You are correct! You have completed this lab!")
                    print("End --> ")
                    pygame.quit()
                    exit()  
                    break
                    

                else:
                    print("You are incorrect!")
                    print("End --> ")   
                    pygame.quit()
                    exit()  
                    break  

    while running:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if running:  
                screen.fill((0, 0, 0))
                screen.blit(img, (x, y))
                pygame.display.update()
        
        compare_SW1()
        compare_SW2()
        compare_SW3()
        compare_SW4()   
        
start_simulation(task)       


                

        
        

    
            
                


