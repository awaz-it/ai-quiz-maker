"""
demo_gui.py

Interactive demo that shows how the GUI works with sample data.
This tests the GUI components without requiring a display server.
"""

import tkinter as tk
from gui import QuizMakerGUI
import time

# Sample notes for demo
sample_notes = """
A router is a networking device that forwards data packets between computer networks. 
Routers examine the destination IP address and use routing tables. 
The Internet Protocol (IP) is fundamental for routing. 
Routers operate at the Network Layer (Layer 3) of the OSI model. 
Ethernet is a common LAN technology. 
TCP/IP is the fundamental protocol suite. 
The Domain Name System (DNS) translates domain names to IP addresses.
"""

def demo_workflow():
    """Demonstrate the GUI workflow programmatically."""
    root = tk.Tk()
    app = QuizMakerGUI(root)
    
    # Simulate user pasting notes
    print("[Demo] Inserting sample notes...")
    app.notes_text_widget.insert("1.0", sample_notes)
    
    # Generate quiz
    print("[Demo] Generating quiz...")
    app._generate_quiz()
    
    # Wait a moment
    root.update()
    time.sleep(1)
    
    # Show MCQ tab (already active)
    print("[Demo] Showing MCQ questions...")
    root.update()
    time.sleep(1)
    
    # Navigate through questions
    print("[Demo] Navigating to next question...")
    app._next_question()
    root.update()
    time.sleep(1)
    
    print("[Demo] Switching to True/False tab...")
    app._switch_tab("tf")
    root.update()
    time.sleep(1)
    
    print("[Demo] Switching to Fill-in-the-Blank tab...")
    app._switch_tab("blank")
    root.update()
    time.sleep(1)
    
    print("[Demo] Workflow complete!")
    print(f"[Demo] Generated quiz has:")
    print(f"  - {len(app.current_quiz['mcq'])} MCQs")
    print(f"  - {len(app.current_quiz['tf'])} True/False questions")
    print(f"  - {len(app.current_quiz['blank'])} Fill-in-the-blank questions")
    
    root.destroy()
    print("[Demo] GUI closed successfully!")

if __name__ == "__main__":
    demo_workflow()
