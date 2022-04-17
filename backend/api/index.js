const express = require('express');
const app = express();

app.get('/api', (req,res)) => {
	const apikey = req.query.apikey;

	res.send({data: 'some data'});
});
