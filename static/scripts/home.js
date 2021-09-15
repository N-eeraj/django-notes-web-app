const newNote = () => window.location.href='/new';

const viewNote = note => window.location.href='/view_note?note='+note;
const editNote = note => window.location.href='/edit_note?note='+note;
const deleteNote = note => window.location.href='/delete_note?note='+note;