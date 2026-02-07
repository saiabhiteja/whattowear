import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Check, RefreshCw, CloudSun, Clock, PartyPopper } from "lucide-react";
import {
  getRecommendations,
  EVENTS,
  WEATHER_OPTIONS,
  TIME_OPTIONS,
  type Suggestion,
} from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import ScoreMeter from "@/components/ScoreMeter";
import { useToast } from "@/hooks/use-toast";

function SuggestionCard({ suggestion, index }: { suggestion: Suggestion; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="overflow-hidden rounded-xl bg-card shadow-card transition-all duration-200 hover:shadow-card-hover"
    >
      <div className="relative aspect-square overflow-hidden">
        <img
          src={suggestion.clothing.image_url}
          alt={suggestion.clothing.clothing_type}
          className="h-full w-full object-cover"
        />
        <div className="absolute right-2 top-2 rounded-lg bg-card/90 px-2.5 py-1 text-xs font-bold text-foreground backdrop-blur-sm shadow-sm">
          #{index + 1}
        </div>
      </div>
      <div className="space-y-3 p-4">
        <div className="flex flex-wrap gap-1.5">
          <span className="rounded-md bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary">
            {suggestion.clothing.clothing_type}
          </span>
          <span className="rounded-md bg-secondary px-2 py-0.5 text-[10px] font-medium text-secondary-foreground">
            {suggestion.clothing.occasion}
          </span>
          <div className="flex items-center gap-1">
            <div
              className="h-3 w-3 rounded-full border border-border"
              style={{ backgroundColor: suggestion.clothing.dominant_color }}
            />
          </div>
        </div>

        <ScoreMeter score={suggestion.score} />

        <div className="space-y-1.5">
          {suggestion.reasons.map((reason, i) => (
            <div key={i} className="flex items-start gap-2">
              <div className="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-success/15">
                <Check className="h-2.5 w-2.5 text-success" />
              </div>
              <p className="text-xs leading-relaxed text-muted-foreground">{reason}</p>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

export default function Recommendations() {
  const { toast } = useToast();
  const [event, setEvent] = useState("");
  const [weather, setWeather] = useState("");
  const [timeOfDay, setTimeOfDay] = useState("");

  const mutation = useMutation({
    mutationFn: () => getRecommendations(event, weather, timeOfDay),
    onError: (err: Error) => {
      toast({ title: "Failed to get suggestions", description: err.message, variant: "destructive" });
    },
  });

  const canSubmit = event && weather && timeOfDay;

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Get Recommendations</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Tell us about your plans and we'll pick the perfect outfit
        </p>
      </div>

      {/* Form */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl bg-card p-6 shadow-card"
      >
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <PartyPopper className="h-4 w-4 text-primary" />
              Event
            </label>
            <Select value={event} onValueChange={setEvent}>
              <SelectTrigger>
                <SelectValue placeholder="Select event" />
              </SelectTrigger>
              <SelectContent>
                {EVENTS.map((e) => (
                  <SelectItem key={e} value={e}>
                    {e}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <CloudSun className="h-4 w-4 text-primary" />
              Weather
            </label>
            <Select value={weather} onValueChange={setWeather}>
              <SelectTrigger>
                <SelectValue placeholder="Select weather" />
              </SelectTrigger>
              <SelectContent>
                {WEATHER_OPTIONS.map((w) => (
                  <SelectItem key={w} value={w}>
                    {w}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Clock className="h-4 w-4 text-primary" />
              Time of Day
            </label>
            <Select value={timeOfDay} onValueChange={setTimeOfDay}>
              <SelectTrigger>
                <SelectValue placeholder="Select time" />
              </SelectTrigger>
              <SelectContent>
                {TIME_OPTIONS.map((t) => (
                  <SelectItem key={t} value={t}>
                    {t}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Button
          onClick={() => mutation.mutate()}
          disabled={!canSubmit || mutation.isPending}
          className="mt-6 w-full gap-2 gradient-primary text-primary-foreground sm:w-auto"
          size="lg"
        >
          {mutation.isPending ? (
            <RefreshCw className="h-4 w-4 animate-spin" />
          ) : (
            <Sparkles className="h-4 w-4" />
          )}
          {mutation.isPending ? "Finding outfits..." : "Get Suggestions"}
        </Button>
      </motion.div>

      {/* Results */}
      <AnimatePresence mode="wait">
        {mutation.data && mutation.data.suggestions.length > 0 ? (
          <motion.div
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-4"
          >
            <h2 className="text-lg font-semibold text-foreground">
              Top Picks for {mutation.data.event} · {mutation.data.weather} · {mutation.data.time_of_day}
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {mutation.data.suggestions.map((s, i) => (
                <SuggestionCard key={s.clothing.id} suggestion={s} index={i} />
              ))}
            </div>
          </motion.div>
        ) : mutation.data && mutation.data.suggestions.length === 0 ? (
          <motion.div
            key="empty"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center rounded-2xl bg-card py-16 shadow-card"
          >
            <Sparkles className="h-10 w-10 text-muted-foreground" />
            <h3 className="mt-3 text-lg font-semibold text-foreground">No suggestions found</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Try adding more clothes to your wardrobe first!
            </p>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  );
}
