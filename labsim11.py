#from pyscript import document
# import pygame
import time
import asyncio

# print("Hello world from the console")

#output_div = document.querySelector("#textarea")
#output_div.innterText = "Hello World from the web"


menu_options = ("h", "x", "s")
async def start_lab_simulation():
    while True:
        print()
        print("h = help")
        print("x = exit")
        print("s = start")

        print()
        user_input = input("Enter an option: ")  # Removed await - input() is not async

        if user_input == "s":
            print("Processing...")
            time.sleep(5)
            break

        elif user_input == "h":
            print()
            print("** HELP **")
            print("Choose a switch to begin. You will configure 4 switches from the network topology that appears in a separate window.")

        elif user_input == "x":
            print()
            print("See you later!")
            exit()

        else:
            print()
            print("Option not available!")

    # Call start_simulation after the menu
    await start_simulation(task)

task = "\nTasks - All physical cabling is in place and verified. Connectivity between all four switches must be established and operational. All ports are pre-configured as 802.1q trunks.\n\n" \
"1. Configure both SW-1 and SW2 ports e0/1 and e0/2 to permit only the allowed VLANs\n" \
"2. Configure both SW-1 and SW-2 e0/1 ports to send and receive untagged traffic over VLAN99\n"\
"3. Configure both SW-3 and SW-4 ports e0/2 to permit only the allowed VLANs\n"\
"4. Configure both SW-3 and SW-4 ports e0/0 and e0/1 for link aggregation using the industry standard protocol. All ports must immediately negotiate the link aggregation\n"\
"5. Permit only the allowed VLANs on the new link\n"


async def start_simulation(task):

    #pygame.init()

    print("\nNetworking Lab Simulation Question 1")
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

    #Answers for SW1 and SW2
    listA2 = [
        "enable",
        "config t",
        "int e0/1",
        "switchport trunk allowed vlan 56, 77, 99",
        "int e0/2",
        "switchport trunk allowed vlan 56, 77, 99",
        "exit",
        "int e0/1",
        "switchport trunk native vlan 99",
        "end",
        "wr"
    ]

    #Answers for SW3 and SW4
    listA7 = [
        "enable",
        "config t",
        "int range e0-1",
        "channel-group 34 mode active",
        "exit",
        "int po 34",
        "switchport trunk allowed vlan 56, 77, 99",
        "int e0/2",
        "switchport trunk allowed vlan 56, 77, 99",
        "end",
        "wr"
    ]

    listS = []

    list_to_check = ["a","b","c","d"]

    width = 1000
    height = 750
    #screen = pygame.display.set_mode((width, height))
    running = True

    print("Start -->")

    #Picture
    #img = pygame.image.load("images/labsim1.jpg")
    #img = pygame.transform.scale(img, (400, 400))

    x = 300
    y = 250

    async def choose_switch():
        while True:
            # this while loop runs this body of code once for each switch choice.
            print()
            print("SW1 = 1, SW2 = 2, SW3 = 3, SW = 4")
            print()
            user_input = input("Choose a switch to begin. Or press q to quit. : ")  # Removed await
            print()

            # pattern: if we find a problem with the user input, print an
            # error message and use 'continue' to restart the loop.
            if user_input.lower() == 'q':
                break # leave the while loop

            try:
                switch_number = int(user_input)
            except ValueError: # not a number
                print('You must enter a valid switch number')
                continue # go back to the top of the loop to try again.

            if switch_number == 1:
                await compare_SW1()

            elif switch_number == 2:
                await compare_SW2()

            elif switch_number == 3:
                await compare_SW3()

            elif switch_number == 4:
                await compare_SW4()

            else:
                print("Not a valid option. Please try again.")
                continue

    async def compare_SW1():
        while True:
            answer = input("Enter the configuration for SW1: ")  # Removed await
            listA1.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")  # Removed await

            for element in listA1:
                        print(element)

            for number in listA1:
                if number in listA2:
                    listA3.append(number)

            if choice == "yes":
                if set(listA3) == set(listA2):
                    print("You are correct!")
                    listS.append("a")
                    if all(item in listS for item in list_to_check):
                        print("You have completed all switch configurations.")
                        await simulation_over()
                    else:
                        await choose_switch()

                else:
                    print("You are incorrect!")
                    await choose_switch()

    async def compare_SW2():
        while True:
            answer = input("Enter the configuration for SW2: ")  # Removed await
            listA4.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")  # Removed await

            for element in listA4:
                        print(element)

            for number in listA4:
                if number in listA2:
                    listA5.append(number)

            if choice == "yes":
                if set(listA5) == set(listA2):
                    print("You are correct!")
                    listS.append("b")
                    if all(item in listS for item in list_to_check):
                        print("You have completed all switch configurations.")
                        await simulation_over()
                    else:
                        await choose_switch()

                else:
                    print("You are incorrect!")
                    print("End --> ")
                    await choose_switch()

    async def compare_SW3():
        while True:
            answer = input("Enter the configuration for SW3: ")  # Removed await
            listA6.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")  # Removed await

            for element in listA6:
                        print(element)

            for number in listA6:
                if number in listA7:
                    listA8.append(number)

            if choice == "yes":
                if set(listA8) == set(listA7):
                    print("You are correct!")
                    listS.append("c")
                    if all(item in listS for item in list_to_check):
                        print("You have completed all switch configurations.")
                        await simulation_over()
                    else:
                        await choose_switch()
                else:
                    print("You are incorrect!")
                    print("\n")
                    await choose_switch()

    async def compare_SW4():
        while True:
            answer = input("Enter the configuration for SW4: ")  # Removed await
            listA9.append(answer)
            choice = input("Want to stop? if yes type yes, otherwise press any key.\n")  # Removed await

            for element in listA9:
                print(element)

            for number in listA9:
                if number in listA7:
                    listA10.append(number)

            if choice == "yes":
                if set(listA10) == set(listA7):
                    print("You are correct!")
                    listS.append("d")
                    if all(item in listS for item in list_to_check):
                        print("You have completed all switch configurations.")
                        await simulation_over()
                    else:
                        await choose_switch()

                else:
                    print("You are incorrect!")
                    await choose_switch()

    async def simulation_over():
        if all(item in listS for item in list_to_check):
            print("The lab is completed!")
            print("\n")
            exit()
        else:
            print("Please make a selection.")
            await choose_switch()

    while running:

        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        running = False
        #        pygame.quit()
        #    if running:
        #        screen.fill((0, 0, 0))
        #        screen.blit(img, (x, y))
        #        pygame.display.update()

        await choose_switch()

# Main execution
if __name__ == "__main__":
    asyncio.run(start_lab_simulation())