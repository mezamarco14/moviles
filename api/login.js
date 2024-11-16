// Datos de usuario ficticios para prueba
const mockUser = {
  username: 'testuser',
  password: 'password123'
};

// Exportar como función serverless
module.exports = (req, res) => {
  // Verificar que la solicitud sea de tipo POST
  if (req.method === 'POST') {
    const { username, password } = req.body;

    // Verificar las credenciales
    if (username === mockUser.username && password === mockUser.password) {
      return res.status(200).json({ message: 'Login exitoso', token: 'abc123' });
    } else {
      return res.status(401).json({ message: 'Credenciales incorrectas' });
    }
  } else {
    // Si el método no es POST, devolver un error
    return res.status(405).json({ message: 'Método no permitido' });
  }
};
