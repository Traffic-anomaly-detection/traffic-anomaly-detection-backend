const express = require("express");
const cors = require("cors");
const pool = require("./configs/db");
const apiRoutes = require("./routes/index");
const app = express();
const dotenv = require("dotenv");
dotenv.config();

const port = process.env.PORT;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.use("/api", apiRoutes);

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});
