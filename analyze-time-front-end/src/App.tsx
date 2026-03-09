import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Activity, Clock3, Database, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { getMetrics, type MetricsResponse, queryDatabase } from "@/lib/api";

const navItems = ["Overview"];

function App() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);

  useEffect(() => {
    let mounted = true;
    getMetrics()
      .then((data) => {
        if (mounted) {
          setMetrics(data);
        }
      })
      .catch(() => {
        if (mounted) {
          setMetrics(null);
        }
      });

    return () => {
      mounted = false;
    };
  }, []);

  const stats = useMemo(
    () => [
      {
        label: "Queries Processed",
        value: metrics ? metrics.queries_processed.toLocaleString() : "N/A",
        icon: Database,
      },
      {
        label: "Avg Response Time",
        value: metrics ? `${metrics.avg_response_time_ms.toFixed(0)}ms` : "N/A",
        icon: Clock3,
      },
      {
        label: "System Health",
        value: metrics ? metrics.system_health : "N/A",
        icon: Activity,
      },
    ],
    [metrics]
  );

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setResponse(null);
    setLoading(true);

    try {
      const data = await queryDatabase(query.trim(), topK);
      setResponse(data.response);
      const refreshedMetrics = await getMetrics();
      setMetrics(refreshedMetrics);
    } catch (err) {
      const message = err instanceof Error ? err.message : "An unexpected error occurred";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-border/80 bg-background/70 backdrop-blur-md">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/20 text-primary">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Time Analyzer</p>
              <p className="text-base font-semibold">AI Intelligence Hub</p>
            </div>
          </div>
          <div className="hidden items-center gap-2 md:flex">
            {navItems.map((item) => (
              <button
                key={item}
                className="rounded-lg px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                type="button"
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      </header>

      <div className="container py-6 lg:py-10">
        <div className="grid gap-6 lg:grid-cols-[240px_1fr]">
          <aside className="hidden h-fit rounded-2xl border border-border/80 bg-card/60 p-4 backdrop-blur-sm lg:sticky lg:top-24 lg:block">
            <p className="mb-4 text-xs uppercase tracking-[0.18em] text-muted-foreground">Workspace</p>
            <div className="space-y-1">
              {navItems.map((item, idx) => (
                <button
                  key={item}
                  type="button"
                  className={`w-full rounded-lg px-3 py-2 text-left text-sm transition-all ${
                    idx === 0
                      ? "bg-primary/15 text-primary"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
          </aside>

          <main className="space-y-6">
            <motion.section
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45 }}
              className="space-y-3"
            >
              <p className="text-xs uppercase tracking-[0.2em] text-primary">Product Analytics</p>
              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Modern Time Intelligence Dashboard</h1>
              <p className="max-w-2xl text-sm text-muted-foreground sm:text-base">
                Query your time-tracking corpus in real time with a premium, low-friction interface tailored for fast analysis.
              </p>
            </motion.section>

            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 * index, duration: 0.4 }}
                  className="xl:col-span-1"
                >
                  <Card className="h-full hover:-translate-y-1">
                    <CardContent className="p-5">
                      <div className="mb-3 inline-flex rounded-lg bg-primary/15 p-2 text-primary">
                        <stat.icon className="h-4 w-4" />
                      </div>
                      <p className="text-2xl font-bold tracking-tight">{stat.value}</p>
                      <p className="text-sm text-muted-foreground">{stat.label}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.45 }}
                className="sm:col-span-2 xl:col-span-3"
              >
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle>Ask Your Time Data</CardTitle>
                    <CardDescription>Natural-language retrieval from your indexed records.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <form className="space-y-4" onSubmit={handleSubmit}>
                      <div className="grid gap-3 sm:grid-cols-[1fr_140px]">
                        <Input
                          required
                          value={query}
                          onChange={(e) => setQuery(e.target.value)}
                          placeholder="What did I spend most time on last week?"
                        />
                        <Input
                          type="number"
                          value={topK}
                          min={1}
                          max={20}
                          onChange={(e) => setTopK(Number(e.target.value) || 1)}
                          className="text-center"
                          aria-label="Top K"
                        />
                      </div>
                      <Button type="submit" disabled={loading} className="w-full sm:w-auto">
                        {loading ? "Analyzing..." : "Run Analysis"}
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25, duration: 0.45 }}
                className="sm:col-span-2 xl:col-span-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle>Result Stream</CardTitle>
                    <CardDescription>Response payload from the query endpoint.</CardDescription>
                  </CardHeader>
                  <CardContent>
                    {error ? (
                      <p className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">{error}</p>
                    ) : null}
                    <div className="min-h-40 rounded-xl border border-border/80 bg-background/50 p-4">
                      <pre className="whitespace-pre-wrap text-sm text-muted-foreground">
                        {response ?? "Submit a query to view intelligent results here."}
                      </pre>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </section>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
