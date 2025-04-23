const app = require("./app");

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 API Loopi.io no ar em http://localhost:${PORT}`);
});
