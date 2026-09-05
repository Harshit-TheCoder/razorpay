"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle, Clock } from "lucide-react";
import Link from "next/link";

export default function EscalationsPage() {
  const [escalations, setEscalations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchEscalations();
  }, []);

  async function fetchEscalations() {
    try {
      const res = await fetch("/api/v1/escalations");
      if (!res.ok) throw new Error("Failed to fetch escalations");
      const data = await res.json();
      setEscalations(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function resolveEscalation(caseId: string) {
    try {
      const res = await fetch(`/api/v1/escalations/${caseId}/resolve`, {
        method: 'POST'
      });
      if (res.ok) {
        fetchEscalations();
      }
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <AlertTriangle className="w-8 h-8 mr-3 text-amber-500" />
            Human Review Queue
          </h1>
          <p className="text-gray-400 mt-2">Cases blocked by the Policy Engine requiring manual override or resolution.</p>
        </div>
        <div className="px-4 py-2 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-lg font-medium">
          {escalations.length} Pending
        </div>
      </div>

      <div className="glass-card rounded-2xl overflow-hidden border border-white/5">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5 border-b border-white/5">
              <th className="p-4 font-semibold text-gray-300">Case ID</th>
              <th className="p-4 font-semibold text-gray-300">Scenario</th>
              <th className="p-4 font-semibold text-gray-300">Escalated At</th>
              <th className="p-4 font-semibold text-gray-300 text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {escalations.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-8 text-center text-gray-500">
                  <CheckCircle className="w-12 h-12 mx-auto mb-3 text-emerald-500/50" />
                  No pending escalations. The queue is clear!
                </td>
              </tr>
            ) : (
              escalations.map((c) => (
                <tr key={c.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                  <td className="p-4">
                    <Link href={`/cases/${c.id}`} className="font-mono text-sm text-indigo-400 hover:underline">
                      {c.id}
                    </Link>
                  </td>
                  <td className="p-4 text-gray-300 capitalize">{c.scenario_type.replace(/_/g, ' ')}</td>
                  <td className="p-4 text-gray-400 flex items-center">
                    <Clock className="w-4 h-4 mr-2 text-gray-500" />
                    {new Date(c.opened_at).toLocaleDateString()}
                  </td>
                  <td className="p-4 text-right">
                    <button 
                      onClick={() => resolveEscalation(c.id)}
                      className="px-4 py-1.5 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 rounded-lg text-sm font-medium transition-colors border border-emerald-500/20"
                    >
                      Resolve & Resume
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
