# main.py

import logging
from control_system import ControlSystem

def main():
    # Configure logging once
    logging.basicConfig(
        filename='progress.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - line %(lineno)d: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    print("=== Goal Manager ===")
    goal = input("Enter your goal: ").strip()
    if not goal:
        print("No goal entered. Exiting.")
        return
    control_system = ControlSystem(goal)
    control_system.run()
    print("All subtasks have been completed. Check 'progress.log' for details.")

if __name__ == "__main__":
    main()
