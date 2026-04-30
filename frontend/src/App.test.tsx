import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { App } from "./App";
import type { RelayState } from "./api";

type MockResponseBody =
  | Record<string, unknown>
  | Array<Record<string, unknown>>
  | Array<string>
  | string
  | null;

function jsonResponse(status: number, body: MockResponseBody): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function installMockApi() {
  const state: {
    loggedIn: boolean;
    accounts: Array<{ email: string }>;
    aliases: Array<{ address: string; target: string }>;
    quotas: Array<{ email: string; quota: string }>;
    relay: RelayState;
    system: { dms_container_name: string; dms_reachable: boolean };
  } = {
    loggedIn: false,
    accounts: [{ email: "hello@example.com" }],
    aliases: [{ address: "postmaster@example.com", target: "hello@example.com" }],
    quotas: [{ email: "hello@example.com", quota: "5 G" }],
    relay: {
      domains: [{ domain: "example.com", host: "smtp.example.com", port: 587, excluded: false }],
      auth: [{ domain: "example.com", username: "relay-user" }],
    },
    system: {
      dms_container_name: "mailserver",
      dms_reachable: true,
    },
  };

  const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = new URL(typeof input === "string" ? input : input.toString());
    const path = `${url.pathname}${url.search}`;
    const method = init?.method ?? "GET";
    const body = init?.body ? JSON.parse(String(init.body)) : null;

    if (path === "/api/auth/session") {
      if (!state.loggedIn) {
        return jsonResponse(401, { detail: "Authentication required" });
      }
      return jsonResponse(200, { authenticated: true, username: "admin" });
    }

    if (path === "/api/auth/login" && method === "POST") {
      state.loggedIn = true;
      return jsonResponse(200, { authenticated: true, username: body.username });
    }

    if (path === "/api/auth/logout" && method === "POST") {
      state.loggedIn = false;
      return jsonResponse(200, { authenticated: false });
    }

    if (!state.loggedIn) {
      return jsonResponse(401, { detail: "Authentication required" });
    }

    if (path === "/api/accounts" && method === "GET") {
      return jsonResponse(200, state.accounts);
    }

    if (path === "/api/accounts" && method === "POST") {
      state.accounts.push({ email: body.email });
      return jsonResponse(200, { status: "applied", detail: `Account ${body.email} created` });
    }

    if (path.startsWith("/api/accounts/") && path.endsWith("/password") && method === "POST") {
      const email = decodeURIComponent(path.replace("/api/accounts/", "").replace("/password", ""));
      return jsonResponse(200, { status: "applied", detail: `Password updated for ${email}` });
    }

    if (path.startsWith("/api/accounts/") && method === "DELETE") {
      const email = decodeURIComponent(path.replace("/api/accounts/", ""));
      state.accounts = state.accounts.filter((entry) => entry.email !== email);
      state.aliases = state.aliases.filter((entry) => entry.target !== email);
      state.quotas = state.quotas.filter((entry) => entry.email !== email);
      return jsonResponse(200, { status: "applied", detail: `Account ${email} removed` });
    }

    if (path === "/api/aliases" && method === "GET") {
      return jsonResponse(200, state.aliases);
    }

    if (path === "/api/aliases" && method === "POST") {
      state.aliases.push({ address: body.address, target: body.target });
      return jsonResponse(200, { status: "applied", detail: `Alias ${body.address} created` });
    }

    if (path.startsWith("/api/aliases/") && method === "DELETE") {
      const address = decodeURIComponent(path.replace("/api/aliases/", "").split("?")[0]);
      const target = url.searchParams.get("target");
      state.aliases = state.aliases.filter(
        (entry) => !(entry.address === address && entry.target === target),
      );
      return jsonResponse(200, { status: "applied", detail: `Alias ${address} removed` });
    }

    if (path === "/api/quotas" && method === "GET") {
      return jsonResponse(200, state.quotas);
    }

    if (path === "/api/quotas" && method === "POST") {
      state.quotas = state.quotas.filter((entry) => entry.email !== body.email);
      state.quotas.push({ email: body.email, quota: body.quota });
      return jsonResponse(200, { status: "applied", detail: `Quota set for ${body.email}` });
    }

    if (path.startsWith("/api/quotas/") && method === "DELETE") {
      const email = decodeURIComponent(path.replace("/api/quotas/", ""));
      state.quotas = state.quotas.filter((entry) => entry.email !== email);
      return jsonResponse(200, { status: "applied", detail: `Quota removed for ${email}` });
    }

    if (path === "/api/relay" && method === "GET") {
      return jsonResponse(200, state.relay);
    }

    if (path === "/api/relay/domains" && method === "POST") {
      state.relay.domains.push({
        domain: body.domain,
        host: body.host,
        port: body.port,
        excluded: false,
      });
      return jsonResponse(200, { status: "applied", detail: `Relay domain ${body.domain} added` });
    }

    if (path === "/api/relay/domains/exclude" && method === "POST") {
      state.relay.domains = state.relay.domains.map((entry) =>
        entry.domain === body.domain
          ? { ...entry, excluded: true, host: null, port: null }
          : entry,
      );
      return jsonResponse(200, {
        status: "applied",
        detail: `Relay domain ${body.domain} excluded`,
      });
    }

    if (path === "/api/relay/auth" && method === "POST") {
      state.relay.auth.push({ domain: body.domain, username: body.username });
      return jsonResponse(200, { status: "applied", detail: `Relay auth for ${body.domain} added` });
    }

    if (path === "/api/system/status" && method === "GET") {
      return jsonResponse(200, state.system);
    }

    throw new Error(`Unhandled request: ${method} ${path}`);
  });

  globalThis.fetch = fetchMock as typeof fetch;
  return { fetchMock, state };
}

describe("App", () => {
  test("shows login form when no session exists", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue(
      jsonResponse(401, { detail: "Authentication required" }),
    ) as typeof fetch;

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "DMS Admin" })).toBeInTheDocument();
    });
  });

  test("supports authenticated operator flows across accounts, aliases, quotas, relay, and system", async () => {
    installMockApi();
    const user = userEvent.setup();

    render(<App />);

    await user.click(await screen.findByRole("button", { name: "Sign in" }));
    await screen.findByText("hello@example.com");

    await user.type(screen.getByPlaceholderText("user@example.com"), "new@example.com");
    await user.type(screen.getByPlaceholderText("Password"), "secret-password");
    await user.click(screen.getByRole("button", { name: "Create account" }));
    await screen.findByText("Account new@example.com created");

    await user.click(screen.getByRole("link", { name: "Aliases" }));
    await screen.findByText("postmaster@example.com");
    await user.type(screen.getByPlaceholderText("alias@example.com"), "sales@example.com");
    await user.type(screen.getByPlaceholderText("target@example.com"), "hello@example.com");
    await user.click(screen.getByRole("button", { name: "Create alias" }));
    await screen.findByText("Alias sales@example.com created");

    await user.click(screen.getByRole("link", { name: "Quotas" }));
    await screen.findByText("5 G");
    const quotaEmailInput = screen.getByPlaceholderText("user@example.com");
    await user.clear(quotaEmailInput);
    await user.type(quotaEmailInput, "new@example.com");
    await user.type(screen.getByPlaceholderText("10 G"), "10 G");
    await user.click(screen.getByRole("button", { name: "Set quota" }));
    await screen.findByText("Quota set for new@example.com");

    await user.click(screen.getByRole("link", { name: "Relay" }));
    await screen.findByText("smtp.example.com:587");
    await user.type(screen.getAllByPlaceholderText("example.com")[0], "billing.example.com");
    await user.type(screen.getByPlaceholderText("smtp.example.com"), "relay.example.net");
    await user.clear(screen.getByPlaceholderText("587"));
    await user.type(screen.getByPlaceholderText("587"), "2525");
    await user.click(screen.getByRole("button", { name: "Add relay domain" }));
    await screen.findByText("Relay domain billing.example.com added");
    await user.click(screen.getAllByRole("button", { name: "Exclude" })[0]);
    await screen.findByText("Relay domain example.com excluded");

    await user.click(screen.getByRole("link", { name: "System" }));
    await screen.findByText("mailserver");
    await screen.findByText("Yes");
  });
});
