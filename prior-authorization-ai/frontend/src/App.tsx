import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { DataStatus } from './pages/DataStatus';
import { SyntheaCases } from './pages/SyntheaCases';
import { UploadCase } from './pages/UploadCase';
import { PolicyExplorer } from './pages/PolicyExplorer';
import { Evaluation } from './pages/Evaluation';
import './styles/global.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <aside className="sidebar">
          <h2>PA Companion</h2>
          <nav>
            <NavLink to="/">Dashboard</NavLink>
            <NavLink to="/data-status">Data Status</NavLink>
            <NavLink to="/synthea-cases">Synthea Cases</NavLink>
            <NavLink to="/upload">Upload Patient</NavLink>
            <NavLink to="/policy-explorer">Policy Explorer</NavLink>
            <NavLink to="/evaluation">Evaluation</NavLink>
          </nav>
        </aside>
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/data-status" element={<DataStatus />} />
            <Route path="/synthea-cases" element={<SyntheaCases />} />
            <Route path="/upload" element={<UploadCase />} />
            <Route path="/policy-explorer" element={<PolicyExplorer />} />
            <Route path="/evaluation" element={<Evaluation />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
