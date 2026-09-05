import Link from 'next/link';
import { LayoutDashboard, BriefcaseBusiness, Settings, CreditCard, RefreshCcw, AlertTriangle } from 'lucide-react';

export default function Sidebar() {
  return (
    <div className="w-64 h-screen fixed left-0 top-0 glass-panel flex flex-col pt-8">
      <div className="px-6 mb-12">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-emerald-400">
          RazorAI
        </h1>
        <p className="text-xs text-gray-400 uppercase tracking-widest mt-1">Recovery Controller</p>
      </div>

      <nav className="flex-1 px-4 space-y-2">
        <Link 
          href="/" 
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-indigo-500/10 hover:border hover:border-indigo-500/20 transition-all group"
        >
          <LayoutDashboard className="w-5 h-5 group-hover:text-indigo-400 transition-colors" />
          <span className="font-medium">Dashboard</span>
        </Link>
        <Link 
          href="/cases" 
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-indigo-500/10 hover:border hover:border-indigo-500/20 transition-all group"
        >
          <BriefcaseBusiness className="w-5 h-5 group-hover:text-indigo-400 transition-colors" />
          <span className="font-medium">Recovery Cases</span>
        </Link>
        <Link 
          href="/payments" 
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-indigo-500/10 hover:border hover:border-indigo-500/20 transition-all group"
        >
          <CreditCard className="w-5 h-5 group-hover:text-indigo-400 transition-colors" />
          <span className="font-medium">Payments</span>
        </Link>
        <Link 
          href="/subscriptions" 
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-indigo-500/10 hover:border hover:border-indigo-500/20 transition-all group"
        >
          <RefreshCcw className="w-5 h-5 group-hover:text-indigo-400 transition-colors" />
          <span className="font-medium">Subscriptions</span>
        </Link>
        <Link 
          href="/escalations" 
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-amber-500/70 hover:text-amber-400 hover:bg-amber-500/10 hover:border hover:border-amber-500/20 transition-all group"
        >
          <AlertTriangle className="w-5 h-5 group-hover:text-amber-400 transition-colors" />
          <span className="font-medium">Review Queue</span>
        </Link>
      </nav>

      <div className="p-4 mb-4">
        <Link href="/policies" className="px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all flex items-center space-x-3 cursor-pointer group">
          <Settings className="w-5 h-5 group-hover:text-gray-300 transition-colors" />
          <span className="font-medium">Settings</span>
        </Link>
      </div>
    </div>
  );
}
