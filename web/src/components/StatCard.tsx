import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  variant?: "default" | "primary" | "accent";
}

const variantStyles = {
  default: "bg-card shadow-card",
  primary: "gradient-primary text-primary-foreground",
  accent: "gradient-accent text-accent-foreground",
};

const iconBgStyles = {
  default: "bg-primary/10 text-primary",
  primary: "bg-primary-foreground/20 text-primary-foreground",
  accent: "bg-accent-foreground/10 text-accent-foreground",
};

export default function StatCard({ label, value, icon: Icon, variant = "default" }: StatCardProps) {
  return (
    <div
      className={cn(
        "flex items-center gap-4 rounded-xl p-5 transition-all duration-200 hover:shadow-card-hover",
        variantStyles[variant]
      )}
    >
      <div
        className={cn(
          "flex h-11 w-11 shrink-0 items-center justify-center rounded-lg",
          iconBgStyles[variant]
        )}
      >
        <Icon className="h-5 w-5" />
      </div>
      <div>
        <p className={cn("text-2xl font-bold leading-none", variant === "default" && "text-foreground")}>
          {value}
        </p>
        <p className={cn("mt-1 text-xs font-medium", variant === "default" ? "text-muted-foreground" : "opacity-80")}>
          {label}
        </p>
      </div>
    </div>
  );
}
