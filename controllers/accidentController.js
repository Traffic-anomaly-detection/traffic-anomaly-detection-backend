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
    const { road_no, km, direction, lat, lon, date_time } = req.body;
    const newAcc = await pool.query(
      "INSERT INTO accident (road_no, km, direction, lat, lon, date_time) VALUES($1,$2,$3,$4,$5) RETURNING *",
      [road_no, km, direction, lat, lon, date_time]
    );
    res.json(newAcc.rows[0]);
  } catch (err) {
    console.log(err.message);
  }
};
