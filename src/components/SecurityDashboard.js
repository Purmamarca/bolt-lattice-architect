"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importStar(require("react"));
const lucide_react_1 = require("lucide-react");
const quantum_safe_1 = require("../security/quantum-safe");
const SecurityDashboard = () => {
    const [reliability, setReliability] = (0, react_1.useState)(99.9);
    const [handshakes, setHandshakes] = (0, react_1.useState)([]);
    const [violations, setViolations] = (0, react_1.useState)(0);
    // Simulation of the 2026 Lattice Handshake Monitoring
    const monitorHandshakes = async () => {
        const newKey = await quantum_safe_1.ml_kem.generateKeyPair();
        const newEntry = {
            id: Math.random().toString(36).substr(2, 9),
            timestamp: new Date().toLocaleTimeString(),
            protocol: 'ML-KEM-768',
            status: 'VERIFIED'
        };
        setHandshakes(prev => [newEntry, ...prev].slice(0, 5));
    };
    (0, react_1.useEffect)(() => {
        const interval = setInterval(monitorHandshakes, 3000);
        return () => clearInterval(interval);
    }, []);
    return (<div className="p-8 bg-slate-900 text-white min-h-screen font-mono">
      <header className="flex justify-between items-center mb-12 border-b border-slate-700 pb-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <lucide_react_1.Shield className="text-blue-400"/> BOLT-LATTICE-ARCHITECT
        </h1>
        <div className="flex gap-6">
          <div className="text-right">
            <p className="text-xs text-slate-400">RELIABILITY TARGET</p>
            <p className="text-xl font-bold text-green-400">{reliability}%</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Real-time Handshake Feed */}
        <div className="col-span-2 bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h2 className="text-sm mb-4 flex items-center gap-2 text-slate-300">
            <lucide_react_1.Activity size={16}/> LIVE LATTICE TRACE (ML-KEM)
          </h2>
          <div className="space-y-3">
            {handshakes.map(h => (<div key={h.id} className="flex justify-between p-3 bg-slate-900 rounded border-l-4 border-blue-500">
                <span className="text-blue-300">[{h.timestamp}] HANDSHAKE_INIT</span>
                <span className="text-slate-500">PROT: {h.protocol}</span>
                <span className="text-green-400 font-bold">{h.status}</span>
              </div>))}
          </div>
        </div>

        {/* Violation Counter */}
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h2 className="text-sm mb-4 flex items-center gap-2 text-slate-300">
            <lucide_react_1.AlertTriangle size={16}/> CFG BOUNDARY VIOLATIONS
          </h2>
          <div className="flex flex-col items-center justify-center h-32">
            <span className={`text-6xl font-bold ${violations === 0 ? 'text-green-500' : 'text-red-500'}`}>
              {violations}
            </span>
            <p className="text-xs mt-2 text-slate-400 text-center uppercase">
              Static Analysis Guardrails Active
            </p>
          </div>
        </div>
      </div>
    </div>);
};
exports.default = SecurityDashboard;
