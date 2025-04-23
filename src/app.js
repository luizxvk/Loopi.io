// app.js
const express = require('express');
const app = express();
const routes = require('./routes');

// Middleware para aceitar JSON
app.use(express.json());

// Middleware de rotas
app.use('/api', routes);

// Rota básica de saúde da API
app.get('/', (req, res) => {
  res.send('API Loopi.io no ar! 🚀');
});

module.exports = app;
