import React, { useState, useEffect } from 'react';

function App() {
  const [vin, setVin] = useState('');
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [owner, setOwner] = useState('');
  const [vehicles, setVehicles] = useState([]);
  const [resp, setResp] = useState(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');

  // 👇 dynamically pick backend URL from environment or default to localhost
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Load vehicles on component mount
  useEffect(() => {
    fetchVehicles();
  }, []);

  async function fetchVehicles() {
    try {
      const r = await fetch(`${API_BASE}/vehicles/`);
      if (r.ok) {
        const data = await r.json();
        setVehicles(data);
      }
    } catch (err) {
      console.error('Error fetching vehicles:', err);
    }
  }

  async function createVehicle() {
    const body = { 
      vin: vin || `VIN${Date.now()}`, 
      make: make || 'Toyota', 
      model: model || 'Demo', 
      year: year ? parseInt(year) : 2020, 
      owner: owner || 'Demo User' 
    };

    try {
      const r = await fetch(`${API_BASE}/vehicles/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!r.ok) throw new Error(`Error: ${r.status}`);
      const data = await r.json();
      setResp(data);
      
      // Clear form and refresh list
      setVin('');
      setMake('');
      setModel('');
      setYear('');
      setOwner('');
      fetchVehicles();
    } catch (err) {
      console.error('Error creating vehicle:', err);
      setResp({ error: err.message });
    }
  }

  async function sendChatMessage() {
    if (!chatMessage.trim()) return;
    
    try {
      const r = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: chatMessage, use_memory: true }),
      });

      if (!r.ok) throw new Error(`Error: ${r.status}`);
      const data = await r.json();
      setChatResponse(data.response);
    } catch (err) {
      console.error('Error sending chat message:', err);
      setChatResponse(`Error: ${err.message}`);
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h1>Vehicle Maintenance System</h1>
      
      {/* Vehicle Creation Form */}
      <div style={{ marginBottom: 30, border: '1px solid #ccc', padding: 15, borderRadius: 5 }}>
        <h2>Add New Vehicle</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 10, marginBottom: 15 }}>
          <input
            placeholder="VIN (optional - auto-generated)"
            value={vin}
            onChange={(e) => setVin(e.target.value)}
          />
          <input
            placeholder="Make (e.g., Toyota)"
            value={make}
            onChange={(e) => setMake(e.target.value)}
          />
          <input
            placeholder="Model (e.g., Corolla)"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          />
          <input
            placeholder="Year (e.g., 2020)"
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
          />
          <input
            placeholder="Owner Name"
            value={owner}
            onChange={(e) => setOwner(e.target.value)}
          />
        </div>
        <button onClick={createVehicle} style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: 3 }}>
          Create Vehicle
        </button>
        {resp && (
          <div style={{ marginTop: 10, padding: 10, backgroundColor: resp.error ? '#f8d7da' : '#d4edda', borderRadius: 3 }}>
            <pre>{JSON.stringify(resp, null, 2)}</pre>
          </div>
        )}
      </div>

      {/* Vehicles List */}
      <div style={{ marginBottom: 30 }}>
        <h2>Vehicles ({vehicles.length})</h2>
        {vehicles.length > 0 ? (
          <div style={{ display: 'grid', gap: 10 }}>
            {vehicles.map(vehicle => (
              <div key={vehicle.id} style={{ border: '1px solid #ddd', padding: 10, borderRadius: 3, backgroundColor: '#f9f9f9' }}>
                <strong>VIN:</strong> {vehicle.vin} | 
                <strong> Make:</strong> {vehicle.make} | 
                <strong> Model:</strong> {vehicle.model} | 
                <strong> Year:</strong> {vehicle.year} | 
                <strong> Owner:</strong> {vehicle.owner}
              </div>
            ))}
          </div>
        ) : (
          <p>No vehicles found. Add one above!</p>
        )}
      </div>

      {/* Chat Interface */}
      <div style={{ border: '1px solid #ccc', padding: 15, borderRadius: 5 }}>
        <h2>AI Chat Assistant</h2>
        <div style={{ display: 'flex', gap: 10, marginBottom: 15 }}>
          <input
            style={{ flex: 1 }}
            placeholder="Ask about vehicles or maintenance..."
            value={chatMessage}
            onChange={(e) => setChatMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
          />
          <button onClick={sendChatMessage} style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: 3 }}>
            Send
          </button>
        </div>
        {chatResponse && (
          <div style={{ padding: 10, backgroundColor: '#e9ecef', borderRadius: 3, fontFamily: 'monospace' }}>
            <strong>Response:</strong> {chatResponse}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
