import { useEffect, useState, useSyncExternalStore } from "react";

const KEY = "awesome-apis:favorites";

const listeners = new Set<() => void>();

function read(): Set<string> {
  if (typeof window === "undefined") return new Set();
  try {
    const raw = window.localStorage.getItem(KEY);
    return new Set<string>(raw ? JSON.parse(raw) : []);
  } catch {
    return new Set();
  }
}

let cache = read();

function write(next: Set<string>) {
  cache = next;
  try {
    window.localStorage.setItem(KEY, JSON.stringify(Array.from(next)));
  } catch {}
  listeners.forEach((l) => l());
}

export function toggleFavorite(name: string) {
  const next = new Set(cache);
  if (next.has(name)) next.delete(name);
  else next.add(name);
  write(next);
}

export function isFavorite(name: string) {
  return cache.has(name);
}

function subscribe(cb: () => void) {
  listeners.add(cb);
  return () => listeners.delete(cb);
}

export function useFavorites() {
  return useSyncExternalStore(
    subscribe,
    () => cache,
    () => new Set<string>()
  );
}

export function useIsMounted() {
  const [m, setM] = useState(false);
  useEffect(() => setM(true), []);
  return m;
}
