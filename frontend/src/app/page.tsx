import {
  getOpenDetentionCasesSummary,
  getRevenueLossSummary,
  getTopDelayedFacilities,
} from "@/lib/api";

function money(value: string) {
  return `$${Number(value).toFixed(2)}`;
}

export default async function HomePage() {
  const [openSummary, revenueSummary, topFacilities] = await Promise.all([
    getOpenDetentionCasesSummary(),
    getRevenueLossSummary(),
    getTopDelayedFacilities(),
  ]);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="mb-8">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
            Detiviq
          </p>
          <h1 className="mt-2 text-4xl font-semibold">Operations Dashboard</h1>
          <p className="mt-3 max-w-2xl text-slate-300">
            Backend-first fleet operations visibility for detention tracking,
            delay analytics, and revenue-loss monitoring.
          </p>
        </div>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">Open detention cases</p>
            <p className="mt-2 text-3xl font-semibold">
              {openSummary.open_case_count}
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">Total revenue loss</p>
            <p className="mt-2 text-3xl font-semibold">
              {money(revenueSummary.total_amount)}
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">Average open amount</p>
            <p className="mt-2 text-3xl font-semibold">
              {money(openSummary.avg_open_amount)}
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <div className="mb-4">
            <h2 className="text-xl font-semibold">Revenue snapshot</h2>
            <p className="mt-1 text-sm text-slate-400">
              Summary generated from detention cases computed by the backend.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl bg-slate-950 p-4">
              <p className="text-sm text-slate-400">Total cases</p>
              <p className="mt-2 text-2xl font-semibold">
                {revenueSummary.total_cases}
              </p>
            </div>

            <div className="rounded-xl bg-slate-950 p-4">
              <p className="text-sm text-slate-400">Closed cases</p>
              <p className="mt-2 text-2xl font-semibold">
                {revenueSummary.closed_case_count}
              </p>
            </div>

            <div className="rounded-xl bg-slate-950 p-4">
              <p className="text-sm text-slate-400">Average case amount</p>
              <p className="mt-2 text-2xl font-semibold">
                {money(revenueSummary.avg_amount)}
              </p>
            </div>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-5">
          <div className="mb-4">
            <h2 className="text-xl font-semibold">Top delayed facilities</h2>
            <p className="mt-1 text-sm text-slate-400">
              Facilities ranked by dwell impact and detention amount.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="text-left text-slate-400">
                <tr className="border-b border-slate-800">
                  <th className="px-3 py-3 font-medium">Facility</th>
                  <th className="px-3 py-3 font-medium">Stops</th>
                  <th className="px-3 py-3 font-medium">Avg dwell (min)</th>
                  <th className="px-3 py-3 font-medium">Total amount</th>
                </tr>
              </thead>
              <tbody>
                {topFacilities.map((facility) => (
                  <tr
                    key={facility.facility_id}
                    className="border-b border-slate-800 last:border-0"
                  >
                    <td className="px-3 py-3">{facility.facility_name}</td>
                    <td className="px-3 py-3">{facility.stop_count}</td>
                    <td className="px-3 py-3">
                      {Number(facility.avg_dwell_minutes).toFixed(0)}
                    </td>
                    <td className="px-3 py-3">
                      {money(facility.total_amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  );
}
