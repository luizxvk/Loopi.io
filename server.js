const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para aceitar JSON
app.use(express.json());

// Rota de teste
app.get('/', (req, res) => {
  res.send('API Loopi.io no ar! 🚀');
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
