const accidentRoutes = require("express").Router();
const accidentController = require("../controllers/accidentController");

accidentRoutes.get("/", accidentController.getAccident);
accidentRoutes.get("/:id",accidentController.getAccidentByParam)
accidentRoutes.post("/", accidentController.createAccident);

module.exports = accidentRoutes;
