# 🎵 SpotiPlay - Player de Música Estilizado

Um player de música moderno e minimalista desenvolvido com **Python + PyQt6**, inspirado em estética premium como o Apple Music e Cider. O projeto oferece uma interface limpa e intuitiva para reprodução de músicas locais, com suporte a metadados e uma experiência visual elegante.

> ⚠️ **Aviso:** Este projeto ainda está em desenvolvimento e pode conter bugs.

---

## 🛠️ Funcionalidades Técnicas

- 🎧 **Reprodução de Músicas Locais**:
  - Suporte a formatos como `.mp3`, `.wav`, `.ogg`, `.flac`.

- 📑 **Leitura de Metadados**:
  - Extração de capa do álbum, nome da faixa, artista, duração da música.

- 📊 **Barra de Progresso**:
  - Estilizada, com tempo decorrido e restante.

- 🎨 **Interface Estilizada**:
  - Tema escuro translúcido com botões personalizados.
  - Tipografia moderna com a fonte San Francisco.

- 🌎 **Navegação por Gênero**:
  - Botões para gêneros: Dance, Rock, Eletronic, Chill (em desenvolvimento).

- 📹 **Capa do Álbum**:
  - Renderiza automaticamente a imagem extraída dos metadados da faixa.

- 📕 **Estilo Personalizado**:
  - Utiliza arquivos `.qss` para facilitar customizações visuais.

---

## 📄 Estrutura Principal

```
SpotiPlay/
├── assets/
│   ├── background.jpg
│   ├── icons/
│   └── fonts/SanFrancisco/
├── music_player.py
└── style.qss
```

---

## 📅 Requisitos

- Python 3.9 ou superior.
- Bibliotecas:
  - PyQt6
  - pygame
  - mutagen

Instale com:
```bash
pip install -r requirements.txt
```

---

## 📅 Uso

Execute o aplicativo com:
```bash
python music_player.py
```

---

## 💡 Atualizações Futuras

- [ ] Conexão com API de streaming.
- [ ] Integração com letras da música.
- [ ] Equalizador embutido.
- [ ] Seleção de temas (light/dark/dynamic).
- [ ] Gerenciador de playlists locais.
- [ ] Versão responsiva para Android com PySide + Kivy (ideia).

---

## 💼 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar, estudar e modificar.

## 📌 Versão
**Versão Atual:** 0.2.0  
Este projeto está em desenvolvimento contínuo.


