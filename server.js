const express = require('express');
const session = require('express-session');
const path = require('path');
const { initializeApp } = require('firebase/app');
const { getFirestore, collection, addDoc, getDocs, query, where } = require('firebase/firestore');

const app = express();
const PORT = process.env.PORT || 3000;

// Конфигурация Firebase
const firebaseConfig = {
  apiKey: "AIzaSyBtrjMqUbS1K4qidCs5hRDCCqjV5JOul8",
  authDomain: "my-project-685aa.firebaseapp.com",
  projectId: "my-project-685aa",
  storageBucket: "my-project-685aa.firebasestorage.app",
  messagingSenderId: "670461810198",
  appId: "1:670461810198:web:e990346883ce18e6dc737",
  measurementId: "G-HF6JSEGXPJ"
};

const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));

app.use(session({
  secret: 'my-super-secret-key',
  resave: false,
  saveUninitialized: false
}));

// Регистрация
app.post('/api/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    const usersRef = collection(db, 'users');
    
    // Проверяем, есть ли уже такой email
    const q = query(usersRef, where('email', '==', email));
    const querySnapshot = await getDocs(q);
    
    if (!querySnapshot.empty) {
      return res.status(400).json({ success: false, message: 'Пользователь с таким email уже существует' });
    }

    await addDoc(usersRef, { username, email, password, role: 'player' });
    res.json({ success: true, message: 'Регистрация успешна!' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Ошибка сервера' });
  }
});

// Логин
app.post('/api/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const usersRef = collection(db, 'users');
    
    const q = query(usersRef, where('email', '==', email), where('password', '==', password));
    const querySnapshot = await getDocs(q);
    
    if (querySnapshot.empty) {
      return res.status(400).json({ success: false, message: 'Неверный email или пароль' });
    }

    const userData = querySnapshot.docs[0].data();
    req.session.user = { username: userData.username, email: userData.email, role: userData.role };
    
    res.json({ success: true, user: req.session.user });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, message: 'Ошибка сервера' });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Сервер запущен на http://localhost:${PORT}`);
});
