import datetime
import random

class PostOpPal:
    def __init__(self, surgery_date, approach_type, side, surgery_name):
        self.surgery_date = surgery_date
        self.approach_type = approach_type 
        self.side = side
        self.surgery_name = surgery_name

    def get_recovery_status(self):
        days_since_surgery = (datetime.date.today() - self.surgery_date).days
        weeks_since_surgery = days_since_surgery / 7

        # 1. Determine Phase Number and Name
        if weeks_since_surgery < 0:
            phase_num, phase_name = 0, "Pre-Op"
            focus = "Surgery date is in the future."
        elif weeks_since_surgery <= 2:
            phase_num, phase_name = 1, "Phase 1: Protection (Weeks 1-2)"
            focus = "Managing pain, reducing swelling, and initiating ROM."
        elif weeks_since_surgery <= 6:
            phase_num, phase_name = 2, "Phase 2: Strengthening (Weeks 2-6)"
            focus = "Progressing ROM, reducing pain, and light strengthening."
        else:
            phase_num, phase_name = 3, "Phase 3: Functional Training (Week 6+)"
            focus = "Strength, stability, and return to day-to-day activity."

        # 2. Assign Exercises based on Phase
        exercise_db = {
            1: ["Isometric quad sets (10 reps)", "Isometric glute sets (10 reps)", "Ankle pumps (20 reps)"],
            2: ["Seated knee flexion stretch (10 reps)", "Sit to stand (10 reps)", "Standing hip outward leg lift (10 reps)"],
            3: ["Balance beam walk (10 feet)", "Step ups/downs (10 reps)", "Squats (2 sets of 10)"]
        }
        
        # 3. Define Clinical Precautions (Ends after 12 weeks)
        precautions = []
        if weeks_since_surgery <= 12:
            if self.approach_type.lower() == "posterior":
                precautions = ["Do not bend hip past 90°", "Do not cross legs", "Do not turn toes inward"]
            elif self.approach_type.lower() == "anterior":
                precautions = ["Avoid hip hyperextension", "Avoid turning toes outward"]
        # If weeks > 12, precautions remain an empty list

        return {
            "num": phase_num,
            "name": phase_name,
            "focus": focus,
            "weeks_out": weeks_since_surgery,
            "exercises": exercise_db.get(phase_num, []),
            "precautions": precautions
        }

# --- INPUT SECTION ---
print("--- Post-Op Pal Setup ---")
print("1: TKR | 2: THR | 3: Hip Fracture ORIF")
choice = input("Enter 1, 2, or 3: ")

surgeries = {"1": "Total Knee Replacement", "2": "Total Hip Replacement", "3": "Hip Fracture ORIF"}
selected_surgery = surgeries.get(choice, "Surgery")
side = input("Surgery Side (Left or Right): ").capitalize()

approach_input = "N/A"
if choice == "2":
    print("\nSelect THR Approach: A: Anterior | P: Posterior")
    approach_choice = input("Enter A or P: ").upper()
    approach_input = "Anterior" if approach_choice == "A" else "Posterior"

print(f"\nEnter Surgery Date:")
y, m, d = int(input("Year: ")), int(input("Month: ")), int(input("Day: "))
surg_date = datetime.date(y, m, d)

# --- RECOVERY LOGIC ---
app = PostOpPal(surg_date, approach_input, side, selected_surgery)
status = app.get_recovery_status()

# --- DASHBOARD DISPLAY ---
print(f"\n" + "="*45)
print(f"DASHBOARD: {app.side} {app.surgery_name}")
if app.approach_type != "N/A": print(f"Approach: {app.approach_type}")
print("="*45)
print(f"CURRENT PHASE: {status['name']}")
print(f"MAIN FOCUS:    {status['focus']}")

# Precautions will only print if weeks <= 12
if status['precautions']:
    print("\n[!] SAFETY PRECAUTIONS (Required until Week 12):")
    for p in status['precautions']: print(f"- {p}")
elif status['weeks_out'] > 12:
    print("\n[✓] Clinical Precautions Lifted: You are past the 12-week safety window.")

# --- FLOWCHART LOGIC: PAIN & DISCHARGE CHECKS ---
can_proceed = False

if status['num'] == 1:
    pain = int(input("\nIs pain 4/10 or less? (Enter 0-10): "))
    if pain <= 4:
        print("Success: Pain managed. Proceeding to exercises (3x reps).")
        can_proceed = True
    else:
        print("STOP: Pain too high. Ice for 20 min and rest.")

elif status['num'] == 2:
    pain = int(input("\nIs pain 3/10 or less? (Enter 0-10): "))
    if pain <= 3:
        print("Success: Pain managed. Proceeding to strengthening (3x reps).")
        can_proceed = True
    else:
        print("ALERT: Pain exceeds threshold. Return to Phase 1 stretches only.")

elif status['num'] == 3:
    returned = input("\nHave you returned to normal function? (y/n): ").lower()
    if returned == 'y':
        print("\n🎉 CONGRATULATIONS: You have reached full recovery. Stop the program.")
    else:
        print("Goal: Continue exercises 3x/day to build total function.")
        can_proceed = True

# --- EXERCISE PROMPT ---
if can_proceed:
    input("\nHit Enter when ready for exercises...")
    for i, ex in enumerate(status['exercises'], 1):
        input(f"[{i}] {ex} - Press Enter when set is complete.")
    
    # Random Fall Prevention Reminder
    tips = [
        "Lighting: Keep hallways well-lit.",
        "Clutter: Remove rugs and loose cords.",
        "Bathroom: Use non-slip mats and grab bars.",
        "Furniture: Ensure clear pathways."
    ]
    print(f"\n[🏠] GENERAL SAFETY TIP: {random.choice(tips)}")

print("\nSession Complete.")