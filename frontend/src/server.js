const app = require('./App.js');

app.listen(3011, () => {
  console.log('CSE115 Server Running');
  console.log('API Testing UI is at: http://localhost:3011/v0/api-docs/');
});
