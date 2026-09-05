"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, Filter, ChevronRight } from "lucide-react";

export default function CasesList() {
  const [cases, setCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    async function fetchCases() {
      try {
        const res = await fetch("/api/v1/cases");
        if (!res.ok) {
          throw new Error(`Failed to fetch cases: ${res.status} ${res.statusText}`);
        }
        const data = await res.json();
        setCases(data);
      } catch (error) {
        console.error("Failed to fetch cases:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchCases();
  }, []);

  const filteredCases = cases.filter(c => 
    c.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.scenario_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.state.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Recovery Cases</h1>
          <p className="text-gray-400">All active and resolved revenue recovery incidents.</p>
        </div>
      </header>

      <div className="glass-card rounded-2xl overflow-hidden">
        {/* Toolbar */}
        <div className="p-4 border-b border-gray-800 flex justify-between items-center bg-white/5">
          <div className="relative w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input 
              type="text" 
              placeholder="Search cases..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-black/20 border border-gray-700 text-sm rounded-lg pl-10 pr-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 transition-colors"
            />
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-black/20 border border-gray-700 rounded-lg text-sm text-gray-300 hover:bg-white/10 transition-colors">
            <Filter className="w-4 h-4" />
            <span>Filter</span>
          </button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          {loading ? (
            <div className="py-24 flex justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-800 text-gray-400 text-sm bg-black/10">
                  <th className="py-4 font-medium px-6">Case ID</th>
                  <th className="py-4 font-medium px-6">Merchant</th>
                  <th className="py-4 font-medium px-6">Scenario</th>
                  <th className="py-4 font-medium px-6">Status</th>
                  <th className="py-4 font-medium px-6">Opened At</th>
                  <th className="py-4 font-medium px-6 text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredCases.map((c) => (
                  <tr key={c.id} className="border-b border-gray-800/50 hover:bg-white/5 transition-colors group">
                    <td className="py-5 px-6 text-gray-300 font-mono text-sm">
                      {c.id}
                    </td>
                    <td className="py-5 px-6 text-gray-300">
                      {c.merchant_id}
                    </td>
                    <td className="py-5 px-6 text-white capitalize">
                      {c.scenario_type.replace(/_/g, ' ')}
                    </td>
                    <td className="py-5 px-6">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                        c.state === 'RECOVERED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 
                        c.state === 'FAILED' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 
                        'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                      }`}>
                        {c.state}
                      </span>
                    </td>
                    <td className="py-5 px-6 text-gray-400 text-sm">
                      {new Date(c.opened_at).toLocaleString()}
                    </td>
                    <td className="py-5 px-6 text-right">
                      <Link 
                        href={`/cases/${c.id}`} 
                        className="inline-flex items-center text-indigo-400 hover:text-indigo-300 text-sm font-medium transition-colors p-2 hover:bg-indigo-500/10 rounded-lg"
                      >
                        View <ChevronRight className="w-4 h-4 ml-1" />
                      </Link>
                    </td>
                  </tr>
                ))}
                {filteredCases.length === 0 && (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-gray-500">
                      No cases found matching your search.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
