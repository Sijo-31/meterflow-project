import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  PieChart, Pie, Cell, ResponsiveContainer
} from "recharts";

function App() {
  const [logs, setLogs] = useState([]);
  const [billing, setBilling] = useState({});
  const [analytics, setAnalytics] = useState({});

  const USER_ID = 1;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const logsRes = await fetch(`http://127.0.0.1:8000/logs/${USER_ID}`);
        const logsData = await logsRes.json();

        const billingRes = await fetch(`http://127.0.0.1:8000/billing/${USER_ID}`);
        const billingData = await billingRes.json();

        const analyticsRes = await fetch(`http://127.0.0.1:8000/analytics/${USER_ID}`);
        const analyticsData = await analyticsRes.json();

        setLogs(logsData);
        setBilling(billingData);
        setAnalytics(analyticsData);

      } catch (err) {
        console.error(err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  //GROUP BY MINUTE
  const grouped = {};

  logs.forEach((log) => {
    const date = new Date(log.timestamp);
    const time = `${date.getHours()}:${date.getMinutes()}`;

    if (!grouped[time]) grouped[time] = 0;
    grouped[time] += 1;
  });

  const chartData = Object.keys(grouped)
    .sort()
    .map((time) => ({
      time,
      requests: grouped[time]
    }));

  //PIE DATA
  const pieData = [
    { name: "Success", value: analytics.success || 0 },
    { name: "Failures", value: analytics.failures || 0 }
  ];

  return (
    <div style={container}>
      <h1 style={title}>🚀 MeterFlow Dashboard</h1>

      {/* 🔹 CARDS */}
      <div style={grid}>
        <Card title="Usage" value={`${billing.usage || 0} requests`} />
        <Card title="Billing" value={`₹ ${billing.cost || 0}`} />
        <Card title="Total Requests" value={analytics.total_requests || 0} />
        <Card title="Success" value={analytics.success || 0} />
        <Card title="Failures" value={analytics.failures || 0} />
        <Card title="Error Rate" value={`${analytics.error_rate || 0}%`} />
      </div>

      {/* REQUEST TREND */}
      <Section title="📈 Request Trends">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="requests"
              stroke="#4f46e5"
              strokeWidth={3}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Section>

      {/* PIE */}
      <Section title="📊 Success vs Failures">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              outerRadius={100}
              label
            >
              <Cell fill="#22c55e" />
              <Cell fill="#ef4444" />
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </Section>

      {/* LATENCY */}
      <Section title="⚡ Latency Trend">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={logs}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="id" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="latency"
              stroke="#f97316"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </Section>

      {/* TABLE */}
      <Section title="📜 API Logs">
        <table style={table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>API Key</th>
              <th>Time</th>
              <th>Latency</th>
              <th>Endpoint</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.api_key.slice(0, 8)}...</td>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
                <td>{log.latency} ms</td>
                <td>{log.endpoint}</td>
                <td style={{
                  color: log.status_code === 200 ? "#22c55e" : "#ef4444",
                  fontWeight: "bold"
                }}>
                  {log.status_code}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

/* COMPONENTS */

const Card = ({ title, value }) => (
  <div style={card}>
    <h4 style={{ color: "#6b7280" }}>{title}</h4>
    <h2>{value}</h2>
  </div>
);

const Section = ({ title, children }) => (
  <div style={section}>
    <h2 style={{ marginBottom: "15px" }}>{title}</h2>
    {children}
  </div>
);

/* STYLES */

const container = {
  padding: "30px",
  fontFamily: "Inter, sans-serif",
  background: "#f9fafb"
};

const title = {
  marginBottom: "20px"
};

const grid = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
  gap: "20px",
  marginBottom: "30px"
};

const card = {
  background: "white",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.05)"
};

const section = {
  background: "white",
  padding: "20px",
  borderRadius: "12px",
  marginBottom: "30px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.05)"
};

const table = {
  width: "100%",
  borderCollapse: "collapse"
};

export default App;