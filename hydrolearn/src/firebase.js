import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getDatabase } from 'firebase/database';

// Your Firebase configuration details
const firebaseConfig = {
    apiKey: "AIzaSyDhUDemOsNC9LeMsuNk7J9MSH1sGWXr8hI",
    authDomain: "hydrolearn-f411f.firebaseapp.com",
    databaseURL: "https://hydrolearn-f411f-default-rtdb.firebaseio.com",
    projectId: "hydrolearn-f411f",
    storageBucket: "hydrolearn-f411f.appspot.com",
    messagingSenderId: "120501477962",
    appId: "1:120501477962:web:89a00b2ee43b760430bcb3",
    measurementId: "G-GPSVNRBWD9"
  };


// Initialize Firebase app
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and export it
const auth = getAuth(app);

// Initialize Firebase Realtime Database and export it
const db = getDatabase(app);

export { auth, db };



