export type Session = {
  authenticated: boolean;
  username?: string | null;
};

export type MutationResult = {
  status: "applied" | "failed" | "verification_failed";
  detail: string;
};

export type Account = {
  email: string;
};

export type Alias = {
  address: string;
  target: string;
};

export type Quota = {
  email: string;
  quota: string;
};

export type RelayDomain = {
  domain: string;
  host?: string | null;
  port?: number | null;
  excluded: boolean;
};

export type RelayAuth = {
  domain: string;
  username: string;
};

export type RelayState = {
  domains: RelayDomain[];
  auth: RelayAuth[];
};

export type SystemState = {
  dms_container_name: string;
  dms_reachable: boolean;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function fetchSession(): Promise<Session> {
  return request<Session>("/auth/session");
}

export async function login(username: string, password: string): Promise<Session> {
  return request<Session>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export async function logout(): Promise<Session> {
  return request<Session>("/auth/logout", {
    method: "POST",
  });
}

export async function fetchAccounts(): Promise<Account[]> {
  return request<Account[]>("/accounts");
}

export async function createAccount(email: string, password: string): Promise<MutationResult> {
  return request<MutationResult>("/accounts", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function updatePassword(email: string, password: string): Promise<MutationResult> {
  return request<MutationResult>(`/accounts/${encodeURIComponent(email)}/password`, {
    method: "POST",
    body: JSON.stringify({ password }),
  });
}

export async function deleteAccount(email: string): Promise<MutationResult> {
  return request<MutationResult>(`/accounts/${encodeURIComponent(email)}`, {
    method: "DELETE",
  });
}

export async function fetchAliases(): Promise<Alias[]> {
  return request<Alias[]>("/aliases");
}

export async function createAlias(address: string, target: string): Promise<MutationResult> {
  return request<MutationResult>("/aliases", {
    method: "POST",
    body: JSON.stringify({ address, target }),
  });
}

export async function deleteAlias(address: string, target: string): Promise<MutationResult> {
  return request<MutationResult>(
    `/aliases/${encodeURIComponent(address)}?target=${encodeURIComponent(target)}`,
    {
      method: "DELETE",
    },
  );
}

export async function fetchQuotas(): Promise<Quota[]> {
  return request<Quota[]>("/quotas");
}

export async function setQuota(email: string, quota: string): Promise<MutationResult> {
  return request<MutationResult>("/quotas", {
    method: "POST",
    body: JSON.stringify({ email, quota }),
  });
}

export async function deleteQuota(email: string): Promise<MutationResult> {
  return request<MutationResult>(`/quotas/${encodeURIComponent(email)}`, {
    method: "DELETE",
  });
}

export async function fetchRelayState(): Promise<RelayState> {
  return request<RelayState>("/relay");
}

export async function addRelayDomain(
  domain: string,
  host: string,
  port?: number,
): Promise<MutationResult> {
  return request<MutationResult>("/relay/domains", {
    method: "POST",
    body: JSON.stringify({ domain, host, port }),
  });
}

export async function excludeRelayDomain(domain: string): Promise<MutationResult> {
  return request<MutationResult>("/relay/domains/exclude", {
    method: "POST",
    body: JSON.stringify({ domain }),
  });
}

export async function addRelayAuth(
  domain: string,
  username: string,
  password: string,
): Promise<MutationResult> {
  return request<MutationResult>("/relay/auth", {
    method: "POST",
    body: JSON.stringify({ domain, username, password }),
  });
}

export async function fetchSystemState(): Promise<SystemState> {
  return request<SystemState>("/system/status");
}
