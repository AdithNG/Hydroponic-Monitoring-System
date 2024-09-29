import React, { useState, useEffect } from 'react';
import './Notes.css'; // Ensure this is the correct path
import { ref, push, onValue, remove } from 'firebase/database';
import { db } from './firebase';

const Notes = () => {
  const [note, setNote] = useState('');
  const [savedNotes, setSavedNotes] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const notesRef = ref(db, 'notes');
    onValue(notesRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const notesArray = Object.entries(data).map(([id, note]) => ({
          id,
          ...note,
        }));
        setSavedNotes(notesArray);
      } else {
        setSavedNotes([]);
      }
    });
  }, []);

  const saveNote = async () => {
    try {
      const noteRef = ref(db, 'notes');
      await push(noteRef, {
        content: note,
        timestamp: new Date().toISOString(),
      });
      setNote('');
      setMessage('Note saved successfully!');
    } catch (error) {
      console.error('Error saving note: ', error);
    }
  };

  const deleteNote = async (id) => {
    try {
      const noteRef = ref(db, `notes/${id}`);
      await remove(noteRef);
    } catch (error) {
      console.error('Error deleting note: ', error);
    }
  };

  return (
    <div className="notes-container">
      <h2>Your Hydroponic Notes</h2>
      <textarea
        className="note-input"
        value={note}
        onChange={(e) => setNote(e.target.value)}
        placeholder="Write your hydroponic notes here..."
      ></textarea>
      <button className="save-note-button" onClick={saveNote}>
        Save Note
      </button>
      {message && <p>{message}</p>}
      <h3>Saved Notes:</h3>
      <div className="notes-list">
        {savedNotes.length > 0 ? (
          savedNotes.map((note) => (
            <div className="note-item" key={note.id}>
              <div>
                <p>{note.content}</p>
                <span className="note-timestamp">Saved on: {new Date(note.timestamp).toLocaleString()}</span>
              </div>
              <div className="note-actions">
                <button className="delete-note-button" onClick={() => deleteNote(note.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))
        ) : (
          <p>No notes saved yet.</p>
        )}
      </div>
    </div>
  );
};

export default Notes;
