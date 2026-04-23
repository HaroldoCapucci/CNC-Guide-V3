import React, { useState } from 'react';
import { Viewer3D } from './components/Viewer3D';

function App() {
  const [gcode, setGcode] = useState('');
  const [machineType, setMachineType] = useState('mitsubishi');
  const [processed, setProcessed] = useState('');

  const handleProcess = async () => {
    const res = await fetch('http://localhost:5000/api/post-process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gcode, machine_type: machineType }),
    });
    const data = await res.json();
    if (data.success) setProcessed(data.gcode);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <h1>CNC-Guide V3</h1>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <textarea
          rows={10}
          cols={50}
          value={gcode}
          onChange={(e) => setGcode(e.target.value)}
          placeholder="Cole seu G-code aqui"
        />
        <div>
          <select value={machineType} onChange={(e) => setMachineType(e.target.value)}>
            <option>mitsubishi</option><option>fanuc</option><option>haas</option><option>siemens</option>
          </select>
          <button onClick={handleProcess}>Processar</button>
        </div>
      </div>
      {processed && (
        <div>
          <h3>G-code processado</h3>
          <textarea rows={10} cols={80} value={processed} readOnly />
        </div>
      )}
      <Viewer3D gcode={gcode} />
    </div>
  );
}

export default App;
