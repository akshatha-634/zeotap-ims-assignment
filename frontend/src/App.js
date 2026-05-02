import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://127.0.0.1:8000/api';

const severityColor = { P0: '#ff4444', P1: '#ff8800', P2: '#ffcc00' };
const statusColor = { OPEN: '#ff4444', INVESTIGATING: '#ff8800', RESOLVED: '#00cc44', CLOSED: '#888888' };

export default function App() {
  const [workItems, setWorkItems] = useState([]);
  const [signals, setSignals] = useState([]);
  const [throughput, setThroughput] = useState(0);
  const [selected, setSelected] = useState(null);
  const [rca, setRca] = useState({ start: '', end: '', category: '', fix: '', prevention: '' });
  const [activeTab, setActiveTab] = useState('dashboard');

  const fetchData = async () => {
    try {
      const [wi, sig, tp] = await Promise.all([
        axios.get(`${API}/work-items`),
        axios.get(`${API}/signals/raw`),
        axios.get(`${API}/throughput`)
      ]);
      setWorkItems(wi.data.work_items.sort((a, b) => {
        const order = { P0: 0, P1: 1, P2: 2 };
        return order[a.severity] - order[b.severity];
      }));
      setSignals(sig.data.signals.reverse());
      setThroughput(tp.data.signals_per_second);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const updateStatus = async (componentId, newStatus) => {
    try {
      await axios.patch(`${API}/work-items/${componentId}/status`, { status: newStatus });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error updating status');
    }
  };

  const submitRCA = async () => {
    if (!rca.category || !rca.fix || !rca.prevention) {
      alert('Please fill all RCA fields!');
      return;
    }
    try {
      await axios.patch(`${API}/work-items/${selected.component_id}/status`, {
        status: 'CLOSED',
        rca: rca
      });
      setSelected(null);
      setRca({ start: '', end: '', category: '', fix: '', prevention: '' });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error submitting RCA');
    }
  };

  return (
    <div style={{ fontFamily: 'monospace', background: '#0d1117', minHeight: '100vh', color: '#e6edf3', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ color: '#58a6ff', margin: 0 }}>🚨 Incident Management System</h1>
        <div style={{ background: '#161b22', padding: '8px 16px', borderRadius: '8px', border: '1px solid #30363d' }}>
          📡 Throughput: <span style={{ color: '#3fb950' }}>{throughput} signals/sec</span>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        {['dashboard', 'signals'].map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            style={{ padding: '8px 20px', borderRadius: '6px', border: 'none', cursor: 'pointer',
              background: activeTab === tab ? '#58a6ff' : '#21262d', color: activeTab === tab ? '#000' : '#e6edf3' }}>
            {tab === 'dashboard' ? '📋 Dashboard' : '📡 Raw Signals'}
          </button>
        ))}
      </div>

      {activeTab === 'dashboard' && (
        <div>
          <h2 style={{ color: '#8b949e' }}>Active Incidents ({workItems.length})</h2>
          {workItems.length === 0 && <p style={{ color: '#8b949e' }}>No incidents yet. Send some signals!</p>}
          {workItems.map(item => (
            <div key={item.id} onClick={() => setSelected(item)}
              style={{ background: '#161b22', border: `1px solid ${severityColor[item.severity]}`,
                borderRadius: '8px', padding: '16px', marginBottom: '12px', cursor: 'pointer' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ color: severityColor[item.severity], fontWeight: 'bold' }}>[{item.severity}]</span>
                  {' '}<span style={{ fontSize: '16px' }}>{item.component_id}</span>
                  <span style={{ color: '#8b949e', marginLeft: '10px' }}>({item.signal_count} signals)</span>
                </div>
                <span style={{ background: statusColor[item.status], color: '#000',
                  padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold' }}>
                  {item.status}
                </span>
              </div>
              <div style={{ marginTop: '10px', display: 'flex', gap: '8px' }}>
                {item.status === 'OPEN' && (
                  <button onClick={(e) => { e.stopPropagation(); updateStatus(item.component_id, 'INVESTIGATING'); }}
                    style={{ background: '#ff8800', border: 'none', color: '#000', padding: '4px 12px', borderRadius: '4px', cursor: 'pointer' }}>
                    → Investigate
                  </button>
                )}
                {item.status === 'INVESTIGATING' && (
                  <button onClick={(e) => { e.stopPropagation(); updateStatus(item.component_id, 'RESOLVED'); }}
                    style={{ background: '#00cc44', border: 'none', color: '#000', padding: '4px 12px', borderRadius: '4px', cursor: 'pointer' }}>
                    → Resolve
                  </button>
                )}
                {item.status === 'RESOLVED' && (
                  <button onClick={(e) => { e.stopPropagation(); setSelected(item); }}
                    style={{ background: '#888', border: 'none', color: '#fff', padding: '4px 12px', borderRadius: '4px', cursor: 'pointer' }}>
                    → Close (RCA)
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'signals' && (
        <div>
          <h2 style={{ color: '#8b949e' }}>Raw Signal Log (last 100)</h2>
          {signals.map((sig, i) => (
            <div key={i} style={{ background: '#161b22', border: '1px solid #30363d',
              borderRadius: '6px', padding: '10px', marginBottom: '8px', fontSize: '13px' }}>
              <span style={{ color: severityColor[sig.severity] }}>[{sig.severity}]</span>
              {' '}<span style={{ color: '#58a6ff' }}>{sig.component_id}</span>
              {' — '}{sig.message}
              <span style={{ color: '#8b949e', float: 'right' }}>{sig.timestamp}</span>
            </div>
          ))}
        </div>
      )}

      {selected && selected.status === 'RESOLVED' && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ background: '#161b22', border: '1px solid #30363d', borderRadius: '12px', padding: '30px', width: '500px' }}>
            <h2 style={{ color: '#58a6ff', marginTop: 0 }}>📝 Root Cause Analysis</h2>
            <p style={{ color: '#8b949e' }}>Component: <strong style={{ color: '#e6edf3' }}>{selected.component_id}</strong></p>
            {[
              { label: 'Incident Start', key: 'start', type: 'datetime-local' },
              { label: 'Incident End', key: 'end', type: 'datetime-local' },
            ].map(f => (
              <div key={f.key} style={{ marginBottom: '12px' }}>
                <label style={{ color: '#8b949e', display: 'block', marginBottom: '4px' }}>{f.label}</label>
                <input type={f.type} value={rca[f.key]}
                  onChange={e => setRca({ ...rca, [f.key]: e.target.value })}
                  style={{ width: '100%', background: '#0d1117', border: '1px solid #30363d', color: '#e6edf3', padding: '8px', borderRadius: '4px' }} />
              </div>
            ))}
            <div style={{ marginBottom: '12px' }}>
              <label style={{ color: '#8b949e', display: 'block', marginBottom: '4px' }}>Root Cause Category</label>
              <select value={rca.category} onChange={e => setRca({ ...rca, category: e.target.value })}
                style={{ width: '100%', background: '#0d1117', border: '1px solid #30363d', color: '#e6edf3', padding: '8px', borderRadius: '4px' }}>
                <option value=''>Select category</option>
                <option>Infrastructure Failure</option>
                <option>Code Deployment</option>
                <option>Network Issue</option>
                <option>Database Failure</option>
                <option>Third Party Service</option>
              </select>
            </div>
            {[
              { label: 'Fix Applied', key: 'fix' },
              { label: 'Prevention Steps', key: 'prevention' }
            ].map(f => (
              <div key={f.key} style={{ marginBottom: '12px' }}>
                <label style={{ color: '#8b949e', display: 'block', marginBottom: '4px' }}>{f.label}</label>
                <textarea value={rca[f.key]} onChange={e => setRca({ ...rca, [f.key]: e.target.value })}
                  rows={3} style={{ width: '100%', background: '#0d1117', border: '1px solid #30363d',
                    color: '#e6edf3', padding: '8px', borderRadius: '4px', resize: 'vertical' }} />
              </div>
            ))}
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
              <button onClick={() => setSelected(null)}
                style={{ background: '#21262d', border: 'none', color: '#e6edf3', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer' }}>
                Cancel
              </button>
              <button onClick={submitRCA}
                style={{ background: '#58a6ff', border: 'none', color: '#000', padding: '8px 20px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>
                Submit RCA & Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}