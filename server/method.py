from datetime import datetime

def debug_send(message:str):
    new_str = f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]:{message}"
    print(new_str)
    old_data = ""
    try:
        with open('server/debug/debug.txt',"r",encoding = 'utf-8') as old_file:
            old_data = old_file.read()
        with open('server/debug/debug.txt',"w",encoding = 'utf-8') as file:
            file.write(old_data + '\n' +new_str)
        file.close()
    except:pass