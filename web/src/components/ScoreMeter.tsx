import { cn } from "@/lib/utils";

interface ScoreMeterProps {
  score: number;
  maxScore?: number;
}

export default function ScoreMeter({ score, maxScore = 12 }: ScoreMeterProps) {
  const pct = Math.min((score / maxScore) * 100, 100);
  const color =
    pct >= 75 ? "bg-success" : pct >= 50 ? "bg-accent" : "bg-destructive";

  return (
    <div className="flex items-center gap-3">
      <div className="h-2 flex-1 overflow-hidden rounded-full bg-muted">
        <div
          className={cn("h-full rounded-full transition-all duration-500", color)}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm font-bold text-foreground">
        {score}/{maxScore}
      </span>
    </div>
  );
}
