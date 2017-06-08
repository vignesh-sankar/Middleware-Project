var express = require('express');
var app = express();
var path = require('path');
var controller = require('./controller/controller')
var bodyParser = require('body-parser')

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 

app.use(express.static('public'));
app.use('/static', express.static(path.join(__dirname, 'public')))

app.set('views', __dirname + '/views');
//app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');

app.get('/', function (req, res) {
   res.render('main.ejs');
})

app.post('/login', function (req, res) {
  // console.log(req.body.password);
  	controller.login(req,res);
  	//res.redirect('/dashboard');
})

app.post('/create', function (req, res) {
  // console.log(req.body.password);
  	controller.create(req,res);
  	//res.redirect('/dashboard');
})
app.get('/dashboard', function(req, res){
	res.render('status.ejs');
})

var server = app.listen(8085, function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Example app listening at http://%s:%s", host, port)
})
