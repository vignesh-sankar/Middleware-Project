var mysql = require('mysql')
const uuidV4 = require('uuid/v4');

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'user',
  password : 'vidhya567',
  database : 'Middleware'
});

connection.connect()

exports.login = function(req, res){
	// console.log(req.body);
	var email = req.body.email;
	var pass = req.body.password;
	var queryDB = "SELECT * from LoginDetails where email='"+email+"' and password='"+pass+"'";
	console.log(queryDB);
	connection.query("SELECT * from LoginDetails where email='"+email+"' and password='"+pass+"'", function (err, rows, fields) {
	  	if (err){ console.log(err);}
	  	// console.log(err);
	  	// console.log('The solution is: ', rows[0].name);
		else{
	  		//console.log(rows[0]);
			if(rows.length == 0){ 
			//console.log(ret_val);
				res.send("Failure");
	
			}
			else 
			{console.log(rows);res.send("Success");}
			//res.send(rows[0].name);
			//return;
		}
	});	
	//connection.end();
	
};

exports.create = function(req,res){
	var email = req.body.email;
	var pass = req.body.password;
	var username=req.body.username;
	var phone = req.body.phoneno;
	var queryDB = "SELECT * from LoginDetails where email='"+email+"'";
	connection.query(queryDB,function(err,result){
	console.log(result);
		 if(result.length) {//console.log("value exists");
					res.send("Failure");}
		 else{
			 uuidV4();
			 console.log("else:create");
			 var insertDB = "INSERT INTO LoginDetails (email,password,name,phoneno) VALUES (\""+email+"\",\""+pass+"\",\""+username+"\",\""+phone+"\")";
	console.log(insertDB);
	connection.query(insertDB,function(err,result){
		if(err) throw err
		//console.log("Login details inserted");
		else {
		res.send("Success");}
	});
		 }
	});
	
	
};
