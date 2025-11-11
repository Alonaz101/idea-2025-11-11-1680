import React, { useState } from 'react';

const moods = ['Happy', 'Sad', 'Excited', 'Calm'];

export default function MoodInputComponent({ onMoodSelected }) {
  const [selectedMood, setSelectedMood] = useState('Happy');

  const handleMoodChange = (event) => {
    setSelectedMood(event.target.value);
    if(onMoodSelected) onMoodSelected(event.target.value);
  };

  return (
    <div>
      <h3>How are you feeling today?</h3>
      <select value={selectedMood} onChange={handleMoodChange}>
        {moods.map(mood => (
          <option key={mood} value={mood}>{mood}</option>
        ))}
      </select>
    </div>
  );
}
