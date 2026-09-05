"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Clock, Activity, CheckCircle, ShieldAlert } from "lucide-react";
import Link from "next/link";

export default function CaseDetail() {
  const { id } = useParams();
  const router = useRouter();
  const [caseDetail, setCaseDetail] = useState<any>(null);
  const [sourceDetail, setSourceDetail] = useState<any>(null);
  const [attempts, setAttempts] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [decisions, setDecisions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    async function fetchCase() {
      try {
        const res = await fetch(`/api/v1/cases/${id}`);
        if (!res.ok) {
          if(res.status === 404) {
             console.log("Case not found");
          }
          throw new Error("Failed to fetch case");
        }
        const data = await res.json();
        setCaseDetail(data);

        // Fetch source, attempts, audit logs, and decisions concurrently
        const [sourceRes, attemptsRes, auditRes, decisionsRes] = await Promise.all([
          fetch(`/api/v1/cases/${id}/source`),
          fetch(`/api/v1/cases/${id}/attempts`),
          fetch(`/api/v1/audit/${id}`),
          fetch(`/api/v1/cases/${id}/decisions`)
        ]);

        if (sourceRes.ok) {
          const sourceData = await sourceRes.json();
          setSourceDetail(sourceData);
        }
        
        if (attemptsRes.ok) {
          const attemptsData = await attemptsRes.json();
          setAttempts(attemptsData);
        }

        if (auditRes.ok) {
          const auditData = await auditRes.json();
          setAuditLogs(auditData);
        }

        if (decisionsRes.ok) {
          const decisionsData = await decisionsRes.json();
          setDecisions(decisionsData);
        }
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }
    if (id) {
      fetchCase();
    }
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (!caseDetail) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] space-y-4">
        <ShieldAlert className="w-16 h-16 text-gray-500" />
        <h2 className="text-2xl font-bold text-white">Case Not Found</h2>
        <button onClick={() => router.back()} className="text-indigo-400 hover:underline">Go Back</button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <Link href="/cases" className="inline-flex items-center text-sm text-gray-400 hover:text-white transition-colors">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Cases
      </Link>

      <div className="glass-card p-8 rounded-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8">
          <span className={`px-4 py-2 rounded-full text-sm font-bold border ${
            caseDetail.state === 'RECOVERED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 
            caseDetail.state === 'FAILED' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 
            'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
          }`}>
            {caseDetail.state}
          </span>
        </div>

        <h1 className="text-3xl font-bold text-white mb-2">Case {caseDetail.id}</h1>
        <div className="flex items-center space-x-4 text-gray-400 mb-8">
          <div className="flex items-center">
            <Clock className="w-4 h-4 mr-1" /> 
            {new Date(caseDetail.opened_at).toLocaleString()}
          </div>
          <span>•</span>
          <div className="capitalize">{caseDetail.scenario_type.replace(/_/g, ' ')}</div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-black/20 rounded-xl p-5 border border-gray-800">
            <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-1">Merchant</h3>
            <p className="text-white font-mono">{caseDetail.merchant_id}</p>
          </div>
          <div className="bg-black/20 rounded-xl p-5 border border-gray-800">
            <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-1">Source Reference</h3>
            <p className="text-white font-mono">{caseDetail.source_ref}</p>
            {sourceDetail?.data && (
              <div className="mt-2 text-sm text-gray-400">
                {sourceDetail.type === 'payment' && `Order: ${sourceDetail.data.order_id || 'N/A'}`}
                {sourceDetail.type === 'subscription' && `Status: ${sourceDetail.data.status}`}
                {sourceDetail.type === 'checkout' && `Cart Value: ${sourceDetail.data.cart_snapshot?.items?.reduce((acc: any, item: any) => acc + item.price * item.qty, 0) || 0} ${sourceDetail.data.cart_snapshot?.currency || 'INR'}`}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="flex space-x-4 border-b border-white/10 mb-6 pb-2">
        <button 
          onClick={() => setActiveTab("overview")}
          className={`pb-2 px-2 text-sm font-medium transition-colors ${activeTab === 'overview' ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-gray-400 hover:text-white'}`}
        >
          Overview
        </button>
        <button 
          onClick={() => setActiveTab("agent")}
          className={`pb-2 px-2 text-sm font-medium transition-colors ${activeTab === 'agent' ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-gray-400 hover:text-white'}`}
        >
          Agent Decisions
        </button>
        <button 
          onClick={() => setActiveTab("audit")}
          className={`pb-2 px-2 text-sm font-medium transition-colors ${activeTab === 'audit' ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-gray-400 hover:text-white'}`}
        >
          Agent Audit Trail
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="glass-card p-8 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-indigo-400" />
            Recovery Interventions
          </h3>
          
          {/* Timeline representing real recovery attempts */}
          <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-700 before:to-transparent">
            
            {attempts.length === 0 ? (
              <div className="text-gray-500 text-center py-4">No recovery attempts logged yet.</div>
            ) : (
              attempts.map((attempt) => (
                <div key={attempt.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full border-4 border-[#0f111a] text-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 ${
                    attempt.status === 'COMPLETED' ? 'bg-emerald-500 shadow-[0_0_0_4px_rgba(16,185,129,0.2)]' : 
                    attempt.status === 'FAILED' ? 'bg-red-500 shadow-[0_0_0_4px_rgba(239,68,68,0.2)]' : 
                    'bg-indigo-500 shadow-[0_0_0_4px_rgba(99,102,241,0.2)]'
                  }`}>
                    {attempt.attempt_number}
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] glass-panel p-4 rounded-xl border border-gray-800 hover:border-gray-600 transition-colors">
                    <div className="flex justify-between items-baseline mb-1">
                      <h4 className="font-bold text-white capitalize">{attempt.action_type.replace(/_/g, ' ')}</h4>
                      <span className="text-xs text-gray-500">{new Date(attempt.executed_at).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center mt-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        attempt.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400' : 
                        attempt.status === 'FAILED' ? 'bg-red-500/10 text-red-400' : 
                        'bg-indigo-500/10 text-indigo-400'
                      }`}>
                        {attempt.status}
                      </span>
                      {attempt.result?.delivery_status && (
                        <span className="text-xs text-gray-400">
                          Delivery: {attempt.result.delivery_status}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'agent' && (
        <div className="glass-card p-8 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6 flex items-center">
            <Activity className="w-5 h-5 mr-2 text-indigo-400" />
            AI Agent Decision
          </h3>
          <div className="space-y-6">
            {decisions.length === 0 ? (
              <div className="text-gray-500 text-center py-4">No agent decisions available for this case.</div>
            ) : (
              decisions.map((decision, idx) => (
                <div key={idx} className="bg-black/30 border border-indigo-500/30 rounded-lg p-6 relative overflow-hidden">
                  <div className="absolute top-0 right-0 -mr-4 -mt-4 w-24 h-24 bg-indigo-500/10 rounded-full blur-2xl"></div>
                  
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">Proposed Action</h4>
                    <div className="inline-flex items-center px-3 py-1 rounded-md bg-indigo-500/20 text-indigo-300 font-mono text-sm border border-indigo-500/30">
                      {decision.action_type}
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">Rationale</h4>
                    <p className="text-gray-300 leading-relaxed bg-black/40 p-4 rounded-md border border-white/5">
                      {decision.rationale_text}
                    </p>
                  </div>
                  
                  {decision.payload && Object.keys(decision.payload).length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">Payload</h4>
                      <pre className="bg-black/50 p-4 rounded-md text-xs font-mono text-gray-400 overflow-x-auto border border-white/5">
                        {JSON.stringify(decision.payload, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'audit' && (
        <div className="glass-card p-8 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6 flex items-center">
            <ShieldAlert className="w-5 h-5 mr-2 text-indigo-400" />
            Immutable Audit Log
          </h3>
          <div className="space-y-4">
            {auditLogs.length === 0 ? (
              <div className="text-gray-500 text-center py-4">No audit logs available for this case.</div>
            ) : (
              auditLogs.map((log, idx) => (
                <div key={idx} className="bg-black/30 border border-white/5 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-3">
                    <div className="flex items-center space-x-3">
                      <span className="px-2 py-1 bg-white/10 text-white rounded text-xs font-mono">{log.action}</span>
                      <span className="text-xs text-gray-500">Actor: {log.actor}</span>
                    </div>
                    <span className="text-xs text-gray-400">{new Date(log.timestamp).toLocaleString()}</span>
                  </div>
                  
                  {(log.previous_state || log.new_state) && (
                    <div className="flex items-center space-x-2 text-sm text-gray-400 mb-3">
                      <span>State:</span>
                      <span className="px-2 py-0.5 bg-gray-800 rounded">{log.previous_state || 'none'}</span>
                      <span>→</span>
                      <span className="px-2 py-0.5 bg-gray-800 rounded text-white">{log.new_state}</span>
                    </div>
                  )}

                  {Object.keys(log.payload || {}).length > 0 && (
                    <div className="mt-3 bg-black/50 p-3 rounded text-xs font-mono text-gray-400 overflow-x-auto">
                      <pre>{JSON.stringify(log.payload, null, 2)}</pre>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
