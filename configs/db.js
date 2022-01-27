const Pool = require("pg").Pool;
const dotenv = require("dotenv");
dotenv.config();

const db_user = process.env.DB_USER;
const db_password = process.env.DB_PASSWORD;
const db_host = process.env.DB_HOST;
const db_port = process.env.DB_PORT;
const db_name = process.env.DB_NAME;

const pool = new Pool({
  user: db_user,
  password: db_password,
  host: db_host,
  port: db_port,
  database: db_name,
  dialectOptions: {
    ssl: {
      require: true,
      rejectUnauthorized: false,
    },
  },
});

module.exports = pool;
