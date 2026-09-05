"use client";

import { useEffect, useState } from "react";
import { Activity, Bell } from "lucide-react";
import Link from "next/link";

export default function LiveFeed() {
  const [events, setEvents] = useState<any[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Determine WS protocol based on current protocol
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    // In dev, assuming API is running on localhost:8000
    // But NEXT_PUBLIC_WS_BASE_URL might be defined in .env
    const wsUrl = process.env.NEXT_PUBLIC_WS_BASE_URL || "ws://localhost:8000/api/v1/live";
    
    const socket = new WebSocket(`${wsUrl}/agent-activity`);

    socket.onopen = () => {
      setConnected(true);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEvents((prev) => [data, ...prev].slice(0, 10)); // Keep last 10 events
    };

    socket.onclose = () => {
      setConnected(false);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="glass-card rounded-2xl p-6 border border-white/5 h-[400px] flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-bold text-white flex items-center text-lg">
          <Activity className="w-5 h-5 mr-2 text-emerald-400" />
          Live Agent Activity
        </h3>
        <div className="flex items-center">
          <span className="relative flex h-3 w-3 mr-2">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${connected ? 'bg-emerald-400' : 'bg-red-400'}`}></span>
            <span className={`relative inline-flex rounded-full h-3 w-3 ${connected ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
          </span>
          <span className="text-xs text-gray-400 font-medium uppercase tracking-wider">
            {connected ? 'Live' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-4 custom-scrollbar">
        {events.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-500">
            <Bell className="w-8 h-8 mb-2 opacity-50" />
            <p className="text-sm">Listening for agent actions...</p>
          </div>
        ) : (
          events.map((ev, i) => (
            <div key={i} className="bg-white/5 p-3 rounded-lg border border-white/5 animate-in fade-in slide-in-from-right-4">
              <div className="flex justify-between items-start mb-1">
                <span className="text-xs font-mono px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded">
                  {ev.action}
                </span>
                <span className="text-[10px] text-gray-500">
                  {new Date(ev.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className="text-sm text-gray-300 mt-2">
                Case: <Link href={`/cases/${ev.case_id}`} className="text-indigo-400 hover:underline">{ev.case_id}</Link>
              </div>
              <div className="text-xs text-emerald-400 mt-1 capitalize">
                Status: {ev.status}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
