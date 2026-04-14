import os
import joblib
import pandas as pd

# -----------------------------
# LOAD MODELS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "Models")

models = {
    "adult": joblib.load(os.path.join(MODEL_DIR, "adult_model.joblib")),
    "child": joblib.load(os.path.join(MODEL_DIR, "child_model.joblib")),
    "maternal": joblib.load(os.path.join(MODEL_DIR, "maternal_model.joblib"))
}

# -----------------------------
# HELPER INPUT
# -----------------------------
def get_input(prompt, dtype=str):
    while True:
        try:
            val = input(prompt)
            return dtype(val)
        except:
            print("Invalid input. Try again.")

# -----------------------------
# ADULT INPUT
# -----------------------------
def adult_input():
    print("\n--- Adult Patient ---")

    data = {
        'age_years': get_input("Age (years): ", int),
        'sex': get_input("Sex (Male/Female): "),
        'heart_rate_bpm': get_input("Heart Rate (40-180): ", int),
        'respiratory_rate_bpm': get_input("Resp Rate (10-40): ", int),
        'systolic_bp_mmHg': get_input("Systolic BP (80-200): ", int),
        'spo2_percent': get_input("SpO2 (70-100): ", int),
        'temperature_c': get_input("Temperature (35-41): ", float),
        'level_of_consciousness': get_input("Consciousness (Alert/Voice/Pain/Unresponsive): "),
        'chief_complaint_category': get_input("Complaint (Respiratory/Cardiac/Infection/Trauma/Other): "),
        'duration_days': get_input("Duration (days): ", int),
        'comorbidity_count': get_input("Comorbidities count (0-5): ", int),
        'pain_distress_score_0_10': get_input("Pain (0-10): ", int)
    }

    return pd.DataFrame([data])

# -----------------------------
# CHILD INPUT
# -----------------------------
def child_input():
    print("\n--- Child Patient ---")

    data = {
        'age_months': get_input("Age (months): ", int),
        'weight_kg': get_input("Weight (kg): ", float),
        'fever_present': get_input("Fever (Yes/No): "),
        'fever_duration_days': get_input("Fever duration (days): ", int),
        'respiratory_rate_bpm': get_input("Resp Rate: ", int),
        'chest_indrawing': get_input("Chest Indrawing (Yes/No): "),
        'ability_to_drink_feed': get_input("Feeding (Normal/Reduced/Unable): "),
        'vomiting_everything': get_input("Vomiting (Yes/No): "),
        'convulsions': get_input("Convulsions (Yes/No): "),
        'lethargic_or_unconscious': get_input("Lethargy (Yes/No): "),
        'diarrhea_duration_days': get_input("Diarrhea (days): ", int),
        'dehydration_signs': get_input("Dehydration (None/Some/Severe): "),
        'spo2_percent': get_input("SpO2: ", int),
        'malnutrition_indicator': get_input("Malnutrition (Yes/No): ")
    }

    return pd.DataFrame([data])

# -----------------------------
# MATERNAL INPUT
# -----------------------------
def maternal_input():
    print("\n--- Maternal Patient ---")

    data = {
        'age_years': get_input("Age: ", int),
        'gestational_age_weeks': get_input("Gestation weeks: ", int),
        'systolic_bp_mmHg': get_input("Systolic BP: ", int),
        'heart_rate_bpm': get_input("Heart Rate: ", int),
        'vaginal_bleeding': get_input("Bleeding (Yes/No): "),
        'severe_headache_or_vision_issues': get_input("Headache/Vision (Yes/No): "),
        'abdominal_pain_severity_0_10': get_input("Pain (0-10): ", int),
        'fetal_movement': get_input("Fetal movement (Normal/Reduced/Absent): "),
        'fever_present': get_input("Fever (Yes/No): "),
        'seizures': get_input("Seizures (Yes/No): "),
        'previous_complications': get_input("Previous complications (Yes/No): "),
        'hemoglobin_g_dL': get_input("Hemoglobin: ", float),
        'edema': get_input("Edema (Yes/No): "),
        'duration_days': get_input("Duration (days): ", int)
    }

    return pd.DataFrame([data])

# -----------------------------
# PREDICTION
# -----------------------------
def predict(patient_type, df_input):
    bundle = models[patient_type]

    model = bundle["model"]
    inv_clinical = bundle["inv_clinical"]
    inv_severity = bundle["inv_severity"]

    pred = model.predict(df_input)[0]

    clinical = inv_clinical[int(pred[0])]
    severity = inv_severity[int(pred[1])]

    print("\n==============================")
    print("Prediction Result")
    print("==============================")
    print("Clinical Disposition:", clinical)
    print("Severity Score     :", severity)
    print("==============================\n")

# -----------------------------
# MAIN
# -----------------------------
def main():
    print("\nSelect Patient Type:")
    print("1 → Adult")
    print("2 → Child")
    print("3 → Maternal")

    choice = input("Enter choice: ")

    if choice == "1":
        df_input = adult_input()
        predict("adult", df_input)

    elif choice == "2":
        df_input = child_input()
        predict("child", df_input)

    elif choice == "3":
        df_input = maternal_input()
        predict("maternal", df_input)

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()