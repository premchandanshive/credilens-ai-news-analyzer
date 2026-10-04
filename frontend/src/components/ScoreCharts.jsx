import { Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar } from 'recharts';

const COLORS = {
  supported: '#34d399',
  contradicted: '#f87171',
  insufficient: '#fbbf24',
  accent: '#7c5cff',
};

export function ComponentScoreChart({ scores }) {
  const s = scores || {};
  const data = [
    { name: 'AI', value: s.aiClassification ?? 0 },
    { name: 'Evidence', value: s.evidenceVerification ?? 0 },
    { name: 'Source', value: s.sourceAnalysis ?? 0 },
    { name: 'Language', value: s.languageAnalysis ?? 0 },
    { name: 'Claims', value: s.claimConsistency ?? 0 },
  ];
  const hasData = Object.values(s).some((v) => Number.isFinite(Number(v)));
  if (!hasData) return null;

  return (
    <section className="card-surface p-5">
      <h2 className="text-sm font-semibold mb-2">Component scores</h2>
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <XAxis dataKey="name" stroke="#8b95ad" fontSize={12} />
            <YAxis domain={[0, 100]} stroke="#8b95ad" fontSize={12} />
            <Tooltip />
            <Bar dataKey="value" fill={COLORS.accent} radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export function ClaimDistributionChart({ claims }) {
  const items = claims || [];
  if (!items.length) return null;
  const counts = {
    Supported: items.filter((c) => c.status === 'SUPPORTED').length,
    Contradicted: items.filter((c) => c.status === 'CONTRADICTED').length,
    Insufficient: items.filter((c) => c.status === 'INSUFFICIENT_EVIDENCE').length,
  };
  const data = Object.entries(counts).map(([name, value]) => ({ name, value }));
  const colors = [COLORS.supported, COLORS.contradicted, COLORS.insufficient];

  return (
    <section className="card-surface p-5">
      <h2 className="text-sm font-semibold mb-2">Claim verification distribution</h2>
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" innerRadius={40} outerRadius={70}>
              {data.map((entry, i) => (
                <Cell key={entry.name} fill={colors[i]} />
              ))}
            </Pie>
            <Legend />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export function HistoryTrendChart({ items }) {
  const rows = (items || [])
    .slice()
    .reverse()
    .map((item) => ({
      name: new Date(item.createdAt).toLocaleDateString(),
      score: item.credibilityScore,
    }))
    .filter((r) => Number.isFinite(r.score));
  if (rows.length < 2) return null;

  return (
    <section className="card-surface p-5">
      <h2 className="text-sm font-semibold mb-2">History trend</h2>
      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows}>
            <XAxis dataKey="name" stroke="#8b95ad" fontSize={11} />
            <YAxis domain={[0, 100]} stroke="#8b95ad" fontSize={11} />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke={COLORS.accent} strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
