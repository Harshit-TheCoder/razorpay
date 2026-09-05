"use client";

import { useEffect, useState } from "react";
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart 
} from 'recharts';
import { ArrowUpRight, TrendingUp, DollarSign, Activity, AlertCircle, CheckCircle2, AlertTriangle } from 'lucide-react';
import Link from 'next/link';
import LiveFeed from '@/components/live-activity/LiveFeed';

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [cases, setCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        // Fetch cases first to get a merchant ID
        const casesRes = await fetch("/api/v1/cases");
        if (!casesRes.ok) {
          throw new Error(`Failed to fetch cases: ${casesRes.status} ${casesRes.statusText}`);
        }
        const casesData = await casesRes.json();
        setCases(casesData);

        if (casesData.length > 0) {
          const merchantId = casesData[0].merchant_id;
          const metricsRes = await fetch(`/api/v1/analytics/metrics/${merchantId}`);
          if (metricsRes.ok) {
            const metricsData = await metricsRes.json();
            setMetrics(metricsData);
          }
        }
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  // Generate some mock chart data based on metrics for visualization
  const chartData = [
    { name: 'Mon', recovered: 4000, atRisk: 5000 },
    { name: 'Tue', recovered: 3000, atRisk: 4000 },
    { name: 'Wed', recovered: 5000, atRisk: 6000 },
    { name: 'Thu', recovered: 4500, atRisk: 4800 },
    { name: 'Fri', recovered: 6000, atRisk: 7000 },
    { name: 'Sat', recovered: parseInt(metrics?.revenue_recovered) || 8000, atRisk: parseInt(metrics?.revenue_at_risk) || 9000 },
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Revenue Recovery Overview</h1>
        <p className="text-gray-400">Monitor and manage AI-driven recovery across your platforms.</p>
      </header>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 -mr-4 -mt-4 w-24 h-24 bg-indigo-500/10 rounded-full blur-2xl group-hover:bg-indigo-500/20 transition-all"></div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 font-medium">Revenue at Risk</h3>
            <Activity className="text-indigo-400 w-5 h-5" />
          </div>
          <p className="text-3xl font-bold text-white">₹{metrics?.revenue_at_risk?.toLocaleString() || "0"}</p>
        </div>

        <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 -mr-4 -mt-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl group-hover:bg-emerald-500/20 transition-all"></div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 font-medium">Recovered</h3>
            <CheckCircle2 className="text-emerald-400 w-5 h-5" />
          </div>
          <p className="text-3xl font-bold text-emerald-400">₹{metrics?.revenue_recovered?.toLocaleString() || "0"}</p>
        </div>

        <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 -mr-4 -mt-4 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl group-hover:bg-blue-500/20 transition-all"></div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 font-medium">Recovery Rate</h3>
            <TrendingUp className="text-blue-400 w-5 h-5" />
          </div>
          <p className="text-3xl font-bold text-white">{(metrics?.recovery_rate * 100).toFixed(1) || "0"}%</p>
        </div>

        <div className="glass-card p-6 rounded-2xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 -mr-4 -mt-4 w-24 h-24 bg-amber-500/10 rounded-full blur-2xl group-hover:bg-amber-500/20 transition-all"></div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 font-medium">Unresolved Cases</h3>
            <AlertTriangle className="text-amber-400 w-5 h-5" />
          </div>
          <p className="text-3xl font-bold text-amber-400">{metrics?.unresolved_cases || "0"}</p>
        </div>
      </div>

      {/* Main Chart area */}
      <div className="glass-card p-6 rounded-2xl mt-8">
        <h3 className="text-xl font-semibold text-white mb-6">Recovery Trends</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorRecovered" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="name" stroke="#4b5563" tick={{fill: '#9ca3af'}} />
              <YAxis stroke="#4b5563" tick={{fill: '#9ca3af'}} />
              <Tooltip 
                contentStyle={{ backgroundColor: 'rgba(15, 17, 26, 0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                itemStyle={{ color: '#fff' }}
              />
              <Area type="monotone" dataKey="atRisk" stroke="#6366f1" fillOpacity={1} fill="url(#colorRisk)" />
              <Area type="monotone" dataKey="recovered" stroke="#10b981" fillOpacity={1} fill="url(#colorRecovered)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Cases Preview */}
      <div className="glass-card p-6 rounded-2xl mt-8">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-semibold text-white">Recent Cases</h3>
          <Link href="/cases" className="text-indigo-400 hover:text-indigo-300 text-sm font-medium transition-colors">
            View All →
          </Link>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-gray-800 text-gray-400 text-sm">
                <th className="pb-3 font-medium px-4">Case ID</th>
                <th className="pb-3 font-medium px-4">Scenario</th>
                <th className="pb-3 font-medium px-4">Status</th>
                <th className="pb-3 font-medium px-4">Opened</th>
              </tr>
            </thead>
            <tbody>
              {cases.slice(0, 5).map((c) => (
                <tr key={c.id} className="border-b border-gray-800/50 hover:bg-white/5 transition-colors group cursor-pointer">
                  <td className="py-4 px-4 text-gray-300 font-mono text-sm">
                    <Link href={`/cases/${c.id}`} className="group-hover:text-indigo-400 transition-colors">
                      {c.id.substring(0,8)}...
                    </Link>
                  </td>
                  <td className="py-4 px-4 text-white capitalize">{c.scenario_type.replace(/_/g, ' ')}</td>
                  <td className="py-4 px-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                      c.state === 'RECOVERED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 
                      c.state === 'FAILED' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 
                      'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                    }`}>
                      {c.state}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-gray-400 text-sm">
                    {new Date(c.opened_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
              {cases.length === 0 && (
                <tr>
                  <td colSpan={4} className="py-8 text-center text-gray-500">
                    No recent cases found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
