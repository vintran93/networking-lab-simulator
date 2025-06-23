import pygame
import time


menu_options = ("h", "x", "s")

while True:
    print()
    print("h = help")
    print("x = exit")
    print("s = start")

    print()
    user_input = input("Enter an option: ")

    if user_input == "s":
        print("Processing...")
        time.sleep(5)
        break
    
    elif user_input == "h":
        print()
        print("** HELP **")
        print("Choose a switch to begin. You will configure 2 routers from the network topology that appears in a separate window.")

    elif user_input == "x":
        print()
        print("See you later!")
        exit()
    
    else:
        print()
        print("Option not available!")
    
task = "\nTasks - Connectivity between four routers has been established. \n \
IP connectivity must be configured in the order presented to complete the implementation. No dynamic routing protocols are included.\n\n" \
"1. Configure static routing using host routes to establish connectivity from router R3 to the router R1 Loopback address using the source IP of 209.165.200.230. \n" \
"2. Configure an IPv4 default route on router R3 destined for router R4. \n"\
"3. Configure an IPv6 default router on router R2 destined for router R4. \n"\

def start_simulation(task):
    
    pygame.init()

    print("\nNetworking Lab Simulation Question 3")
    print(task)

    #SW2
    listA4 = []
    listA5 = []

    #SW3
    listA6 = []
    listA8 = []

    #Answers R3
    listA2 = [
        "config t", 
        "ip route 192.168.1.1 255.255.255.255 209.165.200.229", 
        "end", 
        "copy running start"
    ]

    #Answers for R2
    listA7 = [
        "config t", 
        "ip route 0.0.0.0 0.0.0.0 209.165.202.130", 
        "ipv6 route ::0 2001:db8:abcd::2", 
        "end", 
        "copy running start"
    ]

    listS = []

    list_to_check = ["a","b"]

    width = 1000
    height = 750
    screen = pygame.display.set_mode((width, height))
    running = True

    print("Start -->")

    #Picture
    img = pygame.image.load("images/labsim3.jpg")
    img = pygame.transform.scale(img, (750, 400))

    x = 200
    y = 250

    def choose_router():
        print("\n")
        print("R3 = 3, R2 = 2")
        print("\n")
        user_input = int(input("Choose a router to begin. Or press q to quit. : "))
        print("\n")

        if user_input == 3:
            compare_R3()

        elif user_input == 2:
            compare_R2()

        else:
            print()
            print("Not a valid option. Please try again. ")
            choose_router()

    def compare_R2():
        while True:
            answer = (input("Enter the configuration for R2: "))
            listA4.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")
                                
            for element in listA4:
                        print(element)
                                
            for number in listA4:
                if number in listA7:
                    listA5.append(number)

            if choice == "yes":
                if set(listA5) == set(listA7):
                    print("You are correct!")
                    listS.append("a")
                    if all(item in listS for item in list_to_check):
                        print("You have completed all switch configurations.")
                        simulation_over()
                    else:
                        choose_router()
                    
                else:
                    print("You are incorrect!")
                    print("End --> ")   
                    choose_router()
    
    def compare_R3():
        while True:
            answer = (input("Enter the configuration for R3: "))
            listA6.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")
                                
            for element in listA6:
                        print(element)
                                
            for number in listA6:
                if number in listA2:
                    listA8.append(number)

            if choice == "yes":
                if set(listA8) == set(listA2):
                    print("You are correct!")
                    listS.append("b")
                    if all(item in listS for item in list_to_check):
                        print("You have completed all router configurations.")
                        simulation_over()
                    else:
                        choose_router()
                else:
                    print("You are incorrect!")
                    print("\n")   
                    choose_router()

    def simulation_over():
        if all(item in listS for item in list_to_check):
            print("The lab is completed!")
            print("\n")
            exit()
        else:
            print("Please make a selection.")
            choose_router()

    while running:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if running:  
                screen.fill((0, 0, 0))
                screen.blit(img, (x, y))
                pygame.display.update() 
        
        choose_router()

start_simulation(task) 
        
             