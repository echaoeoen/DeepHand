var SerialPort = require('serialport');
var port = new SerialPort('/dev/cu.usbmodem1A12131', {
  baudRate: 9600
});

port.open(function (err) {
  if (err) {
    return console.log('Error opening port: ', err.message);
  }
 
  // Because there's no callback to write, write errors will be emitted on the port:
  // port.write('grasp#');
});

const express = require('express')
const app = express()

app.get('/cmd/:cmd', (req, res) => {
	res.send({"message":"ok"})
	port.write(req.params.cmd+"#")
})
app.get('/reset',(r,w)=>{
	w.send({"message":"reseted"})
	port.write("reset#")
})

app.listen(3000, () => console.log('Example app listening on port 3000!'))