const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const port = 3000;

// Habilitar CORS para aceptar solicitudes desde cualquier origen
app.use(cors());

// Middleware para parsear el cuerpo de la solicitud como JSON
app.use(bodyParser.json());

// Datos de usuario ficticios para probar el login
const mockUser = {
  username: 'testuser',
  password: 'password123'
};

// Endpoint para login
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  // Comprobar las credenciales
  if (username === mockUser.username && password === mockUser.password) {
    return res.json({ message: 'Login exitoso', token: 'abc123' });
  } else {
    return res.status(401).json({ message: 'Credenciales incorrectas' });
  }
});

// Endpoint para obtener datos (solo para prueba)
app.get('/api/data', (req, res) => {
  res.json({ message: 'API funcionando correctamente' });
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
