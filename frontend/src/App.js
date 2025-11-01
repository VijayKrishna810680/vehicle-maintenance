import React, {useState} from 'react';

function App(){
  const [vin, setVin] = useState('');
  const [resp, setResp] = useState(null);

  async function createVehicle(){
    const body = { vin, make: 'Toyota', model: 'Demo', year: 2020, owner: 'Vijay' };
    const r = await fetch('http://localhost:8000/vehicles/', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body)
    });
    const data = await r.json();
    setResp(data);
  }

  return (
    <div style={{padding:20}}>
      <h2>Vehicle Maintenance - Demo</h2>
      <input placeholder="VIN" value={vin} onChange={e=>setVin(e.target.value)} />
      <button onClick={createVehicle}>Create</button>
      {resp && <pre>{JSON.stringify(resp, null, 2)}</pre>}
    </div>
  )
}

export default App;
