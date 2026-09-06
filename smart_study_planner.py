"""
Smart Study Planner - A console-based study session tracker
Helps students log, review, and analyse study sessions across subjects over a semester
Data persists across sessions via file storage
"""

import json
from datetime import datetime

# Global variable to store all study sessions
sessions = []
DATA_FILE = "study_log.txt"


def load_sessions():
    """
    Load any existing sessions from the data file at program startup.
    Handles the case where the file doesn't exist (first run).
    Returns: None (updates global sessions list)
    """
    global sessions
    try:
        with open(DATA_FILE, "r") as file:
            sessions = json.load(file)
        print(f"✓ Loaded {len(sessions)} previous session(s) from {DATA_FILE}\n")
    except FileNotFoundError:
        # File doesn't exist yet - first run or fresh start
        sessions = []
    except json.JSONDecodeError:
        # File exists but is corrupted - start fresh and warn user
        print(f"⚠ Warning: {DATA_FILE} is corrupted. Starting with empty session list.\n")
        sessions = []


def save_sessions():
    """
    Save all current sessions to the data file in JSON format.
    Called before exiting the program.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(sessions, file, indent=2)
        print(f"✓ Saved {len(sessions)} session(s) to {DATA_FILE}")
    except IOError as e:
        print(f"✗ Error saving sessions: {e}")


def classify_session(duration):
    """
    Classify a study session by duration.
    Args:
        duration (int): Duration of the session in minutes
    Returns:
        str: One of "Short" (<30 min), "Medium" (30-90 min), or "Long" (>90 min)
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session():
    """
    Prompt user to add a new study session with validation.
    Collects: subject, topic, date/day label, duration (validated as positive integer)
    Stores session as a dictionary in the global sessions list.
    """
    print("\n" + "="*60)
    print("ADD NEW STUDY SESSION")
    print("="*60)
    
    # Get subject
    subject = input("Subject name (English, Arabic, ICT, Mathematics, History): ").strip()
    if not subject:
        print("✗ Subject name cannot be empty.")
        return
    
    # Get topic
    topic = input("Topic covered (Quadratic, Equations): ").strip()
    if not topic:
        print("✗ Topic cannot be empty.")
        return
    
    # Get date/day label
    date_label = input("Date or day label ( Monday,26, Tuesday 26, Wednesday 26, Thursday 26, Friday 26 ): ").strip()
    if not date_label:
        print("✗ Date/day label cannot be empty.")
        return
    
    # Get and validate duration - keep prompting until valid
    while True:
        try:
            duration = int(input("Duration in minutes: "))
            if duration <= 0:
                print("✗ Duration must be a positive number. Please try again.")
                continue
            break
        except ValueError:
            print("✗ Invalid input. Please enter a whole number.")
    
    # Create session dictionary
    session = {
        "subject": subject,
        "topic": topic,
        "date": date_label,
        "duration": duration,
        "classification": classify_session(duration)
    }
    
    # Add to sessions list
    sessions.append(session)
    print(f"✓ Session added! ({session['classification']} session - {duration} minutes)")


def view_sessions():
    """
    Display all logged sessions in a neatly formatted table.
    Shows: Subject, Topic, Date, Duration (min), Classification
    If no sessions exist, display a clear message.
    """
    if not sessions:
        print("\n⊘ No study sessions recorded yet. Start by adding a session!\n")
        return
    
    print("\n" + "="*100)
    print("ALL STUDY SESSIONS")
    print("="*100)
    
    # Print header
    print(f"{'Subject':<15} {'Topic':<25} {'Date':<15} {'Duration (min)':<15} {'Classification':<15}")
    print("-"*100)
    
    # Print each session
    for session in sessions:
        print(f"{session['subject']:<15} {session['topic']:<25} {session['date']:<15} "
              f"{session['duration']:<15} {session['classification']:<15}")
    
    print("="*100 + "\n")


def search_by_subject(subject):
    """
    Search and display sessions for a specific subject (case-insensitive).
    Args:
        subject (str): The subject name to search for
    Shows matching sessions and total time spent on that subject.
    """
    # Case-insensitive search
    matching_sessions = [s for s in sessions if s["subject"].lower() == subject.lower()]
    
    if not matching_sessions:
        print(f"\n⊘ No sessions found for subject: '{subject}'\n")
        return
    
    print("\n" + "="*100)
    print(f"SESSIONS FOR: {subject.upper()}")
    print("="*100)
    
    # Print header
    print(f"{'Topic':<30} {'Date':<15} {'Duration (min)':<15} {'Classification':<15}")
    print("-"*100)
    
    # Print matching sessions and calculate total
    total_minutes = 0
    for session in matching_sessions:
        print(f"{session['topic']:<30} {session['date']:<15} "
              f"{session['duration']:<15} {session['classification']:<15}")
        total_minutes += session['duration']
    
    # Display total time
    total_hours = total_minutes / 60
    print("-"*100)
    print(f"Total time on {subject}: {total_hours:.2f} hours ({total_minutes} minutes)")
    print("="*100 + "\n")


def study_statistics():
    """
    Compute and display comprehensive study statistics:
    - Total hours studied overall
    - Total hours studied per subject
    - Subject with least total study time (weakest area)
    - Single longest session recorded
    """
    if not sessions:
        print("\n⊘ No sessions recorded yet. Add sessions to see statistics.\n")
        return
    
    print("\n" + "="*60)
    print("STUDY STATISTICS")
    print("="*60)
    
    # Overall total hours
    total_minutes = sum(s['duration'] for s in sessions)
    total_hours = total_minutes / 60
    print(f"\nTotal hours studied overall: {total_hours:.2f} hours ({total_minutes} minutes)")
    
    # Hours per subject
    print("\nHours per subject:")
    subject_minutes = {}
    for session in sessions:
        subject = session['subject']
        subject_minutes[subject] = subject_minutes.get(subject, 0) + session['duration']
    
    for subject in sorted(subject_minutes.keys()):
        hours = subject_minutes[subject] / 60
        print(f"  • {subject}: {hours:.2f} hours ({subject_minutes[subject]} minutes)")
    
    # Weakest area (least study time)
    weakest_subject = min(subject_minutes, key=subject_minutes.get)
    weakest_hours = subject_minutes[weakest_subject] / 60
    print(f"\nWeakest area (least study time): {weakest_subject} ({weakest_hours:.2f} hours)")
    
    # Longest session
    longest_session = max(sessions, key=lambda s: s['duration'])
    print(f"\nLongest session: {longest_session['duration']} minutes")
    print(f"  • Subject: {longest_session['subject']}")
    print(f"  • Topic: {longest_session['topic']}")
    print(f"  • Date: {longest_session['date']}")
    print(f"  • Classification: {longest_session['classification']}")
    
    print("="*60 + "\n")


def display_menu():
    """
    Display the main menu options.
    """
    print("\n" + "="*60)
    print("SMART STUDY PLANNER - MAIN MENU")
    print("="*60)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("="*60)


def main():
    """
    Main function that runs the menu-driven interface.
    Displays menu, processes user choices, and handles invalid input gracefully.
    Continues until user chooses to exit (option 5).
    """
    print("\n🎓 Welcome to Smart Study Planner!")
    print("Track your study sessions and analyse your progress across subjects.\n")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_session()
        
        elif choice == "2":
            view_sessions()
        
        elif choice == "3":
            subject = input("\nEnter subject name to search: ").strip()
            if subject:
                search_by_subject(subject)
            else:
                print("✗ Subject name cannot be empty.\n")
        
        elif choice == "4":
            study_statistics()
        
        elif choice == "5":
            print("\n" + "="*60)
            print("Saving your data before exit...")
            save_sessions()
            print("Thank you for using Smart Study Planner! 📚")
            print("="*60 + "\n")
            break
        
        else:
            # Invalid menu choice - reject gracefully without crashing
            print("✗ Invalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    # Load any existing sessions from file at startup
    load_sessions()
    
    # Run the main program
    main()
