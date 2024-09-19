import tkinter as tk  
from tkinter import scrolledtext  
  
def on_change(event=None):  
    if event:  # 如果事件被触发  
        print("文本正在被编辑")  
  
# 创建主窗口  
root = tk.Tk()
root.title("ScrolledText 示例")

# 创建ScrolledText组件
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
  
# 绑定事件
text_area.bind("<Key>", on_change)  
text_area.bind("<KeyRelease>", on_change)  
text_area.bind("<Button-1>", on_change)  # 鼠标左键点击  
  
# 运行主循环  
root.mainloop()