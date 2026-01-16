"use client";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0b0f14] flex items-center justify-center px-4">
      <div className="w-full max-w-6xl">
        <h1 className="text-3xl font-bold text-[#f5c16c] mb-6">
          My Tasks
        </h1>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-[#121821] rounded-xl p-6 border border-[#1f2937]">
            <p className="text-gray-400 text-sm">Total Tasks</p>
            <p className="text-2xl font-bold text-white mt-2">1</p>
          </div>

          <div className="bg-[#121821] rounded-xl p-6 border border-[#1f2937]">
            <p className="text-gray-400 text-sm">Completed</p>
            <p className="text-2xl font-bold text-green-400 mt-2">0</p>
          </div>

          <div className="bg-[#121821] rounded-xl p-6 border border-[#1f2937]">
            <p className="text-gray-400 text-sm">Pending</p>
            <p className="text-2xl font-bold text-orange-400 mt-2">1</p>
          </div>
        </div>

        {/* Task Card */}
        <div className="bg-[#121821] rounded-xl p-6 border border-[#1f2937]">
          <div className="flex items-center justify-between">
            <h2 className="text-white font-semibold">
              Meeting in office
            </h2>
            <span className="text-xs px-3 py-1 rounded-full bg-[#1f2937] text-[#f5c16c]">
              Normal
            </span>
          </div>
        </div>
      </div>
    </main>
  );
}
