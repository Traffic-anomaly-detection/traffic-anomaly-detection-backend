const accidentRoutes = require("express").Router();
const accidentController = require("../controllers/accidentController");

accidentRoutes.get("/", accidentController.getAccident);
accidentRoutes.get("/bydate", accidentController.getAccidentByDatetime);
accidentRoutes.get("/byid/:id", accidentController.getAccidentByParam);
accidentRoutes.post("/", accidentController.createAccident);
accidentRoutes.post("/bulk", accidentController.bulkInsert);

module.exports = accidentRoutes;
