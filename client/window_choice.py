import tkinter as tk
from tkinter import messagebox,Toplevel

class Window_choice(Toplevel):
    pass

def on_yes():
    messagebox.showinfo("选择结果", "您选择了 '是'。")

def on_no():
    messagebox.showinfo("选择结果", "您选择了 '否'。")

# 创建主窗口
root = tk.Tk()
root.title("选择窗口")

# 创建标签
label = tk.Label(root, text="请选择 '是' 或 '否'：")
label.pack(pady=10)

# 创建 '是' 按钮
yes_button = tk.Button(root, text="是", width=10, command=on_yes)
yes_button.pack(pady=5)

# 创建 '否' 按钮
no_button = tk.Button(root, text="否", width=10, command=on_no)
no_button.pack(pady=5)

# 运行主循环
root.mainloop()
