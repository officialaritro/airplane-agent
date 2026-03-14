"use client";

import { useState } from "react";
import Link from "next/link";

interface CompensationResult {
  eligible: boolean;
  amount: number;
  reason: string;
}

export default function Calculator() {
  const [distance, setDistance] = useState<number>(0);
  const [delay, setDelay] = useState<number>(0);
  const [result, setResult] = useState<CompensationResult | null>(null);

  const calculate = () => {
    const delayHours = delay / 60;
    let eligible = false;
    let amount = 0;
    let reason = "";

    if (delayHours < 2) {
      reason = "Delay is under 2 hours";
    } else if (distance <= 1500) {
      if (delayHours >= 2) {
        eligible = true;
        amount = delayHours >= 3 ? 300 : 150;
        reason = delayHours >= 3 ? "Delay 3+ hours (short-haul)" : "Delay 2-3 hours (short-haul)";
      }
    } else if (distance <= 3500) {
      if (delayHours >= 3) {
        eligible = true;
        amount = delayHours >= 4 ? 400 : 200;
        reason = delayHours >= 4 ? "Delay 4+ hours (medium-haul)" : "Delay 3-4 hours (medium-haul)";
      } else {
        reason = "Delay under 3 hours (medium-haul)";
      }
    } else {
      if (delayHours >= 4) {
        eligible = true;
        amount = delayHours >= 4 ? 600 : 300;
        reason = "Delay 4+ hours (long-haul)";
      } else {
        reason = "Delay under 4 hours (long-haul)";
      }
    }

    setResult({ eligible, amount, reason });
  };

  return (
    <div className="min-h-screen bg-card">
      <header className="border-b bg-white">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">Reroute</h1>
          <nav className="flex gap-6">
            <Link href="/" className="hover:text-primary transition">Home</Link>
            <Link href="/dashboard" className="hover:text-primary transition">Dashboard</Link>
          </nav>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold mb-4">Flight Delay Compensation Calculator</h1>
        <p className="text-secondary mb-8">
          Calculate your compensation under EC 261/2004 for EU flight delays.
        </p>

        <div className="bg-white rounded-xl p-6 shadow-sm border">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Flight Distance (km)
              </label>
              <input
                type="number"
                value={distance}
                onChange={(e) => setDistance(Number(e.target.value))}
                className="w-full px-4 py-2 border rounded-lg"
                placeholder="e.g., 1200"
              />
              <p className="text-sm text-secondary mt-1">
                Short-haul: ≤1500km | Medium-haul: 1501-3500km | Long-haul: &gt;3500km
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Delay Duration (minutes)
              </label>
              <input
                type="number"
                value={delay}
                onChange={(e) => setDelay(Number(e.target.value))}
                className="w-full px-4 py-2 border rounded-lg"
                placeholder="e.g., 180"
              />
            </div>

            <button
              onClick={calculate}
              className="w-full py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition font-medium"
            >
              Calculate Compensation
            </button>
          </div>

          {result && (
            <div className={`mt-6 p-4 rounded-lg ${result.eligible ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border'}`}>
              {result.eligible ? (
                <>
                  <p className="text-green-600 font-bold text-lg">
                    €{result.amount} Compensation
                  </p>
                  <p className="text-green-600 text-sm mt-1">{result.reason}</p>
                </>
              ) : (
                <>
                  <p className="text-secondary font-medium">No Compensation Due</p>
                  <p className="text-secondary text-sm mt-1">{result.reason}</p>
                </>
              )}
            </div>
          )}
        </div>

        <p className="text-sm text-secondary mt-6 text-center">
          This calculator provides estimates under EC 261/2004. Actual compensation may vary.
        </p>
      </main>
    </div>
  );
}
