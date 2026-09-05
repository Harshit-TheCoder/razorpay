"use client";

import { useEffect, useState } from "react";
import { Settings, Save, AlertCircle } from "lucide-react";

export default function PoliciesPage() {
  const [policy, setPolicy] = useState({
    max_retries: 2,
    max_transaction_amount: 10000,
    max_contacts: 3,
    recovery_window_days: 7,
    require_human_approval: false
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  
  const merchantId = "demo_merchant"; // Hardcoded for demo

  useEffect(() => {
    fetchPolicy();
  }, []);

  async function fetchPolicy() {
    try {
      const res = await fetch(`/api/v1/merchants/${merchantId}/policies`);
      if (res.ok) {
        const data = await res.json();
        setPolicy(data);
      }
    } catch (err) {
      console.error("Failed to fetch policy", err);
    } finally {
      setLoading(false);
    }
  }

  async function savePolicy(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      const res = await fetch(`/api/v1/merchants/${merchantId}/policies`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(policy)
      });
      if (res.ok) {
        setMessage("Settings saved successfully!");
        setTimeout(() => setMessage(""), 3000);
      } else {
        setMessage("Failed to save settings.");
      }
    } catch (err) {
      setMessage("Error saving settings.");
    } finally {
      setSaving(false);
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
    <div className="max-w-4xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div>
        <h1 className="text-3xl font-bold text-white flex items-center">
          <Settings className="w-8 h-8 mr-3 text-indigo-400" />
          Policy Configuration
        </h1>
        <p className="text-gray-400 mt-2">Configure merchant-level guardrails for the AI agent.</p>
      </div>

      <div className="glass-card rounded-2xl p-8 border border-white/5">
        <form onSubmit={savePolicy} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">Max Retries</label>
              <input 
                type="number" 
                value={policy.max_retries}
                onChange={(e) => setPolicy({...policy, max_retries: parseInt(e.target.value)})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500 transition-colors"
              />
              <p className="text-xs text-gray-500">Maximum number of automated recovery attempts per case.</p>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">Max Transaction Amount (₹)</label>
              <input 
                type="number" 
                value={policy.max_transaction_amount}
                onChange={(e) => setPolicy({...policy, max_transaction_amount: parseInt(e.target.value)})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500 transition-colors"
              />
              <p className="text-xs text-gray-500">Escalate if the pending amount exceeds this value.</p>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">Max Customer Contacts</label>
              <input 
                type="number" 
                value={policy.max_contacts}
                onChange={(e) => setPolicy({...policy, max_contacts: parseInt(e.target.value)})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500 transition-colors"
              />
              <p className="text-xs text-gray-500">Maximum number of times to contact a customer per case.</p>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">Recovery Window (Days)</label>
              <input 
                type="number" 
                value={policy.recovery_window_days}
                onChange={(e) => setPolicy({...policy, recovery_window_days: parseInt(e.target.value)})}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-indigo-500 transition-colors"
              />
              <p className="text-xs text-gray-500">Automatically fail cases open longer than this window.</p>
            </div>
          </div>

          <div className="pt-4 border-t border-white/5 flex items-center justify-between">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input 
                type="checkbox" 
                checked={policy.require_human_approval}
                onChange={(e) => setPolicy({...policy, require_human_approval: e.target.checked})}
                className="form-checkbox h-5 w-5 text-indigo-500 bg-white/5 border-white/10 rounded focus:ring-indigo-500 focus:ring-offset-gray-900"
              />
              <span className="text-gray-300 font-medium">Require Human Approval for All Actions</span>
            </label>
            <div className="text-sm text-gray-500 flex items-center">
               <AlertCircle className="w-4 h-4 mr-1" /> Overrides all other limits.
            </div>
          </div>

          <div className="pt-6 flex items-center space-x-4">
            <button 
              type="submit" 
              disabled={saving}
              className="flex items-center px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              <Save className="w-4 h-4 mr-2" />
              {saving ? "Saving..." : "Save Policies"}
            </button>
            {message && (
              <span className={`text-sm ${message.includes("Error") || message.includes("Failed") ? "text-red-400" : "text-emerald-400"}`}>
                {message}
              </span>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
