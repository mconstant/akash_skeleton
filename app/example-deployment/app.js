var express = require('express');
var app = express();
app.get('/', function (req, res) {
  // send the env variable MSG
  res.send('The message is: ' + process.env.TOP_SECRET_MESSAGE);
});
app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});