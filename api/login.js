// api/login.js

const bodyParser = require('body-parser');

// Datos de usuario ficticios para prueba
const mockUser = {
  username: 'testuser',
  password: 'password123'
};

// Exportar como función serverless
module.exports = (req, res) => {
  // Middleware para parsear el cuerpo como JSON
  bodyParser.json()(req, res, () => {
    const { username, password } = req.body;

    // Verificar las credenciales
    if (username === mockUser.username && password === mockUser.password) {
      return res.status(200).json({ message: 'Login exitoso', token: 'abc123' });
    } else {
      return res.status(401).json({ message: 'Credenciales incorrectas' });
    }
  });
};
