# deep
```
ticketsystem/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── sockets.py
│   ├── utils.py
│   └── admin/
│       ├── routes.py
│       └── forms.py
├── templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   ├── admin.html
│   │   └── user.html
│   └── tickets/
│       ├── create.html
│       └── detail.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── main.js
│       └── socket.js
├── uploads/
├── logs/
├── requirements.txt
├── config.py
├── docker-compose.yml
├── Dockerfile
└── nginx.conf
```



```
To complete the setup:

Make setup.sh executable:

bash
Copy
chmod +x setup.sh
Run the setup:

bash
Copy
./setup.sh
Start with Docker:

bash
Copy
docker-compose up --build
```
