const pool = require("../configs/db");
const format = require("pg-format");

const dbname = "incident"

exports.getAccident = async (req, res) => {
  try {
    const allAccident = await pool.query(`SELECT * FROM ${dbname}`);
    res.json(allAccident.rows);
  } catch {}
};

exports.getAccidentByDatetime = async (req, res) => {
  try {
    const incident = await pool.query(
      `SELECT * FROM ${dbname} ORDER BY date_time DESC`
    );
    res.json(incident.rows);
  } catch (err) {
    res.json(err);
  }
};

exports.getAccidentByParam = async (req, res) => {
  try {
    const params = req.params.id;
    const someAccident = await pool.query(`SELECT * FROM ${dbname} LIMIT $1`, [
      params,
    ]);
    res.json(someAccident.rows);
  } catch {}
};

exports.createAccident = async (req, res) => {
  try {
    const {
      road_no,
      km,
      direction,
      inflow_units,
      outflow_units,
      samecell_units,
      all_units,
      avg_speed,
      lat,
      lon,
      date_time,
    } = req.body;
    const newAcc = await pool.query(
      `INSERT INTO ${dbname} (road_no, km, direction, inflow_units, outflow_units, samecell_units, all_units, avg_speed, lat, lon, date_time) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) RETURNING *`,
      [
        road_no,
        km,
        direction,
        inflow_units,
        outflow_units,
        samecell_units,
        all_units,
        avg_speed,
        lat,
        lon,
        date_time,
      ]
    );
    res.json(newAcc.rows[0]);
  } catch (err) {
    console.log(err.message);
  }
};

exports.bulkInsert = async (req, res) => {
  const sql =
    `INSERT INTO ${dbname} (road_no, km, direction, inflow_units, outflow_units, samecell_units, all_units, avg_speed, lat, lon, date_time) VALUES ?`;
  const values = req.body;
  try {
    const ress = await pool.query(
      format(
        `INSERT INTO ${dbname} (road_no, km, direction, inflow_units, outflow_units, samecell_units, all_units, avg_speed, lat, lon, date_time) VALUES %L RETURNING *`,
        values
      )
    );
    res.json(ress.rows);
  } catch (err) {
    console.log(err.message);
  }
};
