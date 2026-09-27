import tkinter as tk
from tkinter import messagebox
import threading
from openai import OpenAI

# Put your Groq API key here.
API_KEY = "YOUR_GROQ_API_KEY"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def show_answer(text):
    answer_box.config(state="normal")
    answer_box.delete("1.0", tk.END)
    answer_box.insert(tk.END, text)
    answer_box.config(state="disabled")
    ask_button.config(state="normal")

def ask_ai():
    question = question_box.get("1.0", tk.END).strip()
    if not question:
        show_answer("لطفاً سؤال خود را وارد کنید.")
        return
    if API_KEY == "YOUR_GROQ_API_KEY":
        messagebox.showwarning("API Key", "ابتدا API Key مربوط به Groq را در کد وارد کنید.")
        return

    ask_button.config(state="disabled")
    show_answer("در حال تحلیل سؤال...")

    def worker():
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "تو یک ماشین حساب هوشمند هستی. سؤال کاربر را تحلیل کن، "
                            "محاسبات را دقیق انجام بده و جواب فارسی واضح بده. "
                            "در مسائل ریاضی مراحل حل و جواب نهایی را مشخص کن."
                        )
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0.2
            )
            root.after(0, show_answer, response.choices[0].message.content)
        except Exception as e:
            root.after(0, show_answer, "خطا در اتصال به هوش مصنوعی:\n\n" + str(e))

    threading.Thread(target=worker, daemon=True).start()

def calc(value):
    if value == "C":
        display.delete(0, tk.END)
    elif value == "=":
        try:
            expr = display.get()
            if not all(c in "0123456789+-*/(). " for c in expr):
                raise ValueError
            result = eval(expr, {"__builtins__": {}}, {})
            display.delete(0, tk.END)
            display.insert(0, str(result))
        except Exception:
            display.delete(0, tk.END)
            display.insert(0, "Error")
    else:
        display.insert(tk.END, value)

root = tk.Tk()
root.title("ماشین حساب هوشمند AI")
root.geometry("900x650")
root.configure(bg="#101522")

tk.Label(
    root, text="🧠 ماشین حساب هوشمند AI",
    font=("Arial", 24, "bold"), bg="#101522", fg="white"
).pack(pady=15)

main = tk.Frame(root, bg="#101522")
main.pack(fill="both", expand=True, padx=20, pady=10)

left = tk.Frame(main, bg="#182033")
left.pack(side="left", fill="y", padx=10)

tk.Label(left, text="🧮 ماشین حساب", font=("Arial", 17, "bold"),
         bg="#182033", fg="white").pack(pady=12)

display = tk.Entry(left, font=("Arial", 22), justify="right", width=16)
display.pack(padx=15, pady=10)

buttons = [
    ["7","8","9","/"],
    ["4","5","6","*"],
    ["1","2","3","-"],
    ["0",".","(",")"],
    ["C","+","="]
]
for row in buttons:
    f = tk.Frame(left, bg="#182033")
    f.pack()
    for b in row:
        tk.Button(
            f, text=b, font=("Arial", 16, "bold"),
            width=4, height=2,
            command=lambda x=b: calc(x)
        ).pack(side="left", padx=4, pady=4)

right = tk.Frame(main, bg="#182033")
right.pack(side="right", fill="both", expand=True, padx=10)

tk.Label(right, text="🤖 سؤال خود را بپرس",
         font=("Arial", 17, "bold"), bg="#182033", fg="white").pack(
             anchor="w", padx=15, pady=10)

question_box = tk.Text(right, height=7, font=("Arial", 13), wrap="word")
question_box.pack(fill="x", padx=15)

ask_button = tk.Button(
    right, text="🤖 تحلیل سؤال", font=("Arial", 14, "bold"),
    command=ask_ai, padx=20, pady=8
)
ask_button.pack(pady=10)

tk.Label(right, text="💡 پاسخ هوش مصنوعی",
         font=("Arial", 15, "bold"), bg="#182033", fg="white").pack(
             anchor="w", padx=15, pady=5)

answer_box = tk.Text(right, font=("Arial", 13), wrap="word", state="disabled")
answer_box.pack(fill="both", expand=True, padx=15, pady=5)

root.mainloop()
