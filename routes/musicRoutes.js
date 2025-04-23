// routes/musicRoutes.js
const express = require("express");
const router = express.Router();
const musicController = require("../controllers/musicController");

// GET /api/music
router.get("/", musicController.getAllMusic);

// GET /api/music/:id
router.get("/:id", musicController.getMusicById);

// POST /api/music
router.post("/", musicController.addMusic);

// DELETE /api/music/:id
router.delete("/:id", musicController.deleteMusic);




module.exports = router;
