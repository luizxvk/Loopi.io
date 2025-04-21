#!/bin/bash

# Ativa o ambiente virtual
source venv/bin/activate

# Exporta variáveis de ambiente pra evitar avisos do Qt e GTK
export QT_QPA_PLATFORM=xcb
export QT_DEBUG_PLUGINS=0
export SDL_AUDIODRIVER=pulseaudio
export XDG_CURRENT_DESKTOP=GNOME

# Executa o programa
python music_player.py
