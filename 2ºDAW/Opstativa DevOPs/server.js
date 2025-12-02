const http = require("http");

const server = http.createServer((req, res) => {
  res.end("Hola! Esta es una página simple desde Node.js en Docker");
});

server.listen(3000, () => {
  console.log("Servidor escuchando en http://localhost:3000");
});
