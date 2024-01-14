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
        for name, phone in data:
            vcf_data = vcf_template.format(name, phone)
            vcf_file.write(vcf_data)

def convert_csv_to_vcf(csv_directory, rows_per_vcf):
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]
    total_converted = 0

    for csv_file in csv_files:
        csv_file_path = os.path.join(csv_directory, csv_file)
        vcf_file_path = os.path.join(csv_directory, 'vcf_files', csv_file.replace('.csv', '_1.vcf'))

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # ข้ามบรรทัดหัวตาราง
            data = []

            for row in csvreader:
                name = entry_name.get()  # ให้ผู้ใช้กรอก Name
                phone = entry_phone.get()  # ให้ผู้ใช้กรอก Phone
                data.append((name, phone))

        os.makedirs(os.path.dirname(vcf_file_path), exist_ok=True)

        for i in range(0, len(data), rows_per_vcf):
            chunk = data[i:i+rows_per_vcf]
            vcf_filename = vcf_file_path.replace('_1.vcf', f'_{i//rows_per_vcf + 1}.vcf')
            create_vcf_file(chunk, vcf_filename)
            total_converted += 1

    messagebox.showinfo('สำเร็จ', f'แปลง CSV เป็น VCF เสร็จสิ้น\nจำนวนไฟล์ที่ถูกแปลง: {total_converted}')

def get_user_input():
    rows_per_vcf = int(entry_rows_per_vcf.get())
    if rows_per_vcf <= 0:
        messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่จำนวน Row ที่ถูกต้อง (มากกว่า 0)")
        return
    convert_csv_to_vcf(csv_directory, rows_per_vcf)

def select_directory():
    global csv_directory
    csv_directory = filedialog.askdirectory()
    if csv_directory:
        user_input_frame.pack()
        select_button.pack_forget()

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
root.title("CSV to VCF Converter")

# สร้างปุ่มเพื่อเลือกโฟลเดอร์
select_button = tk.Button(root, text="เลือกโฟลเดอร์", command=select_directory)
select_button.pack(pady=20)

# สร้าง Frame สำหรับรับข้อมูลจำนวน Row ต่อไฟล์ VCF
user_input_frame = tk.Frame(root)

# สร้าง Entry สำหรับรับข้อมูล Name และ Phone
label_name = tk.Label(user_input_frame, text="Name:")
label_name.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = tk.Entry(user_input_frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_phone = tk.Label(user_input_frame, text="Phone:")
label_phone.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_phone = tk.Entry(user_input_frame)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

label_rows_per_vcf = tk.Label(user_input_frame, text="จำนวน Row ต่อไฟล์ VCF:")
label_rows_per_vcf.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_rows_per_vcf = tk.Entry(user_input_frame)
entry_rows_per_vcf.grid(row=2, column=1, padx=5, pady=5)

button_convert = tk.Button(user_input_frame, text="แปลง CSV เป็น VCF", command=get_user_input)
button_convert.grid(row=3, column=0, columnspan=2, pady=10)

user_input_frame.pack_forget()

# รัน GUI
root.mainloop()
