import tkinter as tk
from tkinter import ttk
import json
import random

# JSON 파일 불러오기
with open("g:내 드라이브/2025/공업일반/1인1프_2학기/직탐공일/concepts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

class StudyApp:
    def __init__(self, root): 
        self.root = root
        self.root.title("개념 학습 프로그램")
        self.root.geometry("1280x800")

        self.current_unit = None
        self.concepts = []
        self.explanations = []
        self.current_index = 0

        self.create_main_screen()

    def create_main_screen(self):
        """메인 화면: 단원 선택"""
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="단원을 선택하세요", font=("Arial", 14))
        label.pack(pady=20)

        # ✅ 초기값을 "01. 산업 구조와 공업의 발달"로 설정
        self.unit_var = tk.StringVar(value="01. 산업 구조와 공업의 발달")
        unit_selector = ttk.Combobox(self.root, textvariable=self.unit_var, values=list(data.keys()), width=30, state="readonly")
        unit_selector.pack(pady=10)

        start_button = tk.Button(self.root, text="시작", command=self.start_unit)
        start_button.pack(pady=20)

    def start_unit(self):
        """선택한 단원 시작"""
        self.current_unit = self.unit_var.get()

        # JSON에서 개념-설명 불러오기
        concepts_dict = data[self.current_unit]

        # 개념-설명 쌍 리스트로 변환
        items = list(concepts_dict.items())

        # 규칙 적용: 10개 이하 → 전부, 10개 초과 → 랜덤 10개
        if len(items) <= 10:
            selected_items = items
        else:
            selected_items = random.sample(items, 10)

        # 순서를 랜덤하게 섞기
        random.shuffle(selected_items)

        # 개념/설명 분리
        self.concepts, self.explanations = zip(*selected_items)
        self.current_index = 0
        self.show_concept()

    def show_concept(self):
        """개념 보여주기"""
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.current_index < len(self.concepts):
            concept = self.concepts[self.current_index]

            label = tk.Label(self.root, text=concept, font=("Arial", 16))
            label.pack(pady=40)

            next_button = tk.Button(self.root, text="다음", command=self.next_concept)
            next_button.pack(pady=20)
        else:
            self.show_explanations()

    def next_concept(self):
        """다음 개념"""
        self.current_index += 1
        self.show_concept()

    def show_explanations(self):
        """모든 개념 본 후 설명 보여주기"""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 스크롤바
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Text 위젯
        text_widget = tk.Text(frame, font=("Arial", 12), wrap="word", yscrollcommand=scrollbar.set)
        text_widget.pack(side="left", fill="both", expand=True)

        # 개념+설명 추가
        for c, e in zip(self.concepts, self.explanations):
            text_widget.insert("end", f"{c}: {e}\n\n\n\n")

        # 편집 금지
        text_widget.config(state="disabled")

        scrollbar.config(command=text_widget.yview)

        back_button = tk.Button(self.root, text="메인으로", command=self.create_main_screen)
        back_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyApp(root)
    root.mainloop()
