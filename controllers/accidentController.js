const pool = require("../configs/db");

exports.getAccident = async (req, res) => {
  try {
    const allAccident = await pool.query("SELECT * FROM accident");
    res.json(allAccident.rows);
  } catch {}
};

exports.getAccidentByParam = async (req, res) => {
  try {
    const params = req.params.id;
    const someAccident = await pool.query("SELECT * FROM accident LIMIT $1", [
      params,
    ]);
    res.json(someAccident.rows);
  } catch {}
};

exports.createAccident = async (req, res) => {
  try {
    const accidentData = {
      road_no: req.body.road_no,
      km: req.body.km,
      lat: req.body.lat,
      lon: req.body.lon,
      date_time: req.body.date_time,
    };
    const newAcc = await pool.query(
      "INSERT INTO accident (road_no, km, lat, lon, date_time) VALUES($1,$2,$3,$4,$5)",
      [
        accidentData.road_no,
        accidentData.km,
        accidentData.lat,
        accidentData.lon,
        accidentData.date_time,
      ]
    );
    res.json(newAcc);
  } catch (err) {
    console.log(err.message);
  }
};
