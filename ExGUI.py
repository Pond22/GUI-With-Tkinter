import os
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def create_vcf_file(data, vcf_filename):
    vcf_template = """BEGIN:VCARD
VERSION:3.0
FN:{}
TEL;TYPE=VOICE,CELL:{}
END:VCARD
"""
    with open(vcf_filename, 'w', encoding='utf-8') as vcf_file:
        for row in data:
            name = row[0]  # สมมุติว่า Name อยู่ในคอลัมน์แรก
            phone = row[1]  # สมมุติว่า Phone อยู่ในคอลัมน์ที่สาม
            vcf_data = vcf_template.format(name, phone)
            vcf_file.write(vcf_data)

def convert_csv_to_vcf(csv_directory):
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]
    total_converted = 0

    for csv_file in csv_files:
        csv_file_path = os.path.join(csv_directory, csv_file)
        vcf_file_path = os.path.join(csv_directory, 'vcf_files', csv_file.replace('.csv', '_1.vcf'))

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # ข้ามบรรทัดหัวตาราง
            data = [row for row in csvreader]

        max_rows_per_vcf = 7000
        os.makedirs(os.path.dirname(vcf_file_path), exist_ok=True)

        for i in range(0, len(data), max_rows_per_vcf):
            chunk = data[i:i+max_rows_per_vcf]
            vcf_filename = vcf_file_path.replace('_1.vcf', f'_{i//max_rows_per_vcf + 1}.vcf')
            create_vcf_file(chunk, vcf_filename)
            total_converted += 1

    messagebox.showinfo('สำเร็จ', f'แปลง CSV เป็น VCF เสร็จสิ้น\nจำนวนไฟล์ที่ถูกแปลง: {total_converted}')

def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        convert_csv_to_vcf(folder_selected)

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
root.title("CSV to VCF Converter")

# สร้างปุ่มเพื่อเลือกโฟลเดอร์
select_button = tk.Button(root, text="เลือกโฟลเดอร์", command=select_directory)
select_button.pack(pady=20)

# รัน GUI
root.mainloop()
