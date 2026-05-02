#PostOp Pal code

# import libraries for date and time and for random module to generate random operations
import datetime
import random

# define functions in the template "class"
class PostOpPal:

    # define the initial info including surgery date, approach type, left or right side, and surgery name
    def __init__(self, surgery_date, approach_type, side, surgery_name):
        self.surgery_date = surgery_date
        self.approach_type = approach_type 
        self.side = side
        self.surgery_name = surgery_name

    # define the recovery status using date input to determine the number of weeks since surgery
    def get_recovery_status(self):
        days_since_surgery = (datetime.date.today() - self.surgery_date).days
        weeks_since_surgery = days_since_surgery / 7

        # classify the patient into different phases based on days since surgery and provide overview or focus of phase goals
        if weeks_since_surgery < 0:
            phase_num, phase_name = 0, "Pre-Op"
            focus = "Surgery date is in the future. Come back after surgery!"
        elif weeks_since_surgery <= 2:
            phase_num, phase_name = 1, "Phase 1: Protection (Weeks 1-2)"
            focus = "Manage pain, reduce swelling, and initiate range of motion."
        elif weeks_since_surgery <= 6:
            phase_num, phase_name = 2, "Phase 2: Strengthening (Weeks 2-6)"
            focus = "Progress range of motion, reduce pain with activity, and light strengthening."
        else:
            phase_num, phase_name = 3, "Phase 3: Functional Training (Week 6+)"
            focus = "Progressive strengthening, joint stabilization, and return to day-to-day activity."

        # assign preset exercises based on the phase
        exercise_db = {
            1: ["Isometric quad sets (10 reps)", "Isometric glute sets (10 reps)", "Ankle pumps (20 reps)"],
            2: ["Seated knee flexion stretch (10 reps)", "Sit to stand (10 reps)", "Standing hip outward leg lift (10 reps)"],
            3: ["Balance beam walk (10 feet)", "Step ups/downs (10 reps)", "Squats (2 sets of 10)"]
        }
        
        # provide clinical precautions for total hip patients if patient is 0-12
        precautions = []
        if weeks_since_surgery <= 12:
            if self.approach_type.lower() == "posterior":
                precautions = ["Do not bend hip past 90°", "Do not cross legs", "Do not turn toes inward"]
            elif self.approach_type.lower() == "anterior":
                precautions = ["Avoid hip hyperextension", "Avoid turning toes outward"]
        # if patient is 12 weeks post-op, leave precautions blank

        return {
            "num": phase_num,
            "name": phase_name,
            "focus": focus,
            "weeks_out": weeks_since_surgery,
            "exercises": exercise_db.get(phase_num, []),
            "precautions": precautions
        }

# print program name
print("--- Post-Op Pal Setup ---")

# ask user to input type of surgery
print("1: Total Knee Replacement | 2: Total Hip Replacement | 3: Hip Fracture ORIF")
choice = input("Enter 1, 2, or 3: ")

surgeries = {"1": "Total Knee Replacement", "2": "Total Hip Replacement", "3": "Hip Fracture ORIF"}
selected_surgery = surgeries.get(choice, "Surgery")

# ask user to input which side left or right
side = input("Surgery Side (Left or Right): ").capitalize()

# for total hip replacement, ask user to select which approach was used (anterior or posterior) as they have different precautions
approach_input = "N/A"
if choice == "2":
    print("\nSelect THR Approach: A: Anterior | P: Posterior")
    approach_choice = input("Enter A or P: ").upper()
    approach_input = "Anterior" if approach_choice == "A" else "Posterior"

# ask user to input the year, month, date to determine surgery date
print(f"\nEnter Surgery Date:")
y, m, d = int(input("Year: ")), int(input("Month: ")), int(input("Day: "))
surg_date = datetime.date(y, m, d)

# --- RECOVERY LOGIC ---
app = PostOpPal(surg_date, approach_input, side, selected_surgery)
status = app.get_recovery_status()

# display or print the surgery information including approach type if applicable, and current phase with main focus area
print(f"\n" + "="*45)
print(f"DASHBOARD: {app.side} {app.surgery_name}")
if app.approach_type != "N/A": print(f"Approach: {app.approach_type}")
print("="*45)
print(f"CURRENT PHASE: {status['name']}")
print(f"MAIN FOCUS:    {status['focus']}")

# for precautions, only display if patient is 0-12 weeks post-op, otherwise patient is exempt from precautions
if status['precautions']:
    print("\n[!] SAFETY PRECAUTIONS (Required until Week 12):")
    for p in status['precautions']: print(f"- {p}")
elif status['weeks_out'] > 12:
    print("\n[✓] Hip Precautions have ended: You are past the 12-week window.")

# check questions to see if patient can progress through program
can_proceed = False

# if pain is low in phase 1, can proceed with program
if status['num'] == 1:
    pain = int(input("\nIs pain 4/10 or less? (Enter 0-10): "))
    if pain <= 4:
        print("Success: Pain managed. Proceeding to exercises (3x reps).")
        can_proceed = True
    
    # if pain is too high, stop and suggest ice and rest
    else:
        print("STOP: Pain too high. Ice for 20 min and rest.")

# if pain is low in phase 2, proceed with program
elif status['num'] == 2:
    pain = int(input("\nIs pain 3/10 or less? (Enter 0-10): "))
    if pain <= 3:
        print("Success: Pain managed. Proceeding to strengthening (3x reps).")
        can_proceed = True
    
    # if pain is too high, then return to stretching from phase 1
    else:
        print("ALERT: Pain exceeds threshold. Return to Phase 1 stretches only.")

# if patient has returned to normal function in phase 3, then stop the program
elif status['num'] == 3:
    returned = input("\nHave you returned to normal function? (y/n): ").lower()
    if returned == 'y':
        print("\n CONGRATULATIONS: You have reached full recovery. Stop the program.")
    
    # if patient still has recovery need, then continue to perform exercises
    else:
        print("Goal: Continue exercises 3x/day to return to normal daily function.")
        can_proceed = True

# prompt patient to hit enter after completing each exercise for the 3 chosen exercises in the phase
if can_proceed:
    input("\nHit Enter when ready for exercises...")
    for i, ex in enumerate(status['exercises'], 1):
        input(f"[{i}] {ex} - Press Enter when set is complete.")
    
    # randomly provide different safety tips
    tips = [
        "Lighting: Keep hallways well-lit.",
        "Clutter: Remove rugs and loose cords.",
        "Bathroom: Use non-slip mats and grab bars.",
        "Furniture: Ensure clear pathways.",
        "Pets: Secure pets when walking during first 3 weeks to avoid tripping over them.",
        "Footwear: Wear shoes with non-slip surfaces such as tennis shoes.",
        "Pain Medication: Be extra careful with moving around after your pain medicine kicks in - it may make you drowsy."
    ]
    print(f"\n GENERAL SAFETY TIP: {random.choice(tips)}")

# end session by printing
print("\nSession Complete.")