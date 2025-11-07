ASISTENCIA_CONFIRMACION_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Confirmación de Asistencia</title>
  <style>
    body {
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: #f5f7fa;
      color: #333;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 600px;
      background-color: #ffffff;
      border-radius: 10px;
      margin: 40px auto;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .header {
      background-color: #05668d;
      color: #ffffff;
      text-align: center;
      padding: 25px;
    }
    .header h1 {
      font-size: 22px;
      margin: 0;
    }
    .body {
      padding: 25px 30px;
      line-height: 1.6;
    }
    .body h2 {
      color: #05668d;
      font-size: 20px;
      margin-bottom: 10px;
    }
    .highlight {
      color: #05668d;
      font-weight: bold;
    }
    .info {
      background-color: #f1f8ff;
      border-left: 4px solid #028090;
      padding: 10px 15px;
      margin: 20px 0;
      border-radius: 6px;
    }
    .footer {
      text-align: center;
      font-size: 12px;
      color: #777;
      padding: 15px 10px;
      background-color: #f0f0f0;
    }
    .footer a {
      color: #028090;
      text-decoration: none;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Confirmación de Asistencia</h1>
    </div>

    <div class="body">
      <h2>Hola <span class="highlight">{{nombre}}</span>,</h2>
      <p>Tu asistencia a la reunión <strong>"{{titulo}}"</strong> ha sido registrada exitosamente.</p>

      <div class="info">
        <p><strong>📅 Fecha:</strong> {{fecha}}</p>
        <p><strong>🕓 Hora:</strong> {{hora}}</p>
        <p><strong>📍 Ubicación:</strong> {{ubicacion}}</p>
      </div>

      <p>Gracias por participar en las actividades de la <strong>Comunidad Quillacinga</strong>.</p>
      <p>Tu compromiso fortalece nuestra comunidad. 💪</p>
    </div>

    <div class="footer">
      <p>Este correo fue enviado automáticamente. Por favor, no respondas a este mensaje.</p>
      <p>© 2025 Comunidad Quillacinga | <a href="quillacinga-consaca.ddns.net">quillacinga-consaca.ddns.net</a></p>
    </div>
  </div>
</body>
</html>
"""
