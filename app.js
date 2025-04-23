const express = require("express");
const app = express();

const pingRoutes = require("./routes/pingRoutes");

app.use(express.json());
app.use("/api", pingRoutes); // essa linha é essencial

module.exports = app;
