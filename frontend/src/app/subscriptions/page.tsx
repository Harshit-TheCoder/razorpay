"use client";

import { useEffect, useState } from "react";
import { RefreshCcw, AlertCircle } from "lucide-react";

export default function SubscriptionsPage() {
  const [subscriptions, setSubscriptions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchSubscriptions() {
      try {
        const res = await fetch("/api/v1/subscriptions");
        if (!res.ok) {
          throw new Error(`Failed to fetch subscriptions: ${res.statusText}`);
        }
        const data = await res.json();
        setSubscriptions(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchSubscriptions();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-4">
        <AlertCircle className="w-16 h-16 text-red-500" />
        <h2 className="text-2xl font-bold text-white">Error Loading Subscriptions</h2>
        <p className="text-gray-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Subscriptions</h1>
          <p className="text-gray-400 mt-2">Manage recurring billing and subscriptions.</p>
        </div>
      </div>

      <div className="glass-card rounded-2xl overflow-hidden border border-white/5">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5 border-b border-white/5">
              <th className="p-4 font-semibold text-gray-300">Sub ID</th>
              <th className="p-4 font-semibold text-gray-300">Customer</th>
              <th className="p-4 font-semibold text-gray-300">Plan ID</th>
              <th className="p-4 font-semibold text-gray-300">Next Billing</th>
              <th className="p-4 font-semibold text-gray-300">Status</th>
              <th className="p-4 font-semibold text-gray-300">Failures</th>
            </tr>
          </thead>
          <tbody>
            {subscriptions.length === 0 ? (
              <tr>
                <td colSpan={6} className="p-8 text-center text-gray-500">
                  No subscriptions found
                </td>
              </tr>
            ) : (
              subscriptions.map((sub) => (
                <tr key={sub.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                  <td className="p-4 font-mono text-sm text-gray-300">{sub.id}</td>
                  <td className="p-4 font-mono text-sm text-gray-400">{sub.customer_id}</td>
                  <td className="p-4 text-gray-400">{sub.plan_id}</td>
                  <td className="p-4 text-gray-400">
                    {sub.next_billing_at ? new Date(sub.next_billing_at).toLocaleDateString() : 'N/A'}
                  </td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                      sub.status === 'halted' || sub.status === 'cancelled' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 
                      sub.status === 'active' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 
                      'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                    }`}>
                      {sub.status}
                    </span>
                  </td>
                  <td className="p-4 text-sm font-medium">
                    {sub.failure_count > 0 ? (
                      <span className="text-amber-400">{sub.failure_count} retries</span>
                    ) : (
                      <span className="text-gray-500">-</span>
                    )}
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
