# todo-gui.py
import customtkinter as ctk
import json
import os
import uuid
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TASKS_FILE = "tasks.json"


# ----------------------------- #
# Armazenamento (JSON)
# ----------------------------- #
def carregar_tarefas():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def salvar_tarefas(tarefas):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)


# ----------------------------- #
# Aplicação (GUI)
# ----------------------------- #
class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Minha Lista de Tarefas")
        self.geometry("500x600")

        self.tarefas = carregar_tarefas()

        # Campo de entrada
        self.entry = ctk.CTkEntry(self, placeholder_text="Digite uma nova tarefa...")
        self.entry.pack(pady=20, padx=20, fill="x")
        self.entry.bind("<Return>", lambda e: self.adicionar_tarefa())

        # Botão adicionar
        self.btn_add = ctk.CTkButton(self, text="+ Adicionar", command=self.adicionar_tarefa)
        self.btn_add.pack(pady=5)

        # Lista de tasks
        self.frame_tarefas = ctk.CTkScrollableFrame(self)
        self.frame_tarefas.pack(pady=20, padx=20, fill="both", expand=True)

        self.atualizar_lista()

    # ----------------------------- #
    # Adicionar tarefa
    # ----------------------------- #
    def adicionar_tarefa(self):
        titulo = self.entry.get().strip()
        if not titulo:
            return

        nova = {
            "id": str(uuid.uuid4()),
            "titulo": titulo,
            "feito": False,
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }

        self.tarefas.append(nova)
        salvar_tarefas(self.tarefas)

        self.entry.delete(0, "end")
        self.atualizar_lista()

    # ----------------------------- #
    # Concluir tarefa
    # ----------------------------- #
    def concluir_tarefa(self, tarefa_id):
        for t in self.tarefas:
            if t["id"] == tarefa_id:
                t["feito"] = not t["feito"]  # permite "desfazer"
                salvar_tarefas(self.tarefas)
                self.atualizar_lista()
                return

    # ----------------------------- #
    # Remover tarefa
    # ----------------------------- #
    def remover_tarefa(self, tarefa_id):
        self.tarefas = [t for t in self.tarefas if t["id"] != tarefa_id]
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()

    # ----------------------------- #
    # Atualizar interface
    # ----------------------------- #
    def atualizar_lista(self):
        # Limpar widgets
        for widget in self.frame_tarefas.winfo_children():
            widget.destroy()

        if not self.tarefas:
            label = ctk.CTkLabel(self.frame_tarefas, text="Nenhuma tarefa ainda! ✨", font=("Arial", 16))
            label.pack(pady=50)
            return

        for t in self.tarefas:
            frame = ctk.CTkFrame(self.frame_tarefas)
            frame.pack(pady=6, padx=10, fill="x")

            texto = f"{t['titulo']}  •  {t['criado_em']}"

            check = ctk.CTkCheckBox(
                frame,
                text=texto,
                command=lambda tid=t["id"]: self.concluir_tarefa(tid),
            )
            check.pack(side="left", padx=10, pady=8, fill="x")

            # Visual (concluído)
            if t["feito"]:
                check.select()
                check.configure(
                    text=f"{t['titulo']} (✓)",
                    fg_color="#3a7f3a",
                    text_color="#7cd67c",
                )

            # Remover
            btn_rm = ctk.CTkButton(
                frame,
                text="🗑",
                width=35,
                fg_color="transparent",
                command=lambda tid=t["id"]: self.remover_tarefa(tid),
            )
            btn_rm.pack(side="right", padx=10)


# ----------------------------- #
# Executar app
# ----------------------------- #
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
