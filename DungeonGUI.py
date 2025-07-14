import tkinter as tk
from tkinter import ttk, messagebox
from main import JogoRPG

class RPGInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon da Silva")
        self.root.geometry("1000x700")
        
        # Configuração do estilo
        self.setup_styles()
        
        # Inicializa o jogo
        self.jogo = JogoRPG()
        self.jogo.game_state.log_mensagem = self.log_mensagem
        
        # Cria os widgets
        self.create_widgets()
        
        # Inicia no menu principal
        self.jogo.game_state.set_state("menu_principal")
        self.update_interface()
    
    def setup_styles(self):
        """Configura os estilos visuais da interface"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores base
        bg_color = '#1a1a1a'
        fg_color = 'white'
        button_color = '#333'
        highlight_color = '#444'
        
        # Configurações de estilo
        self.style.configure('.', background=bg_color, foreground=fg_color)
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=fg_color)
        self.style.configure('TButton', background=button_color, foreground=fg_color, 
                           borderwidth=1, focusthickness=3, focuscolor='none')
        self.style.map('TButton', 
                      background=[('active', highlight_color), ('pressed', highlight_color)])
        self.style.configure('TNotebook', background=bg_color)
        self.style.configure('TNotebook.Tab', background=button_color, foreground=fg_color,
                           padding=[10, 5])
        self.style.configure('TLabelframe', background=bg_color, foreground=fg_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook para diferentes telas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Cria as páginas
        self.create_menu_principal_page()
        self.create_exploracao_page()
        self.create_combate_page()
        self.create_menu_page()
        self.create_loja_page()
        self.create_vitoria_page()
        
        # Barra de status
        self.create_status_bar()
        
        # Histórico de mensagens
        self.create_historico_frame()
    
    def create_menu_principal_page(self):
        """Cria a página do menu principal"""
        self.menu_principal_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.menu_principal_frame, text="Menu Principal", state='hidden')
        
        # Título do jogo
        title_frame = ttk.Frame(self.menu_principal_frame)
        title_frame.pack(pady=50)
        
        ttk.Label(title_frame, text="Dungeon da Silva", font=('Arial', 24, 'bold')).pack()
        ttk.Label(title_frame, text="Um RPG de Dungeon por Turnos", font=('Arial', 12)).pack(pady=10)
        
        # Botões do menu
        buttons_frame = ttk.Frame(self.menu_principal_frame)
        buttons_frame.pack(pady=30, padx=100, fill=tk.X)
        
        ttk.Button(buttons_frame, text="Novo Jogo", command=self.iniciar_novo_jogo).pack(pady=10, fill=tk.X)
        ttk.Button(buttons_frame, text="Carregar Jogo", command=self.carregar_jogo).pack(pady=10, fill=tk.X)
        ttk.Button(buttons_frame, text="Sair", command=self.root.quit).pack(pady=10, fill=tk.X)
    
    def create_exploracao_page(self):
        """Cria a página de exploração"""
        self.exploracao_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.exploracao_frame, text="Exploração", state='hidden')
        
        # Frame superior com informações do jogador
        self.player_info_frame = ttk.LabelFrame(self.exploracao_frame, text="Jogador")
        self.player_info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.player_info_label = ttk.Label(self.player_info_frame, text="", font=('Arial', 10))
        self.player_info_label.pack()
        
        # Frame do mapa
        self.mapa_frame = ttk.LabelFrame(self.exploracao_frame, text="Mapa")
        self.mapa_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.mapa_canvas = tk.Canvas(self.mapa_frame, bg='black', highlightthickness=0)
        self.mapa_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame de controles
        self.controls_frame = ttk.Frame(self.exploracao_frame)
        self.controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.controls_frame, text="Menu (E)", command=self.abrir_menu).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.controls_frame, text="Loja (L)", command=self.abrir_loja).pack(side=tk.LEFT, padx=5)
        
        # Frame de movimento
        self.movement_frame = ttk.Frame(self.exploracao_frame)
        self.movement_frame.pack(pady=5)
        
        ttk.Button(self.movement_frame, text="↑", width=3, 
                  command=lambda: self.mover_jogador('cima')).grid(row=0, column=1, padx=3, pady=3)
        ttk.Button(self.movement_frame, text="←", width=3, 
                  command=lambda: self.mover_jogador('esquerda')).grid(row=1, column=0, padx=3, pady=3)
        ttk.Button(self.movement_frame, text="↓", width=3, 
                  command=lambda: self.mover_jogador('baixo')).grid(row=1, column=1, padx=3, pady=3)
        ttk.Button(self.movement_frame, text="→", width=3, 
                  command=lambda: self.mover_jogador('direita')).grid(row=1, column=2, padx=3, pady=3)
    
    def create_combate_page(self):
        """Cria a página de combate"""
        self.combate_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.combate_frame, text="Combate", state='hidden')
        
        # Frame de informações do combate
        self.combat_info_frame = ttk.LabelFrame(self.combate_frame, text="Combate")
        self.combat_info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame dos sprites
        self.combat_sprites_frame = ttk.Frame(self.combat_info_frame)
        self.combat_sprites_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Jogador
        self.player_combat_frame = ttk.Frame(self.combat_sprites_frame)
        self.player_combat_frame.pack(side=tk.LEFT, expand=True)
        
        ttk.Label(self.player_combat_frame, text="Jogador", font=('Arial', 12)).pack()
        self.player_sprite_label = ttk.Label(self.player_combat_frame, 
                                           text="  O  \n /|\\ \n / \\ ", 
                                           font=('Courier', 14))
        self.player_sprite_label.pack(pady=10)
        
        # VS
        ttk.Label(self.combat_sprites_frame, text="VS", font=('Arial', 16)).pack(side=tk.LEFT, padx=20)
        
        # Inimigo
        self.enemy_combat_frame = ttk.Frame(self.combat_sprites_frame)
        self.enemy_combat_frame.pack(side=tk.LEFT, expand=True)
        
        self.enemy_name_label = ttk.Label(self.enemy_combat_frame, text="Inimigo", font=('Arial', 12))
        self.enemy_name_label.pack()
        self.enemy_sprite_label = ttk.Label(self.enemy_combat_frame, 
                                          text="  ?  \n /|\\ \n | | ", 
                                          font=('Courier', 14))
        self.enemy_sprite_label.pack(pady=10)
        
        # Barras de vida
        self.health_bars_frame = ttk.Frame(self.combat_info_frame)
        self.health_bars_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.player_health_label = ttk.Label(self.health_bars_frame, text="Jogador: 100/100")
        self.player_health_label.pack()
        
        self.enemy_health_label = ttk.Label(self.health_bars_frame, text="Inimigo: 100/100")
        self.enemy_health_label.pack()
        
        # Frame de ações
        self.actions_frame = ttk.Frame(self.combate_frame)
        self.actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.actions_frame, text="Atacar (1)", 
                  command=lambda: self.combate_acao('atacar')).pack(side=tk.LEFT, padx=5, expand=True)
        ttk.Button(self.actions_frame, text="Habilidade (2)", 
                  command=self.abrir_menu_habilidades).pack(side=tk.LEFT, padx=5, expand=True)
        ttk.Button(self.actions_frame, text="Item (3)", 
                  command=self.abrir_menu_itens).pack(side=tk.LEFT, padx=5, expand=True)
        ttk.Button(self.actions_frame, text="Fugir (4)", 
                  command=lambda: self.combate_acao('fugir')).pack(side=tk.LEFT, padx=5, expand=True)
    
    def create_menu_page(self):
        """Cria a página do menu do jogador"""
        self.menu_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.menu_frame, text="Menu", state='hidden')
        
        # Informações do jogador
        self.menu_player_info = ttk.Label(self.menu_frame, text="", font=('Arial', 10))
        self.menu_player_info.pack(pady=10, padx=10, anchor=tk.W)
        
        # Frame com abas para diferentes seções
        self.menu_notebook = ttk.Notebook(self.menu_frame)
        self.menu_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba de Habilidades
        self.habilidades_frame = ttk.Frame(self.menu_notebook)
        self.menu_notebook.add(self.habilidades_frame, text="Habilidades")
        
        self.habilidades_text = tk.Text(self.habilidades_frame, height=10, bg='#1a1a1a', fg='white',
                                      wrap=tk.WORD, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.habilidades_frame, command=self.habilidades_text.yview)
        self.habilidades_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.habilidades_text.pack(fill=tk.BOTH, expand=True)
        self.habilidades_text.config(state=tk.DISABLED)
        
        # Aba de Inventário
        self.inventario_frame = ttk.Frame(self.menu_notebook)
        self.menu_notebook.add(self.inventario_frame, text="Inventário")
        
        self.inventario_text = tk.Text(self.inventario_frame, height=10, bg='#1a1a1a', fg='white',
                                      wrap=tk.WORD, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.inventario_frame, command=self.inventario_text.yview)
        self.inventario_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.inventario_text.pack(fill=tk.BOTH, expand=True)
        self.inventario_text.config(state=tk.DISABLED)
        
        # Aba de Efeitos Ativos
        self.efeitos_frame = ttk.Frame(self.menu_notebook)
        self.menu_notebook.add(self.efeitos_frame, text="Efeitos Ativos")
        
        self.efeitos_text = tk.Text(self.efeitos_frame, height=5, bg='#1a1a1a', fg='white',
                                   wrap=tk.WORD, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.efeitos_frame, command=self.efeitos_text.yview)
        self.efeitos_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.efeitos_text.pack(fill=tk.BOTH, expand=True)
        self.efeitos_text.config(state=tk.DISABLED)
        
        # Frame de opções
        self.menu_options_frame = ttk.Frame(self.menu_frame)
        self.menu_options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.menu_options_frame, text="Usar Poção de Vida (1)", 
                  command=lambda: self.usar_item_menu('Poção de Vida')).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(self.menu_options_frame, text="Usar Poção de Ataque (2)", 
                  command=lambda: self.usar_item_menu('Poção de Ataque')).pack(side=tk.LEFT, padx=2, expand=True)
        
        # Segunda linha de botões
        self.menu_options_frame2 = ttk.Frame(self.menu_frame)
        self.menu_options_frame2.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.menu_options_frame2, text="Salvar Jogo (3)", 
                  command=self.salvar_jogo).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(self.menu_options_frame2, text="Menu Principal (4)", 
                  command=self.voltar_menu_principal).pack(side=tk.LEFT, padx=2, expand=True)
        
        if not self.jogo.player.classe:
            ttk.Button(self.menu_options_frame2, text="Escolher Classe (5)", 
                      command=self.escolher_classe).pack(side=tk.LEFT, padx=2, expand=True)
        
        ttk.Button(self.menu_options_frame2, text="Voltar (0)", 
                  command=self.voltar_exploracao).pack(side=tk.LEFT, padx=2, expand=True)
    
    def create_loja_page(self):
        """Cria a página da loja"""
        self.loja_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.loja_frame, text="Loja", state='hidden')
        
        # Informações do jogador
        self.loja_player_info = ttk.Label(self.loja_frame, text="", font=('Arial', 10))
        self.loja_player_info.pack(pady=10)
        
        # Itens da loja
        self.loja_itens_frame = ttk.LabelFrame(self.loja_frame, text="Itens à Venda")
        self.loja_itens_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.loja_itens_text = tk.Text(self.loja_itens_frame, height=10, bg='#1a1a1a', fg='white',
                                      wrap=tk.WORD, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.loja_itens_frame, command=self.loja_itens_text.yview)
        self.loja_itens_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.loja_itens_text.pack(fill=tk.BOTH, expand=True)
        self.loja_itens_text.config(state=tk.DISABLED)
        
        # Frame de controles
        self.loja_controls_frame = ttk.Frame(self.loja_frame)
        self.loja_controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.loja_controls_frame, text="Digite o número do item e pressione Enter:").pack(side=tk.LEFT)
        
        self.loja_entry = ttk.Entry(self.loja_controls_frame, width=5)
        self.loja_entry.pack(side=tk.LEFT, padx=5)
        self.loja_entry.bind('<Return>', self.comprar_item_loja)
        
        ttk.Button(self.loja_controls_frame, text="Voltar (0)", 
                  command=self.voltar_exploracao).pack(side=tk.RIGHT, padx=5)
    
    def create_vitoria_page(self):
        """Cria a página de vitória"""
        self.vitoria_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.vitoria_frame, text="Vitória", state='hidden')
        
        # Mensagem de vitória
        self.vitoria_label = ttk.Label(self.vitoria_frame, text="", font=('Arial', 16, 'bold'))
        self.vitoria_label.pack(pady=20)
        
        # Recompensas
        self.recompensas_frame = ttk.LabelFrame(self.vitoria_frame, text="Recompensas")
        self.recompensas_frame.pack(fill=tk.X, padx=50, pady=10)
        
        self.recompensas_text = tk.Text(self.recompensas_frame, height=5, bg='#1a1a1a', fg='white',
                                       wrap=tk.WORD, padx=5, pady=5)
        self.recompensas_text.pack(fill=tk.BOTH, expand=True)
        self.recompensas_text.config(state=tk.DISABLED)
        
        # Botão para continuar
        ttk.Button(self.vitoria_frame, text="Continuar Explorando", 
                  command=self.voltar_exploracao).pack(pady=20)
    
    def create_status_bar(self):
        """Cria a barra de status na parte inferior"""
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_bar.pack(fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Pronto para jogar!", 
                                    font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT, padx=5)
    
    def create_historico_frame(self):
        """Cria o frame de histórico de mensagens"""
        self.historico_frame = ttk.LabelFrame(self.main_frame, text="Histórico")
        self.historico_frame.pack(fill=tk.BOTH, expand=True)
        
        self.historico_text = tk.Text(self.historico_frame, height=5, bg='#1a1a1a', fg='white',
                                     wrap=tk.WORD, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.historico_frame, command=self.historico_text.yview)
        self.historico_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.historico_text.pack(fill=tk.BOTH, expand=True)
        self.historico_text.config(state=tk.DISABLED)
    
    # Métodos de atualização da interface
    def update_interface(self):
        """Atualiza toda a interface com base no estado atual do jogo"""
        current_state = self.jogo.game_state.get_state()
        
        # Esconder todas as páginas primeiro
        for tab in self.notebook.tabs():
            self.notebook.tab(tab, state='hidden')
        
        # Mostrar a página correta
        if current_state == "menu_principal":
            self.notebook.tab(self.menu_principal_frame, state='normal')
            self.notebook.select(self.menu_principal_frame)
        elif current_state == "explorando":
            self.update_exploracao_page()
            self.notebook.tab(self.exploracao_frame, state='normal')
            self.notebook.select(self.exploracao_frame)
        elif current_state == "combate":
            self.update_combate_page()
            self.notebook.tab(self.combate_frame, state='normal')
            self.notebook.select(self.combate_frame)
        elif current_state == "menu":
            self.update_menu_page()
            self.notebook.tab(self.menu_frame, state='normal')
            self.notebook.select(self.menu_frame)
        elif current_state == "loja":
            self.update_loja_page()
            self.notebook.tab(self.loja_frame, state='normal')
            self.notebook.select(self.loja_frame)
        elif current_state == "vitoria":
            self.update_vitoria_page()
            self.notebook.tab(self.vitoria_frame, state='normal')
            self.notebook.select(self.vitoria_frame)
        
        # Atualizar histórico de mensagens
        self.update_historico()
        
        # Atualizar barra de status
        self.update_status_bar()
    
    def update_exploracao_page(self):
        """Atualiza a página de exploração"""
        player = self.jogo.player
        dungeon_level = self.jogo.game_map.dungeon_nivel
        
        # Atualizar informações do jogador
        info_text = (f"=== Dungeon Nível {dungeon_level} ===\n"
                    f"Vida: {player.vida}/{player.vida_max} | Nível: {player.nivel} | XP: {player.xp}/{player.nivel*100}\n"
                    f"Ouro: {player.ouro} | Ataque: {player.ataque} | Defesa: {player.defesa}\n"
                    f"Precisão: {player.precisao}% | Esquiva: {player.esquiva}%")
        self.player_info_label.config(text=info_text)
        
        # Atualizar mapa
        self.mapa_canvas.delete("all")
        cell_size = 20
        raio_visao = 10
        
        x_min = max(0, player.x - raio_visao)
        x_max = min(self.jogo.game_map.largura, player.x + raio_visao + 1)
        y_min = max(0, player.y - raio_visao//2)
        y_max = min(self.jogo.game_map.altura, player.y + raio_visao//2 + 1)
        
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                canvas_x = (x - x_min) * cell_size
                canvas_y = (y - y_min) * cell_size
                
                if x == player.x and y == player.y:
                    # Desenhar jogador
                    self.mapa_canvas.create_rectangle(canvas_x, canvas_y, 
                                                     canvas_x + cell_size, canvas_y + cell_size, 
                                                     fill='blue', outline='')
                    self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                text="@", fill='white', font=('Courier', 12))
                else:
                    celula = self.jogo.game_map.mapa[y][x]
                    inimigo, item, portal, npc = self.jogo.game_map.get_entities_at_position(x, y)
                    
                    if celula == '#':
                        # Parede
                        self.mapa_canvas.create_rectangle(canvas_x, canvas_y, 
                                                         canvas_x + cell_size, canvas_y + cell_size, 
                                                         fill='#555', outline='')
                    else:
                        # Chão
                        self.mapa_canvas.create_rectangle(canvas_x, canvas_y, 
                                                         canvas_x + cell_size, canvas_y + cell_size, 
                                                         fill='#222', outline='')
                        
                        if inimigo:
                            if inimigo.chefao:
                                # Chefão
                                self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                            text="D", fill='red', 
                                                            font=('Courier', 12, 'bold'))
                            elif inimigo.is_miniboss:
                                # Mini-chefão
                                self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                            text="B", fill='orange', 
                                                            font=('Courier', 12, 'bold'))
                            else:
                                # Inimigo normal
                                self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                            text="E", fill='red', 
                                                            font=('Courier', 12))
                        elif item:
                            # Item
                            self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                        text="i", fill='green', 
                                                        font=('Courier', 12))
                        elif portal:
                            # Portal
                            self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                        text="O", fill='yellow', 
                                                        font=('Courier', 12))
                        elif npc:
                            # NPC
                            self.mapa_canvas.create_text(canvas_x + cell_size//2, canvas_y + cell_size//2, 
                                                        text="M", fill='cyan', 
                                                        font=('Courier', 12))
    
    def update_combate_page(self):
        """Atualiza a página de combate"""
        inimigo = self.jogo.combat_system.current_enemy
        if not inimigo:
            return
        
        player = self.jogo.player
        
        # Atualizar nome do inimigo
        self.enemy_name_label.config(text=inimigo.tipo)
        
        # Atualizar sprites
        enemy_sprites = {
            'Goblin': "  G  \n /|\\ \n | | ",
            'Orc': " _O_ \n| o |\n|___|",
            'Fantasma de Dragão': " .^. \n/O O\\\n > < ",
            'Morto-Vivo': " x_x \n |\\| \n / \\ ",
            'Slime': "     \n ~~~ \n(o_o)",
            'Ogro': "  _  \n / \\ \n| O |",
            'Lich': "  ^  \n /_\\ \n | | "
        }
        
        self.enemy_sprite_label.config(text=enemy_sprites.get(inimigo.tipo, "  ?  \n /|\\ \n | | "))
        
        # Atualizar barras de vida
        player_health = f"Jogador: [{'#' * int(10 * player.vida/player.vida_max)}{' ' * (10 - int(10 * player.vida/player.vida_max))}] {player.vida}/{player.vida_max}"
        enemy_health = f"{inimigo.tipo}: [{'#' * int(10 * inimigo.vida/inimigo.vida_max)}{' ' * (10 - int(10 * inimigo.vida/inimigo.vida_max))}] {inimigo.vida}/{inimigo.vida_max}"
        
        self.player_health_label.config(text=player_health)
        self.enemy_health_label.config(text=enemy_health)
    
    def update_menu_page(self):
        """Atualiza a página do menu"""
        player = self.jogo.player
        
        # Informações do jogador
        info_text = (f"Classe: {player.classe or 'Nenhuma'}\n"
                    f"Nível: {player.nivel} | XP: {player.xp}/{player.nivel*100}\n"
                    f"Vida: {player.vida}/{player.vida_max} | Ouro: {player.ouro}\n"
                    f"Ataque: {player.ataque} | Defesa: {player.defesa}\n"
                    f"Precisão: {player.precisao}% | Esquiva: {player.esquiva}%")
        self.menu_player_info.config(text=info_text)
        
        # Habilidades
        self.habilidades_text.config(state=tk.NORMAL)
        self.habilidades_text.delete(1.0, tk.END)
        
        if not player.habilidades:
            self.habilidades_text.insert(tk.END, "- Nenhuma habilidade aprendida.")
        else:
            for nome_hab, dados_hab in player.habilidades.items():
                cooldown_info = f" (CD: {dados_hab['cooldown']}/{dados_hab['cooldown_max']})" if dados_hab['cooldown_max'] > 0 else ""
                self.habilidades_text.insert(tk.END, f"- {nome_hab}{cooldown_info}\n")
        self.habilidades_text.config(state=tk.DISABLED)
        
        # Inventário
        self.inventario_text.config(state=tk.NORMAL)
        self.inventario_text.delete(1.0, tk.END)
        
        if not player.inventario:
            self.inventario_text.insert(tk.END, "- Vazio")
        else:
            itens_no_inventario = {k: v for k, v in player.inventario.items() if v > 0}
            if not itens_no_inventario:
                self.inventario_text.insert(tk.END, "- Vazio")
            else:
                for item, qtd in itens_no_inventario.items():
                    self.inventario_text.insert(tk.END, f"- {item}: {qtd}\n")
        self.inventario_text.config(state=tk.DISABLED)
        
        # Efeitos ativos
        self.efeitos_text.config(state=tk.NORMAL)
        self.efeitos_text.delete(1.0, tk.END)
        
        if not player.efeitos_ativos:
            self.efeitos_text.insert(tk.END, "- Nenhum efeito ativo.")
        else:
            for efeito_nome, dados_efeito in player.efeitos_ativos.items():
                self.efeitos_text.insert(tk.END, f"- {efeito_nome} (Turnos restantes: {dados_efeito['turnos_restantes']})\n")
        self.efeitos_text.config(state=tk.DISABLED)
    
    def update_loja_page(self):
        """Atualiza a página da loja"""
        player = self.jogo.player
        loja = self.jogo.shop_system
        
        # Informações do jogador
        self.loja_player_info.config(text=f"Ouro: {player.ouro}")
        
        # Itens da loja
        self.loja_itens_text.config(state=tk.NORMAL)
        self.loja_itens_text.delete(1.0, tk.END)
        
        for idx, item in enumerate(loja.loja_itens, 1):
            self.loja_itens_text.insert(tk.END, f"{idx}. {item.nome} - {item.preco} ouro\n")
        
        self.loja_itens_text.config(state=tk.DISABLED)
        self.loja_entry.delete(0, tk.END)
    
    def update_vitoria_page(self):
        """Atualiza a página de vitória"""
        inimigo = self.jogo.combat_system.current_enemy
        
        self.vitoria_label.config(text=f"VITÓRIA EPICA!\nVocê derrotou o chefão da dungeon nível {self.jogo.game_map.dungeon_nivel}!")
        
        self.recompensas_text.config(state=tk.NORMAL)
        self.recompensas_text.delete(1.0, tk.END)
        
        if inimigo:
            self.recompensas_text.insert(tk.END, f"- {inimigo.xp} XP\n")
            self.recompensas_text.insert(tk.END, f"- {inimigo.ouro} de ouro\n")
        else:
            self.recompensas_text.insert(tk.END, "- Recompensas já coletadas ou inimigo não definido.")
        
        self.recompensas_text.config(state=tk.DISABLED)
    
    def update_historico(self):
        """Atualiza o histórico de mensagens"""
        self.historico_text.config(state=tk.NORMAL)
        self.historico_text.delete(1.0, tk.END)
        
        for msg in self.jogo.game_state.get_historico()[-5:]:
            self.historico_text.insert(tk.END, f"- {msg}\n")
        
        self.historico_text.config(state=tk.DISABLED)
        self.historico_text.see(tk.END)
    
    def update_status_bar(self):
        """Atualiza a barra de status"""
        current_state = self.jogo.game_state.get_state()
        
        if current_state == "explorando":
            self.status_label.config(text="WASD: Mover | E: Menu | Q: Sair | L: Loja (perto de mercador)")
        elif current_state == "combate":
            self.status_label.config(text="1: Atacar | 2: Habilidade | 3: Item | 4: Fugir")
        elif current_state == "menu":
            self.status_label.config(text="1: Poção Vida | 2: Poção Ataque | 3: Salvar | 4: Menu Principal | 5: Escolher Classe | 0: Voltar")
        elif current_state == "loja":
            self.status_label.config(text="Digite o número do item e pressione Enter | 0: Voltar")
        elif current_state == "vitoria":
            self.status_label.config(text="Pressione o botão para continuar explorando")
        else:
            self.status_label.config(text="Pronto para jogar!")
    
    def log_mensagem(self, msg):
        """Adiciona uma mensagem ao histórico"""
        self.jogo.game_state.historico.append(msg)
        if len(self.jogo.game_state.historico) > 5:
            self.jogo.game_state.historico.pop(0)
        self.update_historico()
    
    # Métodos de controle do jogo
    def iniciar_novo_jogo(self):
        """Inicia um novo jogo"""
        self.jogo.iniciar_novo_jogo()
        self.update_interface()
    
    def carregar_jogo(self):
        """Carrega um jogo salvo"""
        jogo_carregado = self.jogo.Menu.carregar_jogo()
        if jogo_carregado:
            self.jogo.carregar_jogo_salvo(jogo_carregado)
            self.update_interface()
        else:
            messagebox.showerror("Erro", "Falha ao carregar o jogo.")
    
    def salvar_jogo(self):
        """Salva o jogo atual"""
        self.jogo.Menu.salvar_jogo(self.jogo)
        self.log_mensagem("Jogo salvo com sucesso!")
    
    def mover_jogador(self, direcao):
        """Move o jogador na direção especificada"""
        if self.jogo.game_state.get_state() != "explorando":
            return
        
        self.jogo.mover_jogador(direcao)
        self.update_interface()
    
    def abrir_menu(self):
        """Abre o menu do jogador"""
        self.jogo.game_state.set_state("menu")
        self.update_interface()
    
    def abrir_loja(self):
        """Abre a loja se o jogador estiver perto de um mercador"""
        mercador = next((n for n in self.jogo.game_map.npcs if n.tipo == 'Mercador'), None)
        if mercador and abs(self.jogo.player.x - mercador.x) <= 1 and abs(self.jogo.player.y - mercador.y) <= 1:
            self.jogo.game_state.set_state("loja")
            self.update_interface()
        else:
            self.log_mensagem("Nenhum mercador por perto!")
    
    def voltar_exploracao(self):
        """Volta para a tela de exploração"""
        self.jogo.game_state.set_state("explorando")
        self.update_interface()
    
    def voltar_menu_principal(self):
        """Volta para o menu principal"""
        self.jogo.game_state.set_state("menu_principal")
        self.update_interface()
    
    def combate_acao(self, acao):
        """Executa uma ação de combate"""
        new_state = self.jogo.combat_system.resolver_combate_acao(acao)
        self.jogo.game_state.set_state(new_state)
        self.update_interface()
    
    def abrir_menu_habilidades(self):
        """Abre o menu de seleção de habilidades durante o combate"""
        habilidades_nomes = list(self.jogo.player.habilidades.keys())
        
        if not habilidades_nomes:
            self.log_mensagem("Você não tem habilidades!")
            return
        
        # Criar janela de seleção de habilidades
        habilidade_window = tk.Toplevel(self.root)
        habilidade_window.title("Selecionar Habilidade")
        habilidade_window.geometry("400x300")
        
        ttk.Label(habilidade_window, text="Selecione uma habilidade:").pack(pady=10)
        
        habilidades_listbox = tk.Listbox(habilidade_window, height=10, bg='#1a1a1a', fg='white',
                                       selectbackground='#333', selectforeground='white')
        scrollbar = ttk.Scrollbar(habilidade_window, command=habilidades_listbox.yview)
        habilidades_listbox.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        habilidades_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for idx, nome_hab in enumerate(habilidades_nomes, 1):
            dados_hab = self.jogo.player.habilidades[nome_hab]
            cooldown_info = f" (CD: {dados_hab['cooldown']}/{dados_hab['cooldown_max']})" if dados_hab['cooldown_max'] > 0 else ""
            habilidades_listbox.insert(tk.END, f"{idx}. {nome_hab}{cooldown_info}")
        
        def usar_habilidade():
            selecao = habilidades_listbox.curselection()
            if selecao:
                habilidade_selecionada_nome = habilidades_nomes[selecao[0]]
                
                if self.jogo.player.pode_usar_habilidade(habilidade_selecionada_nome):
                    new_state = self.jogo.combat_system.aplicar_habilidade(habilidade_selecionada_nome)
                    if new_state == "combate" or new_state == "explorando" or new_state == "vitoria":
                        self.jogo.player.usar_habilidade(habilidade_selecionada_nome)
                    self.jogo.game_state.set_state(new_state)
                    habilidade_window.destroy()
                    self.update_interface()
                else:
                    messagebox.showwarning("Cooldown", 
                                         f"{habilidade_selecionada_nome} está em cooldown! "
                                         f"({self.jogo.player.habilidades[habilidade_selecionada_nome]['cooldown']} turnos restantes)")
        
        buttons_frame = ttk.Frame(habilidade_window)
        buttons_frame.pack(pady=5)
        
        ttk.Button(buttons_frame, text="Usar", command=usar_habilidade).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=habilidade_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focar na janela de habilidades
        habilidade_window.focus_set()
        habilidade_window.grab_set()
    
    def abrir_menu_itens(self):
        """Abre o menu de seleção de itens durante o combate"""
        itens_disponiveis = [item for item, qtd in self.jogo.player.inventario.items() if qtd > 0]
        
        if not itens_disponiveis:
            self.log_mensagem("Você não tem itens para usar!")
            return
        
        # Criar janela de seleção de itens
        item_window = tk.Toplevel(self.root)
        item_window.title("Selecionar Item")
        item_window.geometry("400x300")
        
        ttk.Label(item_window, text="Selecione um item:").pack(pady=10)
        
        itens_listbox = tk.Listbox(item_window, height=10, bg='#1a1a1a', fg='white',
                                  selectbackground='#333', selectforeground='white')
        scrollbar = ttk.Scrollbar(item_window, command=itens_listbox.yview)
        itens_listbox.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        itens_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for idx, item in enumerate(itens_disponiveis, 1):
            itens_listbox.insert(tk.END, f"{idx}. {item} ({self.jogo.player.inventario[item]})")
        
        def usar_item():
            selecao = itens_listbox.curselection()
            if selecao:
                item_selecionado = itens_disponiveis[selecao[0]]
                new_state = self.jogo.combat_system.usar_item_combate(item_selecionado)
                self.jogo.game_state.set_state(new_state)
                item_window.destroy()
                self.update_interface()
        
        buttons_frame = ttk.Frame(item_window)
        buttons_frame.pack(pady=5)
        
        ttk.Button(buttons_frame, text="Usar", command=usar_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=item_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focar na janela de itens
        item_window.focus_set()
        item_window.grab_set()
    
    def comprar_item_loja(self, event=None):
        """Compra um item da loja baseado na entrada do usuário"""
        try:
            item_idx = int(self.loja_entry.get()) - 1
            if 0 <= item_idx < len(self.jogo.shop_system.loja_itens):
                self.jogo.shop_system.comprar_item(item_idx)
                self.update_loja_page()
            else:
                messagebox.showwarning("Item inválido", "Digite um número de item válido!")
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Digite apenas números!")
    
    def usar_item_menu(self, item_nome):
        """Usa um item a partir do menu"""
        self.jogo.player.usar_item(item_nome, self.log_mensagem)
        self.update_interface()
    
    def escolher_classe(self):
        """Abre a janela de seleção de classe"""
        # Criar janela de seleção de classe
        classe_window = tk.Toplevel(self.root)
        classe_window.title("Escolher Classe")
        classe_window.geometry("500x400")
        
        ttk.Label(classe_window, text="Escolha sua classe:", font=('Arial', 14)).pack(pady=10)
        
        # Frame para os botões de classe
        classes_frame = ttk.Frame(classe_window)
        classes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def selecionar_classe(classe):
            if classe == 'Guerreiro':
                self.jogo.player.classe = 'Guerreiro'
                self.jogo.player.vida_max += 10
                self.jogo.player.vida += 10
                self.jogo.player.ataque += 5
                self.jogo.player.precisao += 5
                self.jogo.player._aprender_habilidade('Golpe Poderoso', self.log_mensagem)
                self.log_mensagem("Você agora é um Guerreiro!")
            elif classe == 'Mago':
                self.jogo.player.classe = 'Mago'
                self.jogo.player.ataque += 5
                self.jogo.player.defesa += 1
                self.jogo.player.precisao += 5
                self.jogo.player._aprender_habilidade('Bola de Fogo', self.log_mensagem)
                self.log_mensagem("Você agora é um Mago!")
            elif classe == 'Arqueiro':
                self.jogo.player.classe = 'Arqueiro'
                self.jogo.player.ataque += 3
                self.jogo.player.defesa += 1
                self.jogo.player.precisao += 10
                self.jogo.player.esquiva += 5
                self.jogo.player._aprender_habilidade('Chuva de Flechas', self.log_mensagem)
                self.log_mensagem("Você agora é um Arqueiro!")
            elif classe == 'Ladrão':
                self.jogo.player.classe = 'Ladrão'
                self.jogo.player.ataque += 5
                self.jogo.player.esquiva += 10
                self.jogo.player.precisao += 5
                self.jogo.player._aprender_habilidade('Ataque Rápido', self.log_mensagem)
                self.log_mensagem("Você agora é um Ladrão!")
            elif classe == 'Clérigo':
                self.jogo.player.classe = 'Clérigo'
                self.jogo.player.vida_max += 20
                self.jogo.player.vida += 20
                self.jogo.player.defesa += 2
                self.jogo.player.precisao += 5
                self.jogo.player._aprender_habilidade('Cura Leve', self.log_mensagem)
                self.log_mensagem("Você agora é um Clérigo!")
            
            classe_window.destroy()
            self.update_interface()
        
        # Botões para cada classe
        ttk.Button(classes_frame, text="Guerreiro\n+10 Vida, +5 Ataque, +5 Precisão", 
                  command=lambda: selecionar_classe('Guerreiro')).pack(fill=tk.X, pady=5)
        ttk.Button(classes_frame, text="Mago\n+5 Ataque, +1 Defesa, +5 Precisão", 
                  command=lambda: selecionar_classe('Mago')).pack(fill=tk.X, pady=5)
        ttk.Button(classes_frame, text="Arqueiro\n+3 Ataque, +1 Defesa, +10 Precisão, +5 Esquiva", 
                  command=lambda: selecionar_classe('Arqueiro')).pack(fill=tk.X, pady=5)
        ttk.Button(classes_frame, text="Ladrão\n+5 Ataque, +10 Esquiva, +5 Precisão", 
                  command=lambda: selecionar_classe('Ladrão')).pack(fill=tk.X, pady=5)
        ttk.Button(classes_frame, text="Clérigo\n+20 Vida, +2 Defesa, +5 Precisão", 
                  command=lambda: selecionar_classe('Clérigo')).pack(fill=tk.X, pady=5)
        
        # Focar na janela de seleção de classe
        classe_window.focus_set()
        classe_window.grab_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = RPGInterface(root)
    root.mainloop()