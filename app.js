const express = require("express");
const app = express();

const musicRoutes = require("./routes/musicRoutes");

app.use(express.json());
app.use("/api/music", musicRoutes);

module.exports = app;
