# habilidades
# data/habilidades.py

# Este dicionário conterá todas as definições de habilidades.
# Cada chave é o nome da habilidade.
# O valor é um dicionário com:
# - 'cooldown_max': Cooldown máximo em turnos.
# - 'tipo': Categoria da habilidade (dano, cura, buff, debuff, dano_cura).
# - 'descricao': Uma breve descrição da habilidade (opcional, mas útil).
# - 'efeito_combate': Uma string que será mapeada para o método de aplicação no CombatSystem.

HABILIDADES_DATA = {
    'Ataque Básico': {
        'cooldown_max': 0,
        'tipo': 'dano',
        'descricao': 'Um ataque físico padrão.',
        'efeito_combate': '_aplicar_ataque_basico'
    },
    'Golpe Poderoso': {
        'cooldown_max': 3,
        'tipo': 'dano',
        'descricao': 'Um golpe forte que causa dano extra.',
        'efeito_combate': '_aplicar_golpe_poderoso'
    },
    'Bola de Fogo': {
        'cooldown_max': 22,
        'tipo': 'dano',
        'descricao': 'Lança uma bola de fogo que causa grande dano mágico.',
        'efeito_combate': '_aplicar_bola_de_fogo'
    },
    'Chuva de Flechas': {
        'cooldown_max': 8,
        'tipo': 'dano',
        'descricao': 'Dispara múltiplas flechas em um único alvo.',
        'efeito_combate': '_aplicar_chuva_de_flechas'
    },
    'Ataque Rápido': {
        'cooldown_max': 2,
        'tipo': 'dano',
        'descricao': 'Um ataque veloz com dano moderado.',
        'efeito_combate': '_aplicar_ataque_rapido'
    },
    'Ataque Furtivo': {
        'cooldown_max': 4,
        'tipo': 'dano',
        'descricao': 'Um ataque surpresa que causa dano massivo.',
        'efeito_combate': '_aplicar_ataque_furtivo'
    },
    'Ataque Giratório': {
        'cooldown_max': 5,
        'tipo': 'dano',
        'descricao': 'Um ataque que atinge o inimigo com um giro poderoso.',
        'efeito_combate': '_aplicar_ataque_giratorio'
    },
    'Golpe Crítico': {
        'cooldown_max': 4,
        'tipo': 'dano',
        'descricao': 'Prepara um golpe com alta chance de acerto crítico.',
        'efeito_combate': '_aplicar_golpe_critico'
    },
    'Ataque Duplo': {
        'cooldown_max': 6,
        'tipo': 'dano',
        'descricao': 'Realiza dois ataques rápidos em sequência.',
        'efeito_combate': '_aplicar_ataque_duplo'
    },
    'Cura Rápida': {
        'cooldown_max': 5,
        'tipo': 'cura',
        'descricao': 'Recupera uma pequena quantidade de vida instantaneamente.',
        'efeito_combate': '_aplicar_cura_rapida'
    },
    'Cura Leve': {
        'cooldown_max': 5,
        'tipo': 'cura',
        'descricao': 'Recupera uma quantidade moderada de vida.',
        'efeito_combate': '_aplicar_cura_leve'
    },
    'Cura Menor': {
        'cooldown_max': 7,
        'tipo': 'cura',
        'descricao': 'Recupera uma pequena quantidade de vida.',
        'efeito_combate': '_aplicar_cura_menor'
    },
    'Foco Preciso': {
        'cooldown_max': 7,
        'tipo': 'buff',
        'descricao': 'Aumenta temporariamente sua precisão.',
        'efeito_combate': '_aplicar_foco_preciso'
    },
    'Pele de Pedra': {
        'cooldown_max': 9,
        'tipo': 'buff',
        'descricao': 'Aumenta temporariamente sua defesa.',
        'efeito_combate': '_aplicar_pele_de_pedra'
    },
    'Escudo Divino': {
        'cooldown_max': 8,
        'tipo': 'buff',
        'descricao': 'Invoca um escudo que aumenta muito sua defesa por um curto período.',
        'efeito_combate': '_aplicar_escudo_divino'
    },
    # Novas Habilidades
    'Investida Brutal': {
        'cooldown_max': 6,
        'tipo': 'dano',
        'descricao': 'Avança contra o inimigo causando dano e com chance de atordoar.',
        'efeito_combate': '_aplicar_investida_brutal'
    },
    'Raio Arcano': {
        'cooldown_max': 10,
        'tipo': 'dano',
        'descricao': 'Dispara um raio de energia arcana no inimigo.',
        'efeito_combate': '_aplicar_raio_arcano'
    },
    'Tiro Múltiplo': {
        'cooldown_max': 7,
        'tipo': 'dano',
        'descricao': 'Atira várias flechas no alvo, cada uma causando dano reduzido.',
        'efeito_combate': '_aplicar_tiro_multiplo'
    },
    'Distração': {
        'cooldown_max': 5,
        'tipo': 'debuff',
        'descricao': 'Reduz temporariamente a precisão do inimigo.',
        'efeito_combate': '_aplicar_distracao'
    },
    'Bênção Divina': {
        'cooldown_max': 10,
        'tipo': 'buff',
        'descricao': 'Cura e aumenta a defesa por alguns turnos.',
        'efeito_combate': '_aplicar_bencao_divina'
    },
    'Drenar Vida': {
        'cooldown_max': 8,
        'tipo': 'dano_cura',
        'descricao': 'Causa dano ao inimigo e recupera parte da vida.',
        'efeito_combate': '_aplicar_drenar_vida'
    },
    'Ataque Venenoso': { # Exemplo de nova habilidade
        'cooldown_max': 4,
        'tipo': 'dano_debuff',
        'descricao': 'Ataque que causa dano e envenena o inimigo por alguns turnos.',
        'efeito_combate': '_aplicar_ataque_venenoso'
    },
    'Grito de Guerra': { # Exemplo de nova habilidade (Guerreiro)
        'cooldown_max': 7,
        'tipo': 'buff',
        'descricao': 'Aumenta o ataque do jogador por alguns turnos.',
        'efeito_combate': '_aplicar_grito_de_guerra'
    },
    'Escudo de Mana': { # Exemplo de nova habilidade (Mago)
        'cooldown_max': 12,
        'tipo': 'buff',
        'descricao': 'Cria um escudo que absorve parte do dano recebido.',
        'efeito_combate': '_aplicar_escudo_de_mana'
    },
    'raio solar': {
        'cooldown_max': 1,
        'tipo': 'dano_cura',
        'descricao': 'Causa dano ao inimigo e recupera parte da vida.',
        'efeito_combate': '_aplicar_raio_solar'

    }
}
