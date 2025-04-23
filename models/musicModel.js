// Simulação de um "banco de dados" com músicas
let musicLibrary = [
    {
      id: 1,
      title: "Love Sunshine & Hysteria",
      artist: "Desconhecido",
      genre: "Chill",
      duration: "03:45"
    },
    {
      id: 2,
      title: "Electric Dreams",
      artist: "Synth Waves",
      genre: "Eletronic",
      duration: "04:20"
    }
  ];
  
  // Exporta funções para acessar o "banco de dados"
  module.exports = {
    getAllMusic: () => musicLibrary,
  
    getMusicById: (id) => musicLibrary.find((music) => music.id === id),
  
    addMusic: (newMusic) => {
      const id = musicLibrary.length + 1;
      const music = { id, ...newMusic };
      musicLibrary.push(music);
      return music;
    },
  
    deleteMusic: (id) => {
      musicLibrary = musicLibrary.filter((music) => music.id !== id);
      return true;
    }
  };
  