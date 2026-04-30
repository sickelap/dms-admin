import { useEffect, useState } from "react";
import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";

import {
  addRelayAuth,
  addRelayDomain,
  createAccount,
  createAlias,
  deleteAccount,
  deleteAlias,
  deleteQuota,
  excludeRelayDomain,
  fetchAccounts,
  fetchAliases,
  fetchQuotas,
  fetchRelayState,
  fetchSession,
  fetchSystemState,
  login,
  logout,
  setQuota,
  updatePassword,
  type Account,
  type Alias,
  type Quota,
  type RelayState,
  type Session,
  type SystemState,
} from "./api";

function PanelHeader({
  title,
  description,
  onRefresh,
}: {
  title: string;
  description: string;
  onRefresh: () => Promise<void>;
}) {
  return (
    <header className="page-header">
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <button className="secondary" onClick={() => void onRefresh()}>
        Refresh
      </button>
    </header>
  );
}

function ResultBanner({ message }: { message: string | null }) {
  if (!message) {
    return null;
  }

  return <p className="result-banner">{message}</p>;
}

function LoginForm({ onAuthenticated }: { onAuthenticated: (session: Session) => void }) {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    try {
      const session = await login(username, password);
      onAuthenticated(session);
    } catch {
      setError("Login failed");
    }
  }

  return (
    <main className="auth-layout">
      <form className="panel auth-card" onSubmit={handleSubmit}>
        <h1>DMS Admin</h1>
        <p>Authenticate to manage the running Docker Mail Server instance.</p>
        <label>
          <span>Username</span>
          <input value={username} onChange={(event) => setUsername(event.target.value)} />
        </label>
        <label>
          <span>Password</span>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        {error ? <p className="error">{error}</p> : null}
        <button type="submit">Sign in</button>
      </form>
    </main>
  );
}

function AccountsPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordReset, setPasswordReset] = useState<Record<string, string>>({});

  async function load() {
    setAccounts(await fetchAccounts());
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="panel page">
      <PanelHeader
        title="Accounts"
        description="Create, remove, and reset mail accounts through DMS setup."
        onRefresh={load}
      />
      <ResultBanner message={message} />
      <form
        className="inline-form"
        onSubmit={async (event) => {
          event.preventDefault();
          const result = await createAccount(email, password);
          setMessage(result.detail);
          setEmail("");
          setPassword("");
          await load();
        }}
      >
        <input
          placeholder="user@example.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <button type="submit">Create account</button>
      </form>
      <ul className="resource-list">
        {accounts.map((account) => (
          <li key={account.email} className="resource-item">
            <div>
              <strong>{account.email}</strong>
              <p>Deleting an account may also remove aliases and quota in DMS.</p>
            </div>
            <div className="actions">
              <input
                placeholder="New password"
                type="password"
                value={passwordReset[account.email] ?? ""}
                onChange={(event) =>
                  setPasswordReset((current) => ({ ...current, [account.email]: event.target.value }))
                }
              />
              <button
                className="secondary"
                onClick={async () => {
                  const result = await updatePassword(account.email, passwordReset[account.email] ?? "");
                  setMessage(result.detail);
                  setPasswordReset((current) => ({ ...current, [account.email]: "" }));
                }}
              >
                Reset password
              </button>
              <button
                className="danger"
                onClick={async () => {
                  const result = await deleteAccount(account.email);
                  setMessage(result.detail);
                  await load();
                }}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

function AliasesPage() {
  const [aliases, setAliases] = useState<Alias[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [address, setAddress] = useState("");
  const [target, setTarget] = useState("");

  async function load() {
    setAliases(await fetchAliases());
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="panel page">
      <PanelHeader
        title="Aliases"
        description="Manage alias mappings backed by the DMS setup CLI."
        onRefresh={load}
      />
      <ResultBanner message={message} />
      <form
        className="inline-form"
        onSubmit={async (event) => {
          event.preventDefault();
          const result = await createAlias(address, target);
          setMessage(result.detail);
          setAddress("");
          setTarget("");
          await load();
        }}
      >
        <input
          placeholder="alias@example.com"
          value={address}
          onChange={(event) => setAddress(event.target.value)}
        />
        <input
          placeholder="target@example.com"
          value={target}
          onChange={(event) => setTarget(event.target.value)}
        />
        <button type="submit">Create alias</button>
      </form>
      <ul className="resource-list">
        {aliases.map((alias) => (
          <li key={`${alias.address}:${alias.target}`} className="resource-item">
            <div>
              <strong>{alias.address}</strong>
              <p>{alias.target}</p>
            </div>
            <button
              className="danger"
              onClick={async () => {
                const result = await deleteAlias(alias.address, alias.target);
                setMessage(result.detail);
                await load();
              }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

function QuotasPage() {
  const [quotas, setQuotas] = useState<Quota[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [quota, setQuotaValue] = useState("");

  async function load() {
    setQuotas(await fetchQuotas());
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="panel page">
      <PanelHeader
        title="Quotas"
        description="Read and update quota state directly from the running mail server."
        onRefresh={load}
      />
      <ResultBanner message={message} />
      <form
        className="inline-form"
        onSubmit={async (event) => {
          event.preventDefault();
          const result = await setQuota(email, quota);
          setMessage(result.detail);
          setEmail("");
          setQuotaValue("");
          await load();
        }}
      >
        <input
          placeholder="user@example.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <input
          placeholder="10 G"
          value={quota}
          onChange={(event) => setQuotaValue(event.target.value)}
        />
        <button type="submit">Set quota</button>
      </form>
      <ul className="resource-list">
        {quotas.map((entry) => (
          <li key={entry.email} className="resource-item">
            <div>
              <strong>{entry.email}</strong>
              <p>{entry.quota}</p>
            </div>
            <button
              className="danger"
              onClick={async () => {
                const result = await deleteQuota(entry.email);
                setMessage(result.detail);
                await load();
              }}
            >
              Remove quota
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

function RelayPage() {
  const [relay, setRelay] = useState<RelayState>({ domains: [], auth: [] });
  const [message, setMessage] = useState<string | null>(null);
  const [domain, setDomain] = useState("");
  const [host, setHost] = useState("");
  const [port, setPort] = useState("587");
  const [authDomain, setAuthDomain] = useState("");
  const [authUser, setAuthUser] = useState("");
  const [authPassword, setAuthPassword] = useState("");

  async function load() {
    setRelay(await fetchRelayState());
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="panel page">
      <PanelHeader
        title="Relay"
        description="Manage setup-backed relay domain mappings and relay authentication."
        onRefresh={load}
      />
      <ResultBanner message={message} />
      <form
        className="inline-form"
        onSubmit={async (event) => {
          event.preventDefault();
          const parsedPort = port ? Number(port) : undefined;
          const result = await addRelayDomain(domain, host, parsedPort);
          setMessage(result.detail);
          setDomain("");
          setHost("");
          setPort("587");
          await load();
        }}
      >
        <input
          placeholder="example.com"
          value={domain}
          onChange={(event) => setDomain(event.target.value)}
        />
        <input
          placeholder="smtp.example.com"
          value={host}
          onChange={(event) => setHost(event.target.value)}
        />
        <input placeholder="587" value={port} onChange={(event) => setPort(event.target.value)} />
        <button type="submit">Add relay domain</button>
      </form>
      <form
        className="inline-form"
        onSubmit={async (event) => {
          event.preventDefault();
          const result = await addRelayAuth(authDomain, authUser, authPassword);
          setMessage(result.detail);
          setAuthDomain("");
          setAuthUser("");
          setAuthPassword("");
          await load();
        }}
      >
        <input
          placeholder="example.com"
          value={authDomain}
          onChange={(event) => setAuthDomain(event.target.value)}
        />
        <input
          placeholder="relay user"
          value={authUser}
          onChange={(event) => setAuthUser(event.target.value)}
        />
        <input
          placeholder="relay password"
          type="password"
          value={authPassword}
          onChange={(event) => setAuthPassword(event.target.value)}
        />
        <button type="submit">Add relay auth</button>
      </form>
      <div className="split-grid">
        <div>
          <h3>Relay domains</h3>
          <ul className="resource-list">
            {relay.domains.map((entry) => (
              <li key={`${entry.domain}:${entry.host ?? "excluded"}`} className="resource-item">
                <div>
                  <strong>{entry.domain}</strong>
                  <p>{entry.excluded ? "Excluded from default relay" : `${entry.host}:${entry.port ?? 25}`}</p>
                </div>
                {!entry.excluded ? (
                  <button
                    className="secondary"
                    onClick={async () => {
                      const result = await excludeRelayDomain(entry.domain);
                      setMessage(result.detail);
                      await load();
                    }}
                  >
                    Exclude
                  </button>
                ) : null}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Relay auth</h3>
          <ul className="resource-list">
            {relay.auth.map((entry) => (
              <li key={`${entry.domain}:${entry.username}`} className="resource-item">
                <div>
                  <strong>{entry.domain}</strong>
                  <p>{entry.username}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}

function SystemPage() {
  const [state, setState] = useState<SystemState | null>(null);

  async function load() {
    setState(await fetchSystemState());
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="panel page">
      <PanelHeader
        title="System"
        description="Read current DMS reachability and container targeting on demand."
        onRefresh={load}
      />
      {state ? (
        <dl className="status-grid">
          <div>
            <dt>Container</dt>
            <dd>{state.dms_container_name}</dd>
          </div>
          <div>
            <dt>DMS reachable</dt>
            <dd>{state.dms_reachable ? "Yes" : "No"}</dd>
          </div>
        </dl>
      ) : null}
    </section>
  );
}

function Layout({
  session,
  onLogout,
}: {
  session: Session;
  onLogout: () => Promise<void>;
}) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Connected operator</p>
          <strong>{session.username}</strong>
        </div>
        <nav>
          <NavLink to="/">Accounts</NavLink>
          <NavLink to="/aliases">Aliases</NavLink>
          <NavLink to="/quotas">Quotas</NavLink>
          <NavLink to="/relay">Relay</NavLink>
          <NavLink to="/system">System</NavLink>
        </nav>
        <button className="secondary" onClick={() => void onLogout()}>
          Sign out
        </button>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<AccountsPage />} />
          <Route path="/aliases" element={<AliasesPage />} />
          <Route path="/quotas" element={<QuotasPage />} />
          <Route path="/relay" element={<RelayPage />} />
          <Route path="/system" element={<SystemPage />} />
        </Routes>
      </main>
    </div>
  );
}

export function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    fetchSession()
      .then((result) => {
        setSession(result);
      })
      .catch(() => {
        setSession(null);
      })
      .finally(() => {
        setReady(true);
      });
  }, []);

  async function handleLogout() {
    await logout();
    setSession(null);
  }

  if (!ready) {
    return <main className="auth-layout">Loading…</main>;
  }

  if (!session?.authenticated) {
    return <LoginForm onAuthenticated={setSession} />;
  }

  return (
    <BrowserRouter>
      <Layout session={session} onLogout={handleLogout} />
    </BrowserRouter>
  );
}
