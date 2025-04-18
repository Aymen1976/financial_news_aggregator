#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import os
import pandas as pd

def export_json(data, base_filename="output"):
    os.makedirs("../output", exist_ok=True)
    path = f"../output/{base_filename}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def export_csv(data, base_filename="output"):
    os.makedirs("../output", exist_ok=True)
    path = f"../output/{base_filename}.csv"
    if data:
        keys = data[0].keys()
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
    return path

def export_excel(data, base_filename="output"):
    os.makedirs("../output", exist_ok=True)
    path = f"../output/{base_filename}.xlsx"
    if data:
        df = pd.DataFrame(data)
        df.to_excel(path, index=False)
    return path

def save_articles(data, base_filename="output"):
    print("💾 Sauvegarde des fichiers...")
    json_path = export_json(data, base_filename)
    csv_path = export_csv(data, base_filename)
    excel_path = export_excel(data, base_filename)
    print("📁 Exportations terminées :")
    print(" - JSON  :", json_path)
    print(" - CSV   :", csv_path)
    print(" - Excel :", excel_path)
