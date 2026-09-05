"use client";

import { useEffect, useState } from "react";
import { CreditCard, AlertCircle } from "lucide-react";

export default function PaymentsPage() {
  const [payments, setPayments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchPayments() {
      try {
        const res = await fetch("/api/v1/payments");
        if (!res.ok) {
          throw new Error(`Failed to fetch payments: ${res.statusText}`);
        }
        const data = await res.json();
        setPayments(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchPayments();
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
        <h2 className="text-2xl font-bold text-white">Error Loading Payments</h2>
        <p className="text-gray-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Payments</h1>
          <p className="text-gray-400 mt-2">Monitor all payments and transaction states.</p>
        </div>
      </div>

      <div className="glass-card rounded-2xl overflow-hidden border border-white/5">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5 border-b border-white/5">
              <th className="p-4 font-semibold text-gray-300">Payment ID</th>
              <th className="p-4 font-semibold text-gray-300">Merchant</th>
              <th className="p-4 font-semibold text-gray-300">Order ID</th>
              <th className="p-4 font-semibold text-gray-300">Razorpay Ref</th>
              <th className="p-4 font-semibold text-gray-300">Status</th>
              <th className="p-4 font-semibold text-gray-300">Error Code</th>
            </tr>
          </thead>
          <tbody>
            {payments.length === 0 ? (
              <tr>
                <td colSpan={6} className="p-8 text-center text-gray-500">
                  No payments found
                </td>
              </tr>
            ) : (
              payments.map((payment) => (
                <tr key={payment.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                  <td className="p-4 font-mono text-sm text-gray-300">{payment.id}</td>
                  <td className="p-4 text-gray-400">{payment.merchant_id}</td>
                  <td className="p-4 font-mono text-sm text-gray-400">{payment.order_id || 'N/A'}</td>
                  <td className="p-4 font-mono text-sm text-gray-400">{payment.razorpay_payment_id}</td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                      payment.status === 'failed' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 
                      payment.status === 'captured' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 
                      'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                    }`}>
                      {payment.status}
                    </span>
                  </td>
                  <td className="p-4 text-sm text-red-400">{payment.error_code || '-'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
