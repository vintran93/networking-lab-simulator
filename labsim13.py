import time
import os

class NetworkLabSim:
    def __init__(self):
        self.current_mode = "menu"
        self.current_switch = None
        
        # Switch configuration storage
        self.listA1 = []  # SW1 user input
        self.listA3 = []  # SW1 correct answers
        self.listA4 = []  # SW2 user input
        self.listA5 = []  # SW2 correct answers
        self.listA6 = []  # SW3 user input
        self.listA8 = []  # SW3 correct answers
        self.listA9 = []  # SW4 user input
        self.listA10 = [] # SW4 correct answers
        self.listS = []   # Completed switches
        
        # Correct answers for SW1 and SW2
        self.listA2 = [
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
        
        # Correct answers for SW3 and SW4
        self.listA7 = [
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
        
        self.list_to_check = ["a", "b", "c", "d"]
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        print("=" * 60)
        print("🌐 NETWORK LAB SIMULATION 🌐".center(60))
        print("=" * 60)
    
    def start_simulation(self):
        self.clear_screen()
        self.print_header()
        print("\nTasks - All physical cabling is in place and verified.")
        print("Connectivity between all four switches must be established and operational.")
        print("All ports are pre-configured as 802.1q trunks.")
        print()
        print("1. Configure both SW-1 and SW2 ports e0/1 and e0/2 to permit only the allowed VLANs")
        print("2. Configure both SW-1 and SW-2 e0/1 ports to send and receive untagged traffic over VLAN99")
        print("3. Configure both SW-3 and SW-4 ports e0/2 to permit only the allowed VLANs")
        print("4. Configure both SW-3 and SW-4 ports e0/0 and e0/1 for link aggregation using the industry standard protocol")
        print("5. Permit only the allowed VLANs on the new link")
        self.show_menu()
    
    def show_menu(self):
        self.current_mode = "menu"
        print("\n" + "=" * 30)
        print("MENU".center(30))
        print("=" * 30)
        print("h = help | x = exit | s = start")
        self.get_user_input("Enter an option: ")
    
    def show_switch_menu(self):
        self.current_mode = "switch_selection"
        print("\nSW1 = 1 | SW2 = 2 | SW3 = 3 | SW4 = 4")
        self.get_user_input("Choose a switch to begin (or 'q' to quit): ")
    
    def get_user_input(self, prompt):
        try:
            user_input = input(prompt).strip()
            self.process_input(user_input)
        except KeyboardInterrupt:
            print("\n\nSee you later!")
            exit()
    
    def process_input(self, user_input):
        if self.current_mode == "menu":
            self.handle_menu_input(user_input)
        elif self.current_mode == "switch_selection":
            self.handle_switch_selection(user_input)
        elif self.current_mode.startswith("configuring_"):
            self.handle_switch_config(user_input)
    
    def handle_menu_input(self, user_input):
        if user_input.lower() == "s":
            print("Processing... Start -->")
            self.show_switch_menu()
        elif user_input.lower() == "h":
            print("\n** HELP **")
            print("Choose a switch to begin. You will configure 4 switches from the network topology.")
            print("Enter the correct Cisco IOS commands for each switch configuration.")
            self.show_menu()
        elif user_input.lower() == "x":
            print("See you later!")
            exit()
        else:
            print("Option not available!")
            self.show_menu()
    
    def handle_switch_selection(self, user_input):
        if user_input.lower() == 'q':
            self.show_menu()
            return
        
        try:
            switch_number = int(user_input)
            if switch_number in [1, 2, 3, 4]:
                self.current_switch = switch_number
                self.current_mode = f"configuring_SW{switch_number}"
                print(f"\n🔧 Configuring SW{switch_number}")
                print("Enter commands one by one (type 'done' when finished):")
                print("Type 'help' to see expected commands for this switch")
                self.get_switch_command()
            else:
                print("Invalid option. Please try again.")
                self.show_switch_menu()
        except ValueError:
            print('Must enter a valid switch number (1-4)')
            self.show_switch_menu()
    
    def get_switch_command(self):
        prompt = f"SW{self.current_switch}> "
        self.get_user_input(prompt)
    
    def handle_switch_config(self, user_input):
        if user_input.lower() == 'done':
            self.check_configuration()
        elif user_input.lower() == 'help':
            self.show_switch_help()
            self.get_switch_command()
        else:
            # Store the configuration command
            if self.current_switch == 1:
                self.listA1.append(user_input)
            elif self.current_switch == 2:
                self.listA4.append(user_input)
            elif self.current_switch == 3:
                self.listA6.append(user_input)
            elif self.current_switch == 4:
                self.listA9.append(user_input)
            
            print(f"Command added: {user_input}")
            self.get_switch_command()
    
    def show_switch_help(self):
        print(f"\n💡 Expected commands for SW{self.current_switch}:")
        if self.current_switch in [1, 2]:
            print("- Enable privileged mode")
            print("- Enter global configuration")
            print("- Configure trunk ports with allowed VLANs")
            print("- Set native VLAN for e0/1")
            print("- Save configuration")
        else:  # SW3 or SW4
            print("- Enable privileged mode")
            print("- Enter global configuration")
            print("- Configure port channel/link aggregation")
            print("- Configure trunk ports with allowed VLANs")
            print("- Save configuration")
    
    def check_configuration(self):
        if self.current_switch == 1:
            # Check SW1 configuration
            for cmd in self.listA1:
                if cmd in self.listA2:
                    self.listA3.append(cmd)
            
            if set(self.listA3) == set(self.listA2):
                print("✅ SW1 configuration CORRECT!")
                self.listS.append("a")
            else:
                print("❌ SW1 configuration INCORRECT!")
                print(f"Missing commands: {set(self.listA2) - set(self.listA3)}")
                self.listA1.clear()
                self.listA3.clear()
        
        elif self.current_switch == 2:
            # Check SW2 configuration
            for cmd in self.listA4:
                if cmd in self.listA2:
                    self.listA5.append(cmd)
            
            if set(self.listA5) == set(self.listA2):
                print("✅ SW2 configuration CORRECT!")
                self.listS.append("b")
            else:
                print("❌ SW2 configuration INCORRECT!")
                print(f"Missing commands: {set(self.listA2) - set(self.listA5)}")
                self.listA4.clear()
                self.listA5.clear()
        
        elif self.current_switch == 3:
            # Check SW3 configuration
            for cmd in self.listA6:
                if cmd in self.listA7:
                    self.listA8.append(cmd)
            
            if set(self.listA8) == set(self.listA7):
                print("✅ SW3 configuration CORRECT!")
                self.listS.append("c")
            else:
                print("❌ SW3 configuration INCORRECT!")
                print(f"Missing commands: {set(self.listA7) - set(self.listA8)}")
                self.listA6.clear()
                self.listA8.clear()
        
        elif self.current_switch == 4:
            # Check SW4 configuration
            for cmd in self.listA9:
                if cmd in self.listA7:
                    self.listA10.append(cmd)
            
            if set(self.listA10) == set(self.listA7):
                print("✅ SW4 configuration CORRECT!")
                self.listS.append("d")
            else:
                print("❌ SW4 configuration INCORRECT!")
                print(f"Missing commands: {set(self.listA7) - set(self.listA10)}")
                self.listA9.clear()
                self.listA10.clear()
        
        # Check if all switches are configured
        if all(item in self.listS for item in self.list_to_check):
            print("\n" + "🎉" * 20)
            print("CONGRATULATIONS!".center(40))
            print("All switch configurations completed!".center(40))
            print("Lab finished successfully!".center(40))
            print("🎉" * 20)
            exit()
        else:
            print(f"\n📊 Progress: {len(self.listS)}/4 switches completed")
            input("Press Enter to continue...")
            self.show_switch_menu()

def main():
    # Initialize and start the simulation
    lab_sim = NetworkLabSim()
    lab_sim.start_simulation()

if __name__ == "__main__":
    main()