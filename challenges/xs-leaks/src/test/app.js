const express = require("express");
const APP_URL = process.env.APP_URL || "http://localhost:5000/login"
// App setup
const PORT = 3000;
const app = express();
app.get("/", (req, res) => {
  url = req.query.url
  console.log(url)
  try{
  parsed = new URL("",url)  
  }catch(ee){
    console.log("parsing broke")
  }
  res.send("admin will visit your url");
});
const server = app.listen(PORT, function () {
  console.log(`Listening on port ${PORT}`);
  console.log(`http://localhost:${PORT}`);
});