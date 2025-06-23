import pygame

task = "\nTasks - Physical connectivity is implemented between the two Layer 2 switches, and the network connectivity between them must be configured. \n\n" \
"1. Configure an LACP EtherChannel and number it as 44; configure it between switches SW1 and SW2 using interfaces Ethemet0/0 and Ethernet0/1 on both sides. \n \
The LACP mode must match on both ends.\n" \
"2. Configure the EtherChannel as a trunk link.\n"\
"3. Configure the trunk link with 802.1q tags.\n"\
"4. Configure VLAN 'MONITORING' as the untagged VLAN of the EtherChannel.\n"

def start_simulation(task):

    pygame.init()

    print("\nNetworking Lab Simulation Question 2")
    print(task)

    #SW1
    listA1 = []
    listA3 = []

    #SW2
    listA4 = []
    listA5 = []

    #Answers for SW1 and SW2
    listA2 = [
        "interface range eth0/0-1", 
        "channel-group 44 mode active", 
        "interface port44", 
        "switchport trunk encapsulation dot1q", 
        "switchport mode trunk", 
        "switchport trunk native vlan 746",
        "no shutdown", 
        "end" 
    ]

    width = 1000
    height = 750
    screen = pygame.display.set_mode((width, height))
    running = True

    print("Start -->")

    #Picture
    img = pygame.image.load("images/labsim2.jpg")
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
                    print("You are correct! You have complete this lab!")
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
        
start_simulation(task)       

