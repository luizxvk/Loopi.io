const musicModel = require("../models/musicModel");

exports.getAllMusic = (req, res) => {
  const musics = musicModel.getAllMusic();
  res.json(musics);
};

exports.getMusicById = (req, res) => {
  const id = parseInt(req.params.id);
  const music = musicModel.getMusicById(id);
  if (music) {
    res.json(music);
  } else {
    res.status(404).json({ message: "Música não encontrada" });
  }
};

exports.addMusic = (req, res) => {
  const { title, artist, genre, duration } = req.body;

  if (!title || !artist || !genre || !duration) {
    return res.status(400).json({ error: "Todos os campos são obrigatórios." });
  }

  const newMusic = musicModel.addMusic({ title, artist, genre, duration });
  res.status(201).json(newMusic);
};


exports.deleteMusic = (req, res) => {
  const id = parseInt(req.params.id);
  musicModel.deleteMusic(id);
  res.status(204).send();
};
