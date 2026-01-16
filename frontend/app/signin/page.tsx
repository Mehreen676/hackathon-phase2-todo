"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState("test-user");
  const [loading, setLoading] = useState(false);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Fake auth (hackathon-friendly): store user id locally
    localStorage.setItem("todo_user_id", email.trim() || "test-user");

    setTimeout(() => {
      router.push("/dashboard");
    }, 300);
  };

  return (
    <main className="min-h-screen bg-[#0b0f14] flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-[#121821] border border-[#1f2937] rounded-2xl shadow-2xl p-8">
        <h1 className="text-3xl font-bold text-[#f5c16c]">Sign In</h1>
        <p className="text-gray-400 mt-2">
          Enter your email (or any name). Demo login for hackathon video.
        </p>

        <form onSubmit={onSubmit} className="mt-8 space-y-4">
          <div>
            <label className="text-sm text-gray-300">Email / Username</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-2 w-full rounded-xl bg-[#0b0f14] border border-[#1f2937] px-4 py-3 text-white outline-none focus:border-[#f5c16c]"
              placeholder="mehru@example.com"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl py-3 font-semibold text-black bg-[#f5c16c] hover:brightness-95 transition disabled:opacity-60"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>

          <p className="text-xs text-gray-500">
            * Hackathon demo auth: no real password required.
          </p>
        </form>
      </div>
    </main>
  );
}
