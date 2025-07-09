from time import sleep

class Narrative:
    @staticmethod
    def mostrar_introducao():
        print("\n" * 5)
        Narrative.mostrar_texto_lento("Neste mundo...", velocidade=0.1)
        print("\n")
        sleep(1)
        Narrative.mostrar_texto_lento(r"""~         ~~          __        
       _T      .,,.    ~--~ ^^  
 ^^   // \                    ~ 
      ][O]    ^^      ,-~ ~     
   /''-I_I         _II____      
__/_  /   \ ______/ ''   /'\_,__
  | II--'''' \,--:--..,_/,.-{ },
; '/__\,.--';|   |[] .-.| O{ _ }
:' |  | []  -|   ''--:.;[,.'\,/ 
'  |[]|,.--'' '',   ''-,.    |  
  ..    ..-''    ;       ''. '  


""", velocidade=0.009)
        sleep(1)
        
        dialogo_intro = [
            
            "\nQuem é você?...\n"
        ]
        
        for linha in dialogo_intro:
            Narrative.mostrar_texto_lento(linha)
            sleep(0.8)
        
        input("\nPressione Enter para continuar...")
    
    @staticmethod
    def mostrar_dialogo(npc, mensagens):
        print(f"\n=== {npc.upper()} ===")
        for msg in mensagens:
            Narrative.mostrar_texto_lento(msg)
            sleep(0.5)
        input("\n[Pressione Enter para continuar]")
    
    @staticmethod
    def mostrar_texto_lento(texto, velocidade=0.05):
        for char in texto:
            print(char, end='', flush=True)
            sleep(velocidade)
        print()