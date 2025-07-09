import pickle
import os

class Menu:
    def mostrar_logo(self):
        print(r"""
             []  ,----.___   
           __||_/___      '. 
          / O||    /|       )
         /   ""   / /   =._/ 
        /________/ /         
        |________|/""")

    def mostrar_opcoes_principais(self):
        # Este método não será mais chamado diretamente pelo main.py,
        # mas sim o _mostrar_menu_principal() dentro de JogoRPG
        print("\n=== MENU PRINCIPAL ===")
        print("1. Começar Novo Jogo")
        print("2. Carregar Jogo")
        print("3. Sair")
        return input("Escolha uma opção: ")

    def mostrar_menu_jogo(self, player):
        # Este método também não será mais chamado diretamente,
        # pois _mostrar_menu() em JogoRPG o substitui.
        print("\n=== MENU DO JOGO ===")
        print(f"Jogador: {player.classe} (Nv. {player.nivel})")
        print("1. Continuar")
        print("2. Salvar Jogo")
        print("3. Voltar ao Menu Principal")
        return input("Escolha uma opção: ")
    
    @staticmethod
    def salvar_jogo(jogo, filename='savegame.dat'):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(jogo, file)
            print("Jogo salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar: {e}")

    @staticmethod
    def carregar_jogo(filename='savegame.dat'):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            print("Arquivo de save não encontrado!")
        except Exception as e:
            print(f"Erro ao carregar: {e}")
        return None
