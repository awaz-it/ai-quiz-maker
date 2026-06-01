"""
launcher.py

Simple launcher menu to choose between GUI and CLI versions.
Run this file to see a menu with options.
"""

import subprocess
import sys
import os


def main():
    print("\n" + "=" * 60)
    print("  AI QUIZ MAKER - LAUNCHER")
    print("=" * 60)
    print("\nChoose how you want to run the program:\n")
    print("  1) GUI Version (Recommended - visual interface)")
    print("  2) CLI Version (Terminal - paste text)")
    print("  3) Exit\n")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\nLaunching GUI... Please wait...\n")
        subprocess.run([sys.executable, "gui.py"])
    elif choice == "2":
        print("\nLaunching CLI... Paste your notes below:\n")
        subprocess.run([sys.executable, "main.py"])
    elif choice == "3":
        print("\nGoodbye!")
        sys.exit(0)
    else:
        print("\nInvalid choice. Please try again.\n")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
