import tkinter as tk
from tkinter import messagebox                         # ★新增：拍照弹窗提示
from cv2_enumerate_cameras import enumerate_cameras
import cv2
from PIL import Image, ImageTk
import time                                            # ★新增：生成时间戳文件名

camera = None
current_frame = None
is_running = True

def init_camera(cam_list, camera_label):
    selected = cam_list[0]
    cap = None

    for backend in (cv2.CAP_DSHOW, cv2.CAP_ANY):
        c = cv2.VideoCapture(selected.index, backend)
        if c.isOpened():
            cap = c
            break
        c.release()

    if cap is None:
        camera_label.config(text=f"打开失败：{selected.name}", fg="red")
        return None
    camera_label.config(text=f"正在使用：{selected.name}", fg="green")
    return cap

def update_frame(video_label):
    global camera, current_frame, is_running
    if camera is not None and camera.isOpened():
        ret, frame = camera.read()
        if ret:
            current_frame = frame.copy()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)
            pil_img.thumbnail((640, 480), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(pil_img, master=root)
            video_label.config(image=imgtk)
            video_label.last_image = imgtk
    if is_running:
        root.after(30, lambda: update_frame(video_label))

# ★修改：补全拍照保存逻辑（原来只有 print）
def take_photo():
    global current_frame
    if current_frame is None:
        messagebox.showwarning("提示", "尚未获取到画面，请稍候。")
        return
    # 文件名含时间戳，避免重复覆盖
    filename = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.png"
    cv2.imwrite(filename, current_frame)   # current_frame 为 BGR，直接写入即可
    messagebox.showinfo("拍照成功", f"已保存：{filename}")

def on_closing():
    global camera, is_running
    is_running = False
    if camera is not None:
        camera.release()
    root.destroy()

def main():
    global root, camera

    root = tk.Tk()
    root.title("摄像工具")
    root.geometry("800x600")
    root.resizable(False, False)

    camera_label = tk.Label(root, text="", font=("Microsoft YaHei", 12), fg="blue")
    camera_label.pack(pady=5)

    video_label = tk.Label(root, bg='black')
    video_label.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

    cam_list = list(enumerate_cameras())
    if len(cam_list) != 0:
        camera = init_camera(cam_list, camera_label)
        if camera:
            update_frame(video_label)
    else:
        camera_label.config(text="未找到摄像头")

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    capture_btn = tk.Button(btn_frame, text="拍照", command=take_photo,
                            width=15, height=2, font=("Microsoft YaHei", 12))
    capture_btn.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
