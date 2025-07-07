import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
from main import JogoRPG

class RPGAppPremium:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG da Silva DELUXE")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#34495e")
        self.style.configure("TButton", padding=6, relief="flat", background="#3498db")
        self.style.map("TButton", background=[("active", "#2980b9")])
        
        self.game = JogoRPG()
        self.cell_size = 12
        self.images = self.load_images()
        self.setup_ui()
        self.update_ui()
        
        # Efeitos sonoros (opcional - descomente se tiver pygame)
        # self.sounds = {
        #     "walk": pygame.mixer.Sound("walk.wav"),
        #     "combat": pygame.mixer.Sound("combat.wav")
        # }

    def load_images(self):
        """Carrega imagens para sprites (substitua pelos seus arquivos)"""
        images = {}
        try:
            # Exemplo com sprites básicos (substitua por suas imagens)
            for entity in ["player", "goblin", "dragon", "item", "merchant"]:
                img = Image.new("RGBA", (7, 7), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                images[entity] = ImageTk.PhotoImage(img)
        except:
            # Fallback para texto se imagens não carregarem
            images = None
        return images

    def setup_ui(self):
        # Layout principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Área do mapa
        self.map_frame = ttk.LabelFrame(main_frame, text="Dungeon", padding=10)
        self.map_frame.grid(row=0, column=0, sticky="nsew")
        
        self.canvas = tk.Canvas(
            self.map_frame,
            width=self.game.game_map.largura * self.cell_size,
            height=self.game.game_map.altura * self.cell_size,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack()

        # Painel direito
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10)

        # Status do jogador
        self.status_frame = ttk.LabelFrame(right_panel, text="Status", padding=10)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.hp_bar = ttk.Progressbar(self.status_frame, length=200, mode="determinate")
        self.hp_bar.pack()
        self.hp_label = ttk.Label(self.status_frame, text="HP: 100/100")
        self.hp_label.pack()
        
        ttk.Label(self.status_frame, text=f"Nível: {self.game.player.nivel}").pack()
        ttk.Label(self.status_frame, text=f"Ouro: {self.game.player.ouro}").pack()

        # Controles
        controls_frame = ttk.LabelFrame(right_panel, text="Controles", padding=10)
        controls_frame.pack(fill=tk.X, pady=5)
        
        control_grid = ttk.Frame(controls_frame)
        control_grid.pack()
        
        ttk.Button(control_grid, text="↑", command=lambda: self.move_player('cima')).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(control_grid, text="←", command=lambda: self.move_player('esquerda')).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(control_grid, text="↓", command=lambda: self.move_player('baixo')).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(control_grid, text="→", command=lambda: self.move_player('direita')).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Button(controls_frame, text="Menu (E)", command=self.show_menu).pack(fill=tk.X, pady=2)
        ttk.Button(controls_frame, text="Loja (L)", command=self.show_shop).pack(fill=tk.X, pady=2)
        ttk.Button(controls_frame, text="Habilidades (H)", command=self.show_skills).pack(fill=tk.X, pady=2)

        # Log de mensagens
        self.log_frame = ttk.LabelFrame(right_panel, text="Log", padding=10)
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(
            self.log_frame,
            height=10,
            width=40,
            bg="#1a1a1a",
            fg="white",
            insertbackground="white",
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        scrollbar = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Configuração de teclado
        self.root.bind("<w>", lambda e: self.move_player('cima'))
        self.root.bind("<a>", lambda e: self.move_player('esquerda'))
        self.root.bind("<s>", lambda e: self.move_player('baixo'))
        self.root.bind("<d>", lambda e: self.move_player('direita'))
        self.root.bind("<e>", lambda e: self.show_menu())
        self.root.bind("<l>", lambda e: self.show_shop())
        self.root.bind("<h>", lambda e: self.show_skills())

        # Configure o grid para expansão
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def move_player(self, direction):
        self.game.mover_jogador(direction)
        # if hasattr(self, 'sounds'):
        #     self.sounds["walk"].play()
        self.update_ui()
        
        # Verifica se entrou em combate
        if self.game.game_state.get_state() == "combate":
            self.show_combat()

    def update_ui(self):
        # Atualiza canvas
        self.canvas.delete("all")
        
        # Desenha mapa
        for y in range(self.game.game_map.altura):
            for x in range(self.game.game_map.largura):
                cell = self.game.game_map.mapa[y][x]
                color = "#555555" if cell == "#" else "#222222"
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill=color,
                    outline="#444444",
                    width=1
                )

        # Desenha entidades
        entities = {
            "player": ("@", "#e74c3c"),
            "enemy": ("E", "#c0392b"),
            "item": ("i", "#2ecc71"),
            "npc": ("M", "#3498db"),
            "portal": ("O", "#9b59b6")
        }

        # Desenha portal primeiro (fundo)
        for portal in self.game.game_map.portais:
            self.draw_entity(portal['x'], portal['y'], "O", "#9b59b6")

        # Desenha itens
        for item in self.game.game_map.itens:
            self.draw_entity(item.x, item.y, "i", "#2ecc71")

        # Desenha NPCs
        for npc in self.game.game_map.npcs:
            self.draw_entity(npc.x, npc.y, "M", "#3498db")

        # Desenha inimigos
        for enemy in self.game.game_map.inimigos:
            color = "#e67e22" if enemy.chefao else "#c0392b"
            self.draw_entity(enemy.x, enemy.y, "E", color)

        # Desenha jogador por último (sobreposto)
        self.draw_entity(self.game.player.x, self.game.player.y, "@", "#e74c3c")

        # Atualiza status
        self.hp_bar["value"] = (self.game.player.vida / self.game.player.vida_max) * 100
        self.hp_label.config(text=f"HP: {self.game.player.vida}/{self.game.player.vida_max}")
        
        # Atualiza log
        self.update_log()

    def draw_entity(self, x, y, symbol, color):
        if self.images:
            # Usa sprites se disponíveis
            img_key = "player" if symbol == "@" else "goblin" if symbol == "E" else "item"
            self.canvas.create_image(
                x * self.cell_size + self.cell_size // 2,
                y * self.cell_size + self.cell_size // 2,
                image=self.images.get(img_key, None)
            )
        else:
            # Fallback para texto
            self.canvas.create_text(
                x * self.cell_size + self.cell_size // 2,
                y * self.cell_size + self.cell_size // 2,
                text=symbol,
                fill=color,
                font=("Consolas", 12, "bold")
            )

    def update_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        for msg in self.game.game_state.get_historico():
            tag = "combat" if "combate" in msg.lower() else "loot" if "ouro" in msg.lower() else "system"
            self.log_text.insert(tk.END, msg + "\n", tag)
        
        self.log_text.tag_config("combat", foreground="#e74c3c")
        self.log_text.tag_config("loot", foreground="#f1c40f")
        self.log_text.tag_config("system", foreground="#3498db")
        
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def show_menu(self):
        menu_win = tk.Toplevel(self.root)
        menu_win.title("Menu do Jogador")
        menu_win.geometry("400x500")
        
        notebook = ttk.Notebook(menu_win)
        
        # Aba de status
        status_frame = ttk.Frame(notebook)
        self.create_status_tab(status_frame)
        notebook.add(status_frame, text="Status")
        
        # Aba de inventário
        inv_frame = ttk.Frame(notebook)
        self.create_inventory_tab(inv_frame)
        notebook.add(inv_frame, text="Inventário")
        
        # Aba de missões
        quest_frame = ttk.Frame(notebook)
        self.create_quests_tab(quest_frame)
        notebook.add(quest_frame, text="Missões")
        
        notebook.pack(expand=True, fill=tk.BOTH)

    def create_status_tab(self, frame):
        ttk.Label(frame, text=f"Classe: {self.game.player.classe or 'Nenhuma'}").pack(pady=5)
        ttk.Label(frame, text=f"Nível: {self.game.player.nivel}").pack(pady=5)
        
        hp_frame = ttk.Frame(frame)
        ttk.Label(hp_frame, text="Vida:").pack(side=tk.LEFT)
        ttk.Progressbar(hp_frame, length=200, value=self.game.player.vida).pack(side=tk.LEFT, padx=5)
        hp_frame.pack(pady=5)
        
        ttk.Label(frame, text=f"Ataque: {self.game.player.ataque}").pack(pady=5)
        ttk.Label(frame, text=f"Defesa: {self.game.player.defesa}").pack(pady=5)
        ttk.Label(frame, text=f"XP: {self.game.player.xp}/{self.game.player.nivel * 100}").pack(pady=5)
        ttk.Label(frame, text=f"Ouro: {self.game.player.ouro}").pack(pady=5)

    def create_inventory_tab(self, frame):
        if not self.game.player.inventario:
            ttk.Label(frame, text="Inventário vazio").pack()
            return
            
        tree = ttk.Treeview(frame, columns=("qty", "use"), show="headings")
        tree.heading("#0", text="Item")
        tree.heading("qty", text="Quantidade")
        tree.heading("use", text="Usar")
        
        for item, qty in self.game.player.inventario.items():
            tree.insert("", tk.END, text=item, values=(qty, "✔" if item in ["Poção de Vida", "Poção de Ataque"] else ""))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        def use_item():
            selected = tree.focus()
            if selected:
                item = tree.item(selected, "text")
                if item in ["Poção de Vida", "Poção de Ataque"]:
                    self.game.player.usar_item(item, self.game.game_state.log_mensagem)
                    self.update_ui()
                    menu_win.destroy()
        
        ttk.Button(frame, text="Usar Item", command=use_item).pack(pady=5)

    def create_quests_tab(self, frame):
        missions = self.game.mission_system.get_active_missions()
        if not missions:
            ttk.Label(frame, text="Nenhuma missão ativa").pack()
            return
            
        for mission in missions:
            ttk.Label(frame, text=mission['objetivo'], font=("Arial", 10, "bold")).pack(anchor=tk.W)
            progress = ttk.Progressbar(
                frame,
                length=200,
                maximum=mission['alvo'],
                value=mission['quantidade']
            )
            progress.pack(pady=2)
            ttk.Label(frame, text=f"{mission['quantidade']}/{mission['alvo']}").pack(anchor=tk.W)
            ttk.Separator(frame).pack(fill=tk.X, pady=5)

    def show_shop(self):
        # Verifica se há mercador próximo
        mercador_proximo = any(
            abs(self.game.player.x - npc.x) <= 1 and abs(self.game.player.y - npc.y) <= 1
            for npc in self.game.game_map.npcs if npc.tipo == "Mercador"
        )

        if not mercador_proximo:
            messagebox.showinfo("Loja", "Nenhum mercador por perto!")
            return

        shop_win = tk.Toplevel(self.root)
        shop_win.title("Loja do Mercador")
        shop_win.geometry("500x400")

        ttk.Label(shop_win, text=f"Seu ouro: {self.game.player.ouro}", font=("Arial", 12, "bold")).pack(pady=10)

        tree = ttk.Treeview(shop_win, columns=("price", "buy"), show="headings")
        tree.heading("#0", text="Item")
        tree.heading("price", text="Preço")
        tree.heading("buy", text="Comprar")
        
        for idx, item in enumerate(self.game.shop_system.get_shop_items(), 1):
            tree.insert("", tk.END, text=item.nome, values=(item.preco, "✔"))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def buy_item():
            selected = tree.focus()
            if selected:
                item_idx = tree.index(selected)
                self.game.shop_system.comprar_item(item_idx)
                self.update_ui()
                shop_win.destroy()
                messagebox.showinfo("Sucesso", f"Você comprou {tree.item(selected, 'text')}!")
        
        ttk.Button(shop_win, text="Comprar Item Selecionado", command=buy_item).pack(pady=10)

    def show_skills(self):
        skills_win = tk.Toplevel(self.root)
        skills_win.title("Habilidades")
        skills_win.geometry("300x400")
        
        ttk.Label(skills_win, text="Habilidades Disponíveis:", font=("Arial", 12, "bold")).pack(pady=10)
        
        for skill in self.game.player.habilidades:
            ttk.Label(skills_win, text=f"• {skill}").pack(anchor=tk.W, padx=20)
        
        if self.game.game_state.get_state() == "combate":
            ttk.Separator(skills_win).pack(fill=tk.X, pady=10)
            ttk.Label(skills_win, text="Usar em Combate:", font=("Arial", 10)).pack()
            
            for idx, skill in enumerate(self.game.player.habilidades, 1):
                ttk.Button(
                    skills_win,
                    text=skill,
                    command=lambda s=skill: self.use_skill_in_combat(s, skills_win)
                ).pack(fill=tk.X, padx=20, pady=2)

    def use_skill_in_combat(self, skill, window):
        new_state = self.game.combat_system.aplicar_habilidade(skill)
        self.game.game_state.set_state(new_state)
        window.destroy()
        self.update_ui()
        
        if new_state == "explorando":
            messagebox.showinfo("Vitória", "Inimigo derrotado!")
        elif new_state == "game_over":
            self.handle_game_over()

    def show_combat(self):
        combat_win = tk.Toplevel(self.root)
        combat_win.title("Combate!")
        combat_win.geometry("500x400")
        
        enemy = self.game.combat_system.current_enemy
        
        # Cabeçalho
        ttk.Label(
            combat_win,
            text=f"Combate contra {enemy.tipo}!" + (" (CHEFÃO)" if enemy.chefao else ""),
            font=("Arial", 14, "bold"),
            foreground="red" if enemy.chefao else "black"
        ).pack(pady=10)
        
        # Barras de HP
        self.create_hp_bar(combat_win, "Você", self.game.player.vida, self.game.player.vida_max)
        self.create_hp_bar(combat_win, enemy.tipo, enemy.vida, enemy.vida_max)
        
        # Ações
        ttk.Label(combat_win, text="Escolha sua ação:", font=("Arial", 10)).pack(pady=10)
        
        action_frame = ttk.Frame(combat_win)
        action_frame.pack()
        
        ttk.Button(action_frame, text="Atacar", command=lambda: self.resolve_combat("atacar", combat_win)).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Habilidade", command=lambda: self.show_skills()).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Usar Item", command=lambda: self.use_item_in_combat(combat_win)).grid(row=0, column=2, padx=5)
        ttk.Button(action_frame, text="Fugir", command=lambda: self.resolve_combat("fugir", combat_win)).grid(row=0, column=3, padx=5)

    def create_hp_bar(self, parent, name, current, max_hp):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(frame, text=f"{name}:", width=10).pack(side=tk.LEFT)
        ttk.Progressbar(frame, length=200, value=(current/max_hp)*100).pack(side=tk.LEFT, padx=5)
        ttk.Label(frame, text=f"{current}/{max_hp}").pack(side=tk.LEFT)

    def resolve_combat(self, action, window):
        new_state = self.game.combat_system.resolver_combate_acao(action)
        self.game.game_state.set_state(new_state)
        window.destroy()
        self.update_ui()
        
        if new_state == "explorando":
            messagebox.showinfo("Combate", "Inimigo derrotado!" if action != "fugir" else "Fuga bem-sucedida!")
        elif new_state == "game_over":
            self.handle_game_over()
        elif new_state == "vitoria":
            messagebox.showinfo("Vitória Épica", "Você derrotou o chefão!")

    def use_item_in_combat(self, window):
        item_win = tk.Toplevel(window)
        item_win.title("Usar Item")
        
        ttk.Label(item_win, text="Selecione um item para usar:").pack(pady=10)
        
        usable_items = [item for item in self.game.player.inventario.keys() if item in ["Poção de Vida", "Poção de Ataque"]]
        
        if not usable_items:
            ttk.Label(item_win, text="Nenhum item utilizável").pack()
            return
            
        for item in usable_items:
            ttk.Button(
                item_win,
                text=f"{item} ({self.game.player.inventario[item]})",
                command=lambda i=item: self.use_selected_item(i, item_win, window)
            ).pack(fill=tk.X, padx=20, pady=2)

    def use_selected_item(self, item, item_window, combat_window):
        new_state = self.game.combat_system.usar_item_combate(item)
        item_window.destroy()
        combat_window.destroy()
        self.game.game_state.set_state(new_state)
        self.update_ui()
        
        if new_state == "game_over":
            self.handle_game_over()

    def handle_game_over(self):
        if messagebox.askyesno("Game Over", "Você foi derrotado! Jogar novamente?"):
            self.game = JogoRPG()
            self.update_ui()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RPGAppPremium(root)
    root.mainloop()