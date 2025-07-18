🧴 Gestor de Lociones

Una aplicación web interactiva para administrar lociones, clientes, compras y reportes. Desarrollada con Python y Streamlit, conectada a una base de datos PostgreSQL alojada en Supabase.

⸻

🚀 Características principales
• 👥 Registro, inicio de sesión y roles (cliente, empleado, administrador)
• 🛍️ Catálogo visual de lociones con imagen y stock
• 📦 CRUD completo de clientes, lociones y compras
• 🔒 Autorización de usuarios por rol
• 📊 Gráficos de ventas en tiempo real
• 📁 Exportación de compras a CSV
• ✅ Validaciones básicas para formularios y acciones

⸻

🛠 Tecnologías y herramientas utilizadas

1. Lenguaje y Backend
   • Python
   • Librerías:
   • streamlit (interfaz web)
   • psycopg2 (conexión a PostgreSQL)
   • pandas, matplotlib (análisis y gráficas)
   • werkzeug.security (hash de contraseñas)
   • rich (menú CLI bonito en la versión consola)

2. Interfaz Web
   • Streamlit
   • Navegación por menú
   • Formularios, tablas, gráficas

3. Base de Datos
   • PostgreSQL
   • Supabase ✨
   • Servicio en la nube que aloja la base de datos
   • Usamos su editor SQL para insertar datos reales
   • Acceso desde Python mediante psycopg2

4. Extras
   • Exportación a CSV para reportes
   • Control de roles y autorizaciones
   • Gráficas de torta, barras y líneas para visualización de datos

⸻

📂 Estructura del proyecto

.
├── app.py
├── auth/
│ └── usuarios.py
├── database/
│ └── connection.py
├── modules/
│ ├── clientes.py
│ ├── compras.py
│ ├── productos.py
│ └── reportes.py
├── utils/
│ └── helpers.py
├── views/
│ ├── catalogo_view.py
│ ├── clientes_view.py
│ ├── compras_view.py
│ ├── graficos.py
│ ├── lociones_view.py
│ ├── menu.py
│ ├── panel_admin.py
│ ├── roles_view.py
│ └── autorizacion_view.py

⸻

🔓 Roles y permisos

Rol Puede acceder a…
Cliente Catálogo, registrar compras
Empleado Gestionar clientes y lociones, ver reportes
Administrador Autorizar usuarios, asignar roles, todo

⸻

🧪 Datos de prueba sugeridos

Puedes insertar lociones, clientes y compras reales usando el editor SQL de Supabase o la interfaz Streamlit. La app ya está preparada para funcionar con datos reales.

⸻

🧭 Próximas mejoras
• Validación avanzada con expresiones regulares
• Interfaz gráfica con imagen para cada usuario
• Dashboards con Seaborn o Plotly
• Conexión con API o integración con pagos

⸻

🤝 Créditos

Desarrollado por Anderson Rengifo con la ayuda de ChatGPT como copiloto técnico y mentor.

⸻

📬 Contacto

Si quieres mejorar esta app o colaborar, puedes escribirme a: anderson…@correo.com (ajusta con tu correo real)

⸻

“La mejor forma de aprender a programar es construir cosas reales.” ✨
