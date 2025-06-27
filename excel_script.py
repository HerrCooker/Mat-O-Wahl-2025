import pandas as pd
import csv
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Benutzung: python wahlomat_parser.py <Pfad_zur_Excel_Datei>")
        sys.exit(1)

    excel_path = sys.argv[1]

    if not os.path.exists(excel_path):
        print(f"Datei nicht gefunden: {excel_path}")
        sys.exit(1)

    # Lade die Excel-Datei
    df = pd.read_excel(excel_path, sheet_name=0)

    # Entferne die erste Zeile (enthält Header)
    df = df.iloc[1:].reset_index(drop=True)

    # Stimme umrechnen
    def get_vote(row):
        if pd.notna(row[1]):
            return 1
        elif pd.notna(row[2]):
            return -1
        elif pd.notna(row[3]):
            return 0
        else:
            return None

    df["vote"] = df.apply(get_vote, axis=1).astype("Int64")

    # Extrahiere Texte
    deutsch = df[["vote", df.columns[4]]].dropna()
    deutsch.columns = ["vote", "text"]

    englisch = df[["vote", df.columns[5]]].dropna()
    englisch.columns = ["vote", "text"]

    # Generiere Ausgabepfade basierend auf dem Eingabedateinamen
    base_name = os.path.splitext(os.path.basename(excel_path))[0]
    base_dir = os.path.dirname(excel_path)
    csv_de = os.path.join(base_dir, f"{base_name}_jusos_antworten.csv")
    csv_en = os.path.join(base_dir, f"{base_name}_jusos_antworten_en.csv")

    # Speichern
    deutsch.to_csv(csv_de, sep=";", index=False, header=False, quoting=csv.QUOTE_NONNUMERIC)
    englisch.to_csv(csv_en, sep=";", index=False, header=False, quoting=csv.QUOTE_NONNUMERIC)

    print(f"Dateien erfolgreich erstellt:\n- {csv_de}\n- {csv_en}")

if __name__ == "__main__":
    main()

