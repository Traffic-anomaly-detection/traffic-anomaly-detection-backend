const express = require("express");
const accidentRoutes = require("./accidentRoutes");

const router = express.Router();

router.get("/", (req, res) => {
  res.send("API ROUTE");
});

router.use("/accident", accidentRoutes);

module.exports = router;
