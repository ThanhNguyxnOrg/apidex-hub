import { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import { CheckCircle2, Heart, Info, X } from "lucide-react";

export type ToastType = "success" | "heart" | "info";

interface Toast {
  id: string;
  message: string;
  type: ToastType;
}

interface ToastContextType {
  showToast: (message: string, type?: ToastType) => void;
}

const ToastContext = createContext<ToastContextType>({
  showToast: () => {},
});

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((message: string, type: ToastType = "success") => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev.slice(-2), { id, message, type }]); // Keep at most 3 toasts

    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 2600);
  }, []);

  const dismissToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {/* Toast container floating at bottom right */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none max-w-sm w-full px-4">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            style={{ animation: "toastSlideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1)" }}
            className="pointer-events-auto flex items-center justify-between gap-3 px-4 py-3 rounded-xl border border-border/80 bg-card/95 backdrop-blur-md shadow-2xl text-sm font-medium text-foreground ring-1 ring-white/10"
          >
            <div className="flex items-center gap-2.5 min-w-0">
              {toast.type === "success" && (
                <CheckCircle2 size={16} className="text-emerald-500 shrink-0" />
              )}
              {toast.type === "heart" && (
                <Heart size={16} className="text-rose-500 fill-current shrink-0" />
              )}
              {toast.type === "info" && (
                <Info size={16} className="text-primary shrink-0" />
              )}
              <span className="truncate">{toast.message}</span>
            </div>
            <button
              onClick={() => dismissToast(toast.id)}
              aria-label="Dismiss notification"
              className="text-muted-foreground hover:text-foreground p-0.5 rounded-md hover:bg-secondary transition-colors"
            >
              <X size={13} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}
